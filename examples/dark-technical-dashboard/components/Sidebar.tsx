export function Sidebar() {
  // UX115: persistent rail >=1024px, overlay drawer below -- wire the drawer state in the shell.
  return (
    <aside className="hidden w-60 shrink-0 border-r border-ink/10 p-4 lg:block">
      <div className="mb-6 font-display font-bold">{/* TODO: product name */}</div>
      <nav className="space-y-1">{/* TODO: nav items with active state distinct from hover (UX046) */}</nav>
    </aside>
  );
}
