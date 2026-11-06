import { useEffect, useRef, useState } from "react"
import { motion, useReducedMotion, useScroll, useTransform } from "motion/react"
import { ArrowUpRight } from "lucide-react"
import { Cue } from "@/lib/cue"
import { LiveOrb } from "@/components/ui/live-orb"
import { Sketch, useFrames, type Hand } from "./sketch"

const ease = [0.23, 1, 0.32, 1] as const

function Rise({ children, delay = 0, className }: { children: React.ReactNode; delay?: number; className?: string }) {
  const reduce = useReducedMotion()
  return (
    <motion.div
      className={className}
      initial={reduce ? false : { opacity: 0, y: 28 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-12% 0px" }}
      transition={{ duration: 0.8, delay, ease }}
    >
      {children}
    </motion.div>
  )
}

/* ---------- the light table, rendered in Blender ---------- */
export function LightTable() {
  const ref = useRef<HTMLElement>(null)
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start end", "end start"] })
  const scale = useTransform(scrollYProgress, [0, 1], [1.12, 1])
  const reduce = useReducedMotion()
  return (
    <section ref={ref} aria-labelledby="table-title" className="relative overflow-hidden bg-night">
      <motion.img
        src="/art/lighttable-hero.webp"
        alt="A light table at night: sheets of animation paper on a peg bar, the top drawing turned and smiling, earlier drawings glowing through it."
        className="h-[min(100svh,980px)] w-full object-cover"
        style={reduce ? undefined : { scale }}
        width={2400}
        height={1350}
        loading="lazy"
      />
      <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-night via-night/70 to-transparent px-5 pb-12 pt-40 sm:px-10">
        <div className="mx-auto grid max-w-[1600px] gap-6 lg:grid-cols-2 lg:items-end">
          <h2 id="table-title" className="font-heading text-[clamp(2.2rem,1.4rem+3.2vw,4.8rem)] font-[720] leading-[0.92] tracking-[-0.04em] text-chalk">
            Every in-between<br />was drawn by hand.
          </h2>
          <p className="max-w-[46ch] text-lg leading-relaxed text-chalk/80 lg:justify-self-end">
            An animator flips sheets on a light table and draws the poses between two keys. Cue keeps your two keys and
            proposes the fourteen between them; a sentence decides what moves first.
          </p>
        </div>
      </div>
    </section>
  )
}

/* ---------- one sentence, four hands ---------- */
const HANDS: { hand: Hand; name: string; note: string; className: string }[] = [
  { hand: "pencil", name: "Graphite", note: "Rough pass on animation bond", className: "md:col-span-7 md:rotate-[-1deg]" },
  { hand: "ink", name: "Sumi ink", note: "Brush that swells on the curves", className: "md:col-span-5 md:mt-28 md:rotate-[1.4deg]" },
  { hand: "chalk", name: "Chalk on plum", note: "Broken, dusty line", className: "md:col-span-5 md:-mt-6 md:rotate-[-1.6deg]" },
  { hand: "gouache", name: "Gouache", note: "Flat colour, soft edge", className: "md:col-span-7 md:mt-16 md:rotate-[0.7deg]" },
]

function HandCard({ hand, name, note, className, index }: (typeof HANDS)[number] & { index: number }) {
  const plan = Cue.parseInstruction(Cue.EXAMPLES[2])
  const [hover, setHover] = useState(false)
  const ref = useRef<HTMLElement>(null)
  const [inView, setInView] = useState(false)
  useEffect(() => {
    const io = new IntersectionObserver(([e]) => setInView(e.isIntersecting), { threshold: 0.4 })
    if (ref.current) io.observe(ref.current)
    return () => io.disconnect()
  }, [])
  const { frames, i } = useFrames(plan, hover || inView, 5)
  return (
    <motion.figure
      ref={ref}
      className={`group ${className}`}
      onPointerEnter={() => setHover(true)}
      onPointerLeave={() => setHover(false)}
      initial={{ opacity: 0, y: 40 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-10% 0px" }}
      transition={{ duration: 0.9, delay: index * 0.08, ease }}
    >
      <div className="overflow-hidden rounded-sm shadow-[0_40px_60px_-30px_rgb(0_0_0/0.9)] transition-transform duration-500 ease-out group-hover:scale-[1.015]">
        <Sketch pose={frames[i]} hand={hand} className="aspect-[8/5] w-full" label={`${name}: frame ${i + 1}`} />
      </div>
      <figcaption className="mt-3 flex items-baseline justify-between gap-4 text-chalk">
        <span className="font-heading text-xl font-[650] tracking-[-0.02em]">{name}</span>
        <span className="text-sm text-chalk/55">{note}</span>
      </figcaption>
    </motion.figure>
  )
}

export function FourHands() {
  return (
    <section aria-labelledby="hands-title" className="bg-night px-5 py-[clamp(96px,12vw,200px)] sm:px-10">
      <div className="mx-auto max-w-[1600px]">
        <Rise className="grid gap-6 md:grid-cols-12">
          <h2 id="hands-title" className="font-heading text-[clamp(2.4rem,1.4rem+4vw,6rem)] font-[750] leading-[0.88] tracking-[-0.045em] text-chalk md:col-span-7">
            One sentence,<br /><span className="text-pink">four hands.</span>
          </h2>
          <p className="max-w-[40ch] self-end text-lg leading-relaxed text-chalk/70 md:col-span-4 md:col-start-9">
            “Glance left quickly, then raise a hand while turning, then lower it and smile.” The order is the same in every
            style; only the line changes. Hover a sheet to play it.
          </p>
        </Rise>
        <div className="mt-16 grid gap-10 md:grid-cols-12 md:gap-x-8 md:gap-y-12">
          {HANDS.map((h, k) => <HandCard key={h.hand} {...h} index={k} />)}
        </div>
        <p className="mt-10 text-sm text-chalk/45">Styles are drawn in the browser from Cue’s sketch engine; they are illustrations of a plan, not model output.</p>
      </div>
    </section>
  )
}

/* ---------- storyboard, rendered ---------- */
export function Storyboard() {
  return (
    <section aria-labelledby="board-title" className="bg-[#120d12] py-[clamp(80px,10vw,160px)]">
      <div className="mx-auto max-w-[1600px] px-5 sm:px-10">
        <Rise className="flex flex-wrap items-end justify-between gap-6">
          <h2 id="board-title" className="font-heading text-[clamp(2rem,1.3rem+2.6vw,3.8rem)] font-[720] leading-[0.95] tracking-[-0.04em] text-chalk">
            Six sheets of sixteen.
          </h2>
          <p className="max-w-[44ch] text-chalk/65">Frames 1, 4, 7, 10, 13 and 16 of the wave, laid out on the desk. The first and the last are the drawings you bring; Cue fills in the rest.</p>
        </Rise>
      </div>
      <Rise delay={0.1}>
        <img src="/art/storyboard-flat.webp" width={2520} height={700} loading="lazy" className="mt-12 w-full" alt="Six sheets of animation paper laid side by side on a dark desk, showing a character glancing left, raising a hand, turning and smiling." />
      </Rise>
    </section>
  )
}

/* ---------- history ---------- */
export function History() {
  const vid = useRef<HTMLVideoElement>(null)
  useEffect(() => {
    const v = vid.current
    if (!v || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return
    const io = new IntersectionObserver(([e]) => (e.isIntersecting ? v.play().catch(() => {}) : v.pause()), { threshold: 0.3 })
    io.observe(v)
    return () => io.disconnect()
  }, [])
  return (
    <section aria-labelledby="hist-title" className="bg-paper px-5 py-[clamp(96px,12vw,180px)] text-ink sm:px-10">
      <div className="mx-auto grid max-w-[1600px] gap-10 md:grid-cols-12">
        <Rise className="md:col-span-5">
          <h2 id="hist-title" className="font-heading text-[clamp(2.4rem,1.4rem+3.6vw,5.2rem)] font-[750] leading-[0.88] tracking-[-0.045em]">
            Inbetweening,<br />since 1833.
          </h2>
          <p className="mt-6 max-w-[42ch] text-lg leading-relaxed text-ink/75">
            Discs of twelve poses, strips spun in a drum, a horse photographed frame by frame, a clown drawn line by line.
            The craft has always been the frames in between.
          </p>
        </Rise>
        <Rise delay={0.1} className="md:col-span-7">
          <figure className="overflow-hidden rounded-sm bg-black">
            <video ref={vid} muted loop playsInline preload="none" poster="/archive/fantasmagorie-1908-poster.jpg" className="aspect-[4/3] w-full object-cover" aria-label="Émile Cohl's Fantasmagorie, 1908: a hand draws a clown in white line on black, and the drawing begins to move.">
              <source src="/archive/fantasmagorie-1908.webm" type="video/webm" />
            </video>
          </figure>
          <figcaption className="mt-2 text-sm text-ink/60">Émile Cohl, Fantasmagorie, 1908 (excerpt)</figcaption>
        </Rise>
        <Rise className="md:col-span-4"><img src="/archive/phenakistiscope-disc-dancing-man-simon.webp" alt="A hand-coloured phenakistiscope disc with a dancing figure in twelve poses." width={1024} height={1014} loading="lazy" className="w-full rounded-full" /><p className="mt-2 text-sm text-ink/60">Phenakistiscope disc, 1830s</p></Rise>
        <Rise delay={0.08} className="md:col-span-8 md:self-end"><img src="/archive/plate-number-57-walking-turning.webp" alt="Muybridge plate of a woman with a basket, walking and turning, in three rows of frames." width={1024} height={645} loading="lazy" className="w-full" /><p className="mt-2 text-sm text-ink/60">Eadweard Muybridge, Walking turning, 1887 — one motion, recorded under control, the way Cue’s dataset plans it</p></Rise>
      </div>
      <div className="mt-16 overflow-hidden" aria-hidden><img src="/archive/zoetrope-strip-dancers.jpg" alt="" width={4000} height={470} className="h-28 w-auto max-w-none md:h-40" /></div>
    </section>
  )
}

/* ---------- where the research stands ---------- */
const WEEKS = [
  ["1", "Requirements, architecture, AI pipeline", "Reviewed"],
  ["2", "Mockups, database design, capture protocol", "This site"],
  ["3", "Pilot dataset, held-out split, first baseline", "Next"],
  ["4–6", "API, database, model service, 2–3 experiments", "Planned"],
  ["7", "End to end: drawings and a sentence in, frames out", "Planned"],
  ["8–10", "Deployment, tests, held-out evaluation", "Planned"],
]
export function Research() {
  return (
    <section aria-labelledby="res-title" className="bg-night px-5 py-[clamp(96px,12vw,180px)] sm:px-10">
      <div className="mx-auto grid max-w-[1600px] gap-12 lg:grid-cols-12">
        <Rise className="lg:col-span-5">
          <h2 id="res-title" className="font-heading text-[clamp(2.2rem,1.4rem+3vw,4.4rem)] font-[720] leading-[0.92] tracking-[-0.04em] text-chalk">Where the research stands.</h2>
          <p className="mt-6 max-w-[40ch] text-lg leading-relaxed text-chalk/70">A ten-week university design project. Nothing on this page is a model result yet: the frames are drawn by a sketch engine, and the room is a Blender render.</p>
          <dl className="mt-10 grid grid-cols-2 gap-x-6 gap-y-8">
            {[["~1,000", "clips, long-term target"], ["~10 s", "per clip"], ["~15", "frames sampled per second"], ["150,000", "real ↔ drawing pairs, at most"]].map(([v, k]) => (
              <div key={k}><dd className="font-heading text-[clamp(2rem,1.5rem+1.6vw,3.2rem)] font-[650] tracking-[-0.04em] text-chalk tabular-nums">{v}</dd><dt className="mt-1 text-chalk/55">{k}</dt></div>
            ))}
          </dl>
        </Rise>
        <Rise delay={0.1} className="lg:col-span-6 lg:col-start-7">
          <ol className="divide-y divide-chalk/10 rounded-2xl bg-night-2 ring-1 ring-chalk/10">
            {WEEKS.map(([w, t, s]) => (
              <li key={w} className={`grid grid-cols-[4.5rem_1fr_auto] items-center gap-4 px-5 py-4 ${s === "This site" ? "bg-pink/10" : ""}`}>
                <span className="text-right text-sm tabular-nums text-chalk/50">Week {w}</span>
                <span className="text-chalk/90">{t}</span>
                <span className={`rounded-full px-3 py-1 text-xs font-medium ${s === "Reviewed" ? "bg-mint/15 text-mint" : s === "This site" ? "bg-pink text-[#160a10]" : "bg-chalk/10 text-chalk/70"}`}>{s}</span>
              </li>
            ))}
          </ol>
        </Rise>
      </div>
    </section>
  )
}

/* ---------- the close: the cast looks at the door ---------- */
export function Closing() {
  return (
    <section aria-labelledby="close-title" className="relative overflow-hidden bg-pink px-5 py-[clamp(96px,12vw,180px)] text-[#160a10] sm:px-10">
      <div className="mx-auto grid max-w-[1600px] items-center gap-10 md:grid-cols-[1fr_auto]">
        <div>
          <h2 id="close-title" className="font-heading text-[clamp(3rem,1.6rem+6vw,8.5rem)] font-[780] leading-[0.85] tracking-[-0.05em]">Bring two<br />drawings.</h2>
          <a href="/studio/app.html#s2" className="group mt-10 inline-flex h-14 items-center gap-3 rounded-full bg-[#160a10] px-7 text-lg font-semibold text-pink transition-transform duration-150 active:scale-[0.97]">
            Open the studio <ArrowUpRight className="size-5 transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
          </a>
        </div>
        <div className="flex items-end gap-4" aria-hidden>
          <LiveOrb size={180} theme="dark" variant="black" />
          <LiveOrb size={120} theme="dark" variant="white" />
          <LiveOrb size={80} theme="dark" variant="custom" color="#ff8a3d" eyeColor="#160a10" />
        </div>
      </div>
    </section>
  )
}

export function Footer() {
  const [time, setTime] = useState("")
  useEffect(() => {
    const f = new Intl.DateTimeFormat("en-GB", { hour: "2-digit", minute: "2-digit", timeZone: "Europe/Istanbul" })
    const tick = () => setTime(f.format(new Date()))
    tick()
    const t = setInterval(tick, 30000)
    return () => clearInterval(t)
  }, [])
  return (
    <footer className="bg-night px-5 pb-10 pt-20 text-chalk sm:px-10">
      <div className="mx-auto max-w-[1600px]">
        <p aria-hidden className="select-none font-heading text-[clamp(7rem,30vw,30rem)] font-[800] leading-[0.75] tracking-[-0.06em] text-chalk/[0.07]">Cue</p>
        <div className="mt-10 grid gap-8 text-sm text-chalk/60 md:grid-cols-4">
          <p className="text-base text-chalk/80">Language-guided drawing inbetweening. A university AI engineering design project.</p>
          <ul className="space-y-1.5">
            <li><a className="hover:text-pink" href="/studio/app.html#s2">Studio mockup</a></li>
            <li><a className="hover:text-pink" href="https://github.com/miclaldogan/language-guided-drawing-inbetweening">Source on GitHub</a></li>
            <li><a className="hover:text-pink" href="#cue-sheet">Try a sentence</a></li>
          </ul>
          <p>Elazığ, Türkiye<br /><span className="tabular-nums">{time}</span> local time</p>
          <p className="leading-relaxed">
            Archive: Cohl, <em>Fantasmagorie</em> (1908), public domain; Muybridge plate 57, phenakistiscope disc and zoetrope strip, CC0 (via Wikimedia Commons, rawpixel, Openverse). Orbs and glyph background from 21st.dev. Renders made in Blender.
          </p>
        </div>
      </div>
    </footer>
  )
}
