"""CLI, Python client and example notebook (plan-system 3.4): CLI-01…03."""
from __future__ import annotations

import io
import json
import logging
import socket
import threading
import time
from contextlib import redirect_stdout
from pathlib import Path

import pytest
import uvicorn

from api import cli
from api.client import ApiError, Client
from tests.conftest import mk_client, settings_for

SEQ = 'DIMFLVDSSGSIGPENFSKMKTFMKNLV'
APP = Path(__file__).resolve().parents[1]


@pytest.fixture()
def live(mini, dbcopy, tmp_path):
    """The real app on a free loopback port in a thread (embedded worker), for the urllib client."""
    from api.main import create_app
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    st = settings_for(mini, dbcopy, workspace_dir=tmp_path / 'ws', embedded_worker=True, worker_poll_seconds=0.1)
    server = uvicorn.Server(uvicorn.Config(create_app(st), host='127.0.0.1', port=port, log_level='warning'))
    t = threading.Thread(target=server.run, daemon=True)
    t.start()
    for _ in range(100):
        if server.started:
            break
        time.sleep(0.05)
    yield f'http://127.0.0.1:{port}'
    server.should_exit = True
    t.join(10)


def _run(argv) -> tuple[int, str]:
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = cli.run(argv)
    return code, buf.getvalue()


def test_cli01_cli_equals_api_in_both_modes(live, mini, dbcopy, monkeypatch):
    c, _ = mk_client(mini, dbcopy)
    api_cells = c.post('/v1/predict', json={'sequence': SEQ}).json()['cells']
    code, out = _run(['--api', live, 'predict', '--sequence', SEQ])
    assert code == 0
    got = json.loads(out)['cells']
    assert len(got) == 532 and all(abs(x['score_dpsi_raw'] - y['score_dpsi_raw']) < 1e-9 and
                                   abs(x['p_dpsi_ge_1_calibrated'] - y['p_dpsi_ge_1_calibrated']) < 1e-9
                                   for x, y in zip(got, api_cells, strict=True))
    monkeypatch.setenv('DF_DATABASE_URL', dbcopy)
    monkeypatch.setenv('DF_MODEL_DIR', str(mini['model_dir']))
    if c.app.state.core.settings.gate_card:
        monkeypatch.setenv('DF_GATE_CARD', str(c.app.state.core.settings.gate_card))
    code, out = _run(['--offline', 'predict', '--sequence', SEQ])
    assert code == 0 and json.loads(out)['cells'] == api_cells
    code, out = _run(['--api', live, 'predict', '--uniprot', 'P12345', '--tile', '1', '--format', 'csv'])
    assert code == 0 and out.startswith('# model_id=') and len([ln for ln in out.splitlines() if not ln.startswith('#')]) == 533


def test_cli_job_export_compare_and_errors(live, tmp_path):
    cl = Client(live)
    pid = cl.create_project('cli')['project_id']
    fa = tmp_path / 'p.fa'
    fa.write_text(f'>alpha\n{SEQ * 3}\n>beta\n{SEQ}\n')
    out = tmp_path / 'manifest.csv'
    code, _ = _run(['--api', live, 'job', '--project', pid, '--fasta', str(fa), '--override-domain', '--wait',
                    '--export', 'csv', '--out', str(out)])
    assert code == 0
    rows = [ln for ln in out.read_text().splitlines() if not ln.startswith('#')]
    assert 'input_id' in rows[0] and any(',alpha,' in r for r in rows) and any(',beta,' in r for r in rows)
    peps = tmp_path / 'peps.csv'
    peps.write_text(f'input_id,sequence\nx1,{SEQ}\nbad,ACD\n')
    code, text = _run(['--api', live, 'job', '--project', pid, '--peptides', str(peps), '--wait'])
    assert code == 0 and json.loads(text)['state'] == 'partial'
    a = cl.save_analysis(pid, sequence=SEQ)
    b = cl.save_analysis(pid, sequence=SEQ, calibrator='iso')
    code, text = _run(['--api', live, 'compare', a['analysis_id'], b['analysis_id']])
    assert code == 0 and json.loads(text)['metrics']['n_cells'] == 532
    code, _ = _run(['--api', live, 'predict', '--sequence', 'ACD'])
    assert code == 2
    with pytest.raises(ApiError) as e:
        cl.predict(sequence='ACD')
    assert e.value.code == 'INVALID_LENGTH'


def test_cli02_no_sequence_in_the_log(live, caplog):
    with caplog.at_level(logging.DEBUG):
        code, out = _run(['--api', live, 'predict', '--sequence', SEQ])
    assert code == 0 and SEQ in out                           # the result itself goes to stdout
    text = '\n'.join(r.getMessage() for r in caplog.records)
    assert 'scored 532 cells' in text and SEQ not in text


def test_cli03_notebook_runs_from_start_to_end(live, monkeypatch):
    """Executes the code cells of docs/notebooks/degron-footprint-client.ipynb in order against the live app (no
    Jupyter needed: the cells are plain Python)."""
    nb = json.loads((APP / 'docs/notebooks/degron-footprint-client.ipynb').read_text())
    monkeypatch.setenv('DF_API_URL', live)
    monkeypatch.setenv('DF_NOTEBOOK_WAIT', '60')
    ns: dict = {}
    buf = io.StringIO()
    with redirect_stdout(buf):
        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                exec(compile(''.join(cell['source']), 'notebook', 'exec'), ns)     # noqa: S102 (our own notebook)
    out = buf.getvalue()
    assert 'domain:' in out and 'evidence:' in out and 'completed' in out and '532 substitutions' in out
