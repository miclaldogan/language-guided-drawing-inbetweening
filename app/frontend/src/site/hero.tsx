import { motion, useReducedMotion } from "motion/react"
import { ArrowDownRight, ArrowUpRight } from "lucide-react"
import { GlyphBackground } from "@/components/ui/backgrounds-glyph"
import { LiveOrb } from "@/components/ui/live-orb"
import { Cue } from "@/lib/cue"
import { Sketch } from "./sketch"
import { useMedia } from "./use-media"

/** The cast: one orb per lane of the cue sheet. They watch the pointer — eyes first. */
export const CAST = {
  gaze: { label: "Gaze", variant: "white" as const },
  head: { label: "Head", variant: "custom" as const, color: "#ff4f8b", eyeColor: "#160a10" },
  smile: { label: "Expression", variant: "webgl" as const, colors: ["#ff4f8b", "#ff8a3d", "#8fe3cf"] },
  hand: { label: "Hand", variant: "custom" as const, color: "#ff8a3d", eyeColor: "#160a10" },
}

function CastOrb({ lane, size, className, delay = 0 }: { lane: keyof typeof CAST; size: number; className: string; delay?: number }) {
  const c = CAST[lane]
  const reduce = useReducedMotion()
  return (
    <motion.figure
      className={`pointer-events-none absolute flex flex-col items-center gap-2 ${className}`}
      initial={reduce ? false : { opacity: 0, scale: 0.9, y: 12 }}
      animate={{ opacity: 1, scale: 1, y: 0 }}
      transition={{ duration: 0.9, delay, ease: [0.23, 1, 0.32, 1] }}
    >
      <LiveOrb
        size={size}
        theme="dark"
        variant={c.variant}
        color={"color" in c ? c.color : undefined}
        eyeColor={"eyeColor" in c ? c.eyeColor : undefined}
        colors={"colors" in c ? c.colors : undefined}
      />
      <figcaption className="rounded-full bg-night/70 px-2.5 py-0.5 text-[13px] font-medium tracking-tight text-chalk/80">
        {c.label}
      </figcaption>
    </motion.figure>
  )
}

function Pinned({ children, rotate, className, caption }: { children: React.ReactNode; rotate: number; className: string; caption: string }) {
  const reduce = useReducedMotion()
  return (
    <motion.figure
      className={`absolute ${className}`}
      initial={reduce ? false : { opacity: 0, y: 30, rotate: rotate * 2 }}
      animate={{ opacity: 1, y: 0, rotate }}
      transition={{ duration: 1.1, delay: 0.35, ease: [0.23, 1, 0.32, 1] }}
    >
      <div className="relative bg-paper p-2 shadow-[0_30px_60px_-20px_rgb(0_0_0/0.8)]">
        <span aria-hidden className="absolute -top-3 left-1/2 h-6 w-16 -translate-x-1/2 rotate-[-3deg] bg-pink/80" />
        {children}
      </div>
      <figcaption className="mt-2 text-[13px] text-chalk/60">{caption}</figcaption>
    </motion.figure>
  )
}

export function Hero() {
  const wide = useMedia("(min-width: 768px)", true)
  return (
    <GlyphBackground
      className="relative min-h-[100svh] w-full text-[#8d7f93]"
      shapeColor="#ff4f8b"
      fontSize={11}
    >
      <div className="relative z-10 mx-auto flex min-h-[100svh] max-w-[1600px] flex-col justify-between px-5 pb-10 pt-28 sm:px-10">
        <h1 className="pointer-events-none select-none font-heading text-[clamp(2.5rem,10.5vw,11rem)] font-[750] leading-[0.86] tracking-[-0.045em] text-chalk">
          <span className="block">Draw the ends.</span>
          <span className="mt-[0.06em] block sm:pl-[14vw] sm:pr-[2vw] sm:text-right">
            Say the <em className="not-italic text-pink">middle.</em>
          </span>
        </h1>
        {/* on a phone the cast stands in a row under the title */}
        {!wide && <div className="mt-10 flex items-end gap-4" aria-label="The cast: gaze, head, expression, hand">
          {(["gaze", "head", "smile", "hand"] as const).map((lane, k) => (
            <figure key={lane} className="flex flex-col items-center gap-1.5">
              <LiveOrb size={[58, 82, 54, 40][k]} theme="dark" variant={CAST[lane].variant}
                color={"color" in CAST[lane] ? (CAST[lane] as { color: string }).color : undefined}
                eyeColor={"eyeColor" in CAST[lane] ? (CAST[lane] as { eyeColor: string }).eyeColor : undefined}
                colors={"colors" in CAST[lane] ? (CAST[lane] as { colors: string[] }).colors : undefined} />
              <figcaption className="text-xs text-chalk/70">{CAST[lane].label}</figcaption>
            </figure>
          ))}
        </div>}

        <div className="relative z-20 mt-10 grid gap-8 md:mt-[26vh] md:grid-cols-[minmax(0,34rem)_1fr] md:items-end">
          <div>
            <p className="max-w-[34ch] text-[clamp(1.1rem,1rem+0.5vw,1.45rem)] leading-snug text-chalk/85">
              Cue generates the sixteen frames between your first and last drawing. One English sentence sets the order:
              eyes first, then the head, then the smile.
            </p>
            <div className="mt-7 flex flex-wrap items-center gap-3">
              <a
                href="/studio/app.html#s2"
                className="group inline-flex h-12 items-center gap-2 rounded-full bg-pink px-6 font-semibold text-[#160a10] transition-transform duration-150 ease-out active:scale-[0.97]"
              >
                Open the studio
                <ArrowUpRight className="size-4 transition-transform duration-200 group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
              </a>
              <a href="#cue-sheet" className="inline-flex h-12 items-center gap-2 rounded-full px-5 font-medium text-chalk ring-1 ring-chalk/25 transition-colors hover:bg-chalk/10">
                Write a sentence <ArrowDownRight className="size-4" />
              </a>
            </div>
          </div>
          <p className="hidden justify-self-end text-right text-[13px] text-chalk/50 md:block">
            The dark is made of letters. Click it.
          </p>
        </div>
      </div>

      {/* the cast and the two keyframes, pinned to the light table */}
      <div className="pointer-events-none absolute inset-0 z-0 mx-auto max-w-[1600px]" aria-hidden={false}>
        <Pinned rotate={-4} className="left-[57%] top-[47%] hidden w-[15vw] min-w-[170px] max-w-[260px] lg:block" caption="Frame 1 · your start drawing">
          <Sketch pose={Cue.START} className="aspect-[8/5] w-full" label="Start drawing: facing forward" />
        </Pinned>
        <Pinned rotate={3} className="left-[76%] top-[50%] hidden w-[15vw] min-w-[170px] max-w-[260px] lg:block" caption="Frame 16 · your end drawing">
          <Sketch pose={Cue.END} className="aspect-[8/5] w-full" label="End drawing: turned left, smiling" />
        </Pinned>
        {wide && <>
        <CastOrb lane="gaze" size={124} className="left-[4%] top-[47%] hidden md:flex" delay={0.2} />
        <CastOrb lane="head" size={190} className="left-[18%] top-[45%] hidden md:flex" delay={0.35} />
        <CastOrb lane="smile" size={108} className="left-[37%] top-[49%] hidden md:flex" delay={0.5} />
        <CastOrb lane="hand" size={76} className="left-[48%] top-[57%] hidden md:flex" delay={0.65} />
        </>}
      </div>
    </GlyphBackground>
  )
}
