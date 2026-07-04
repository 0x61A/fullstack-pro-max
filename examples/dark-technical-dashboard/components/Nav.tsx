export function Nav() {
  // UX115/UX116: pick the mobile collapse pattern deliberately (drawer vs bottom tabs).
  return (
    <header className="sticky top-0 z-40 border-b border-ink/10 bg-base/90 backdrop-blur">
      <nav className="mx-auto flex h-14 max-w-6xl items-center justify-between px-6">
        <a href="/" className="font-display font-bold">{/* TODO: wordmark */}</a>
        <div className="hidden gap-6 md:flex">{/* TODO: 3-5 links max */}</div>
        <button className="md:hidden" aria-label="Menu">{/* TODO: drawer trigger */}</button>
      </nav>
    </header>
  );
}
