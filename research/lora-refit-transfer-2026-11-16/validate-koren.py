"""Validate S4 parsing and variable-length inference without changing core code."""
import importlib.util
import json
from pathlib import Path
import sys
import uuid
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('koren',HERE/'score-koren.py')
koren=importlib.util.module_from_spec(spec);spec.loader.exec_module(koren)
import numpy as np
import pandas as pd
import torch
from degron_v3.common import atomic_json
from degron_v3.data import Dataset
from degron_v3.finetune import MutationRegressor,infer
from degron_v3.plm import Encoder
from degron_v3.local_training import predict
from degron_v3.local_control import Control,Paused,process_lock
from degron_v3.local_campaign import implementation_hash


def main():
    frame,qc=koren.parse_source()
    root=HERE/'local'/('koren-validation-'+uuid.uuid4().hex);root.mkdir(parents=True)
    torch.set_num_threads(2);torch.cuda.set_per_process_memory_fraction(.75)
    ds=Dataset(koren.ROOT/'data/processed/degron-data-v3-fullpsi')
    fixture=ds.sat[koren.FEATURES].head(16)
    reports=[]
    for mode in ['lora','frozen']:
        base=MutationRegressor(Encoder('esm2_8m',[koren.V3/'output/local/weights',koren.V3/'output/weights'],'cuda','float32'),mode,17)
        normal=infer(base,fixture,batch=8);adapter=koren.VariableLength(base)
        adapted=infer(adapter,fixture,batch=8)
        assert np.array_equal(koren.variable_aux(fixture),koren.features(fixture,'composition'))
        assert np.allclose(normal,adapted,atol=1e-5,rtol=1e-5)
        synthetic=[]
        for length in [12,23]:
            seq=('ACDEFGHIKLMNPQRSTVWY'*2)[:length]
            for pos in [1,length]:
                mutant='V' if seq[pos-1]!='V' else 'A'
                synthetic.append(dict(cell_id=f'{length}-{pos}',peptide_id=f'p{length}',group_id=f'g{length}',
                    wt_sequence=seq,mutant_sequence=seq[:pos-1]+mutant+seq[pos:],position_1based=pos,
                    wt_aa=seq[pos-1],mut_aa=mutant))
        synthetic=pd.DataFrame(synthetic*4)
        synthetic['cell_id']=[f'synthetic-{i}' for i in range(len(synthetic))]
        folder=root/mode;folder.mkdir()
        full=predict(adapter,synthetic,folder/'full.npy',Control(folder,'test'))
        class StopAt8(Control):
            def log(self,message,force=False,**progress):
                if progress.get('rows',0)>=8:self.requested=True
        try:predict(adapter,synthetic,folder/'resumed.npy',StopAt8(folder,'test'))
        except Paused:pass
        assert json.loads((folder/'resumed.json').read_text())['completed']==8
        resumed=predict(adapter,synthetic,folder/'resumed.npy',Control(folder,'test'))
        assert np.array_equal(full,resumed) and np.isfinite(full).all()
        reports.append(dict(mode=mode,parity_28aa_max_abs=float(abs(normal-adapted).max()),
            variable_lengths=[12,23],residue_positions_checked='first_and_last',
            prefix_resume_exact=True,finite=True))
        del adapter,base;koren.gc.collect();torch.cuda.empty_cache()
    plan=koren.read(koren.LOCAL/'aa4fc2b7ce29abf9/plan.json') if hasattr(koren,'LOCAL') else koren.read(koren.V3/'output/local/aa4fc2b7ce29abf9/plan.json')
    assert implementation_hash()==plan['code_sha256']
    report=dict(status='pass',scope='parser_QC_and_synthetic_8M_inference_not_S4_efficacy',
        source_sha256=koren.sha256(koren.RAW),source_bytes=koren.RAW.stat().st_size,substrates=9,parsed_rows=1827,
        mutants=len(frame),QC=qc,inference=reports,core_code_unchanged=True,
        script_sha256=koren.sha256(HERE/'score-koren.py'),protocol_sha256=koren.sha256(HERE/'KOREN-PROTOCOL.md'))
    atomic_json(HERE/'koren-validation.json',report)
    print(json.dumps(report,indent=2))


if __name__=='__main__':
    local=koren.V3/'output/local'
    with process_lock(local/'session.lock'):
        with process_lock(local/'worker.lock'):main()
