import { ArrowUpRight } from "lucide-react"

export function Header() {
  return (
    <header className="fixed inset-x-0 top-0 z-50 px-5 pt-5 sm:px-10">
      <nav aria-label="Main" className="mx-auto flex max-w-[1600px] items-center justify-between">
        <a href="/" className="flex h-11 items-center gap-2.5 rounded-full bg-night-2/95 px-4 text-chalk ring-1 ring-chalk/10" aria-label="Cue, home">
          <svg viewBox="0 0 40 28" className="h-6 w-auto" aria-hidden>
            <rect x="1" y="4" width="14" height="20" rx="2" fill="none" stroke="currentColor" strokeWidth="2.2" />
            <rect x="25" y="4" width="14" height="20" rx="2" fill="none" stroke="currentColor" strokeWidth="2.2" />
            <circle cx="20" cy="14" r="3.2" fill="#ff4f8b" />
          </svg>
          <span className="font-heading text-xl font-[700] tracking-[-0.03em]">Cue</span>
        </a>
        <div className="flex items-center gap-1 rounded-full bg-night-2/95 p-1 ring-1 ring-chalk/10">
          <a href="#cue-sheet" className="hidden rounded-full px-4 py-2 text-sm text-chalk/80 transition-colors hover:bg-chalk/10 hover:text-chalk sm:block">Try it</a>
          <a href="#hands" className="hidden rounded-full px-4 py-2 text-sm text-chalk/80 transition-colors hover:bg-chalk/10 hover:text-chalk sm:block">Hands</a>
          <a href="#research" className="hidden rounded-full px-4 py-2 text-sm text-chalk/80 transition-colors hover:bg-chalk/10 hover:text-chalk sm:block">Research</a>
          <a href="/studio/app.html#s1" className="inline-flex items-center gap-1 rounded-full bg-chalk px-4 py-2 text-sm font-semibold text-ink transition-transform duration-150 active:scale-[0.97]">
            Studio <ArrowUpRight className="size-3.5" />
          </a>
        </div>
      </nav>
    </header>
  )
}
