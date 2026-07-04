export function DataTable() {
  // UX118: below tablet width this should render as labeled cards, not a squeezed table.
  return (
    <div className="overflow-x-auto rounded-lg border border-ink/10">
      <table className="w-full text-sm">
        <thead className="bg-surface text-left text-ink/60">
          <tr>{/* TODO: th cells -- tabular-nums on numeric columns */}</tr>
        </thead>
        <tbody>{/* TODO: rows; hover actions need touch equivalents (UX120) */}</tbody>
      </table>
    </div>
  );
}
