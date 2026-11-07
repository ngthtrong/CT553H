/** Rule W-6: attribution and disclaimer directly beside the ClinVar toggle and in the hover card. */
export function ClinvarNotice({ attribution, disclaimer }: { attribution: string; disclaimer: string }) {
  return (
    <p className="muted" data-testid="clinvar-notice" style={{ margin: '0.25rem 0' }}>
      {attribution} {disclaimer}
    </p>
  );
}
