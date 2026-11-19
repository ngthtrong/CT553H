/**
 * Glossary (plan-system 5.1). Wording follows system/srs.md §1.4; "domain gate", "raw score" and "top 10 %" are not in
 * §1.4 and follow the interface texts (domain banner, ui-design §5, priority panel). Explanations only: they never
 * replace the limitation labels next to the numbers (R-1).
 */
export const GLOSSARY = {
  psi: { term: 'PSI', text: 'Protein stability index of the GPS reporter assay (Zhang et al. 2023): the reporter cells sorted into stability bins. Higher PSI means a more stable reporter.' },
  dpsi: { term: 'ΔPSI', text: 'PSI(mutant) − PSI(wild type). A positive ΔPSI means greater reporter stability in this assay, i.e. the substitution weakens the degron signal.' },
  tile: { term: 'Tile', text: 'A full 28-residue window of a protein, taken every 23 residues (5 residues overlap). Each tile is scored on its own; a cell is one of its 532 non-wild-type substitutions.' },
  domain: { term: 'Domain gate', text: 'The R3 gate decides whether a tile resembles the tiles the model was trained on (tiles that behave as degrons). Outside the domain the scores are refused unless you override; borderline tiles carry a warning.' },
  calibration: { term: 'Calibrated probability', text: "Estimate of P(ΔPSI ≥ 1.0) in the model's assay and domain, from a calibrator fitted on out-of-fold predictions. It is separate from the raw regression score and is not a probability of disease." },
  raw: { term: 'Raw score', text: 'The regression output of the model for ΔPSI. Not a probability and not clipped; scores of different models need not share a scale.' },
  top10: { term: 'Top 10 %', text: 'The 54 substitutions with the highest raw score within this tile (ceil(10 % × 532)). A ranking inside one tile, never across tiles; retrospective, development benchmark.' },
} as const;

export type GlossaryId = keyof typeof GLOSSARY;
