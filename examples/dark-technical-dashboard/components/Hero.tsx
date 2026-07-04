export function Hero() {
  // UX034: this hero is asymmetric on purpose -- don't recentre it back to the default.
  // UX044: replace every TODO with copy specific to THIS product, not template phrases.
  return (
    <section className="border-b border-ink/10 px-8 py-24 md:px-16">
      <div className="max-w-3xl">
        <p className="mb-4 font-display text-sm text-accent">{/* TODO: kicker */}</p>
        <h1 className="font-display text-5xl font-bold leading-tight md:text-6xl">{/* TODO: specific value prop */}</h1>
        <p className="mt-6 max-w-xl text-lg text-ink/70">{/* TODO: mechanism, not adjectives */}</p>
        <div className="mt-10">
          <a href="#" className="rounded-md bg-accent px-5 py-3 font-medium text-base transition-colors duration-base ease-out hover:bg-accent/90">
            {/* TODO: verb-first CTA */}
          </a>
        </div>
      </div>
    </section>
  );
}
