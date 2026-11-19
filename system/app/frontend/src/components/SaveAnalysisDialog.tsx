import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Save } from 'lucide-react';
import { workspace } from '../api/client';
import type { TileRequest } from '../api/types';
import { ErrorBanner } from './ErrorBanner';
import { ModelSelect } from './ModelSelect';
import { Button, Dialog } from './ui';
import { ProjectPicker } from './workspace';

/** Explicit save of a preview (FR-32): the result is recomputed and stored with its provenance and annotations. */
export function SaveAnalysisDialog({ request, parentAnalysisId, label = 'Save to project', defaultProject = '', chooseModel = false }: {
  request: TileRequest;
  parentAnalysisId?: string;
  label?: string;
  defaultProject?: string;
  /** "Run again" lets the user pick another model (plan-system 1.1); the result is always a new analysis (A-5). */
  chooseModel?: boolean;
}) {
  const [open, setOpen] = useState(false);
  const [project, setProject] = useState(defaultProject);
  const [modelId, setModelId] = useState<string | undefined>(undefined);
  const navigate = useNavigate();
  const qc = useQueryClient();
  const save = useMutation({
    mutationFn: () => workspace.saveAnalysis(project, chooseModel && modelId ? { ...request, model_id: modelId } : request, parentAnalysisId),
    onSuccess: (a) => {
      void qc.invalidateQueries({ queryKey: ['analyses', a.project_id] });
      void qc.invalidateQueries({ queryKey: ['projects'] });
      setOpen(false);
      navigate(`/analyses/${a.analysis_id}`);
    },
  });
  return (
    <>
      <Button variant={parentAnalysisId ? 'secondary' : 'primary'} icon={Save} onClick={() => { save.reset(); setOpen(true); }}>
        {label}
      </Button>
      <Dialog
        open={open}
        title={parentAnalysisId ? 'Run again as a new analysis' : 'Save this analysis'}
        onClose={() => setOpen(false)}
        actions={<><Button onClick={() => setOpen(false)}>Cancel</Button><Button variant="primary" icon={Save} busy={save.isPending} disabled={!project} onClick={() => save.mutate()}>Save</Button></>}
      >
        <p>
          {parentAnalysisId
            ? 'The saved input is scored again with the model you choose (by default the service default). The result is stored as a new analysis linked to this one; the original is not changed.'
            : 'The input, the result, the model version and the annotations of today are stored in the project on this computer. Reopening it later shows exactly this result.'}
        </p>
        <ProjectPicker value={project} onChange={setProject} />
        {chooseModel && <ModelSelect value={modelId} onChange={setModelId} testId="rerun-model-select" />}
        {save.isError && <ErrorBanner error={save.error} />}
      </Dialog>
    </>
  );
}
