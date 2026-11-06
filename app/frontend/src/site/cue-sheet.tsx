import { useEffect, useMemo, useState } from "react"
import { AnimatePresence, motion, useReducedMotion } from "motion/react"
import { ChevronLeft, ChevronRight, Pause, Play, TriangleAlert } from "lucide-react"
import { Cue, type CueEvent, type Plan, type Region } from "@/lib/cue"
import { LiveOrb } from "@/components/ui/live-orb"
import { CAST } from "./hero"
import { Sketch, useFrames } from "./sketch"
import { useMedia } from "./use-media"

const LANES: Region[] = ["gaze", "head", "smile", "hand"]
const SPEED = { slow: "slowly", normal: "normal speed", fast: "quickly" } as const
const CHIPS = [
  { label: "Eyes, then head, then smile", text: Cue.EXAMPLES[0] },
  { label: "All at once", text: Cue.EXAMPLES[1] },
  { label: "With a wave", text: Cue.EXAMPLES[2] },
  { label: "Turn right", text: "Turn the head to the right and smile." },
]
const colWord = (i: number, n: number) => (n === 1 ? "Together" : i === 0 ? "First" : i === n - 1 ? "Last" : "Then")

type Ordered = { si: number; e: CueEvent; n: number }

function order(plan: Plan): Ordered[] {
  if (!plan.ok) return []
  const out: Ordered[] = []
  plan.steps.forEach((st, si) => st.events.forEach((e) => out.push({ si, e, n: 0 })))
  out.sort((a, b) => a.si - b.si || LANES.indexOf(a.e.region) - LANES.indexOf(b.e.region))
  out.forEach((o, i) => (o.n = i + 1))
  return out
}

function LaneOrb({ lane }: { lane: Region }) {
  const c = CAST[lane]
  return (
    <LiveOrb
      size={34}
      theme="dark"
      blink
      variant={c.variant}
      color={"color" in c ? c.color : undefined}
      eyeColor={"eyeColor" in c ? c.eyeColor : undefined}
      colors={"colors" in c ? c.colors : undefined}
    />
  )
}

export function CueSheet({ seed }: { seed?: string }) {
  const [text, setText] = useState(seed ?? Cue.EXAMPLES[0])
  const [planned, setPlanned] = useState(text)
  const [playing, setPlaying] = useState(false)
  const [onion, setOnion] = useState(true)
  const reduce = useReducedMotion()
  const wide = useMedia("(min-width: 768px)", true)

  useEffect(() => {
    if (seed) { setText(seed); setPlanned(seed) }
  }, [seed])
  useEffect(() => {
    const t = setTimeout(() => setPlanned(text), 380)
    return () => clearTimeout(t)
  }, [text])

  const plan = useMemo(() => Cue.parseInstruction(planned), [planned])
  const ordered = useMemo(() => order(plan), [plan])
  const stale = text !== planned
  const usable = plan.ok ? plan : Cue.parseInstruction("")
  const { frames, i, setI } = useFrames(usable, playing, 3)
  const n = plan.ok && !plan.empty ? plan.steps.length : 1
  const planKey = JSON.stringify(plan)

  const step = (d: number) => { setPlaying(false); setI((c) => (c + d + 16) % 16) }

  return (
    <section id="cue-sheet" aria-labelledby="cue-title" className="relative bg-night px-5 py-[clamp(96px,12vw,180px)] sm:px-10">
      <div className="mx-auto max-w-[1600px]">
        <div className="grid gap-10 lg:grid-cols-[minmax(0,5fr)_minmax(0,7fr)] lg:gap-16">
          {/* the sentence */}
          <div>
            <h2 id="cue-title" className="font-heading text-[clamp(2.4rem,1.6rem+3vw,4.6rem)] font-[720] leading-[0.92] tracking-[-0.04em] text-chalk">
              Type the middle.
            </h2>
            <p className="mt-5 max-w-[42ch] text-lg leading-relaxed text-chalk/70">
              Write the order of the motion in plain English. The cast below reads it, lane by lane, and the sixteen frames
              are redrawn. Everything runs in your browser.
            </p>
            <label htmlFor="cue-text" className="mt-10 block text-sm font-medium text-chalk/60">Describe the motion (optional)</label>
            <textarea
              id="cue-text"
              rows={4}
              value={text}
              spellCheck={false}
              onChange={(e) => setText(e.target.value)}
              className="mt-3 w-full resize-none rounded-2xl bg-night-2 p-5 font-heading text-[clamp(1.25rem,1.1rem+0.6vw,1.7rem)] leading-snug tracking-[-0.015em] text-chalk ring-1 ring-chalk/15 transition-shadow placeholder:text-chalk/30 focus:outline-none focus:ring-2 focus:ring-pink"
              placeholder="First move the eyes to the left, then turn the head."
            />
            <div className="mt-4 flex flex-wrap gap-2" role="group" aria-label="Example sentences">
              {CHIPS.map((c) => (
                <button
                  key={c.label}
                  type="button"
                  onClick={() => { setText(c.text); setPlanned(c.text) }}
                  aria-pressed={planned === c.text}
                  className="h-9 rounded-full px-4 text-sm text-chalk/80 ring-1 ring-chalk/20 transition-[background-color,transform] duration-150 active:scale-[0.96] hover:bg-chalk/10 aria-pressed:bg-pink aria-pressed:text-[#160a10] aria-pressed:ring-pink"
                >
                  {c.label}
                </button>
              ))}
            </div>
          </div>

          {/* the light table: the frame, big, on paper */}
          <div>
            <div className="relative overflow-hidden rounded-[22px] bg-paper p-3 shadow-[0_40px_80px_-40px_rgb(255_79_139/0.35)]">
              <Sketch pose={frames[i]} onion={onion && i > 0 ? frames[i - 1] : null} className="aspect-[8/5] w-full" label={`Frame ${i + 1} of 16`} />
              <span className="absolute left-5 top-5 rounded-full bg-ink/85 px-3 py-1 text-[13px] font-medium text-chalk tabular-nums">
                {i === 0 ? "Frame 1 · your drawing" : i === 15 ? "Frame 16 · your drawing" : `Frame ${i + 1}${onion ? ` · onion skin shows ${i}` : ""}`}
              </span>
            </div>
            <div className="mt-4 flex flex-wrap items-center gap-2">
              <button type="button" onClick={() => step(-1)} aria-label="Previous frame" className="grid size-11 place-items-center rounded-full text-chalk ring-1 ring-chalk/20 active:scale-95 hover:bg-chalk/10"><ChevronLeft className="size-5" /></button>
              <button type="button" onClick={() => setPlaying((p) => !p)} aria-label={playing ? "Pause" : "Play"} className="grid size-11 place-items-center rounded-full bg-chalk text-ink active:scale-95">{playing ? <Pause className="size-5" /> : <Play className="size-5 translate-x-px" />}</button>
              <button type="button" onClick={() => step(1)} aria-label="Next frame" className="grid size-11 place-items-center rounded-full text-chalk ring-1 ring-chalk/20 active:scale-95 hover:bg-chalk/10"><ChevronRight className="size-5" /></button>
              <span className="ml-2 tabular-nums text-chalk/60">Frame {i + 1} of 16</span>
              <label className="ml-auto inline-flex h-11 cursor-pointer items-center gap-2 text-chalk/70">
                <input type="checkbox" checked={onion} onChange={(e) => setOnion(e.target.checked)} className="size-4 accent-pink" /> Onion skin
              </label>
            </div>
            <div className="mt-4 grid grid-cols-8 gap-1.5 sm:grid-cols-16" role="listbox" aria-label="Sixteen frames">
              {frames.map((p, k) => (
                <button
                  key={k}
                  type="button"
                  role="option"
                  aria-selected={k === i}
                  aria-label={`Frame ${k + 1}`}
                  onClick={() => { setPlaying(false); setI(k) }}
                  className={`overflow-hidden rounded-md bg-paper ring-offset-2 ring-offset-night transition-transform duration-150 active:scale-95 ${k === i ? "ring-2 ring-pink" : ""} ${k === 0 || k === 15 ? "outline outline-2 -outline-offset-2 outline-ink" : ""}`}
                >
                  <Sketch pose={p} className="pointer-events-none aspect-[8/5] w-full" />
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* the cue sheet: one lane per member of the cast */}
        <div className={`mt-16 transition-[opacity,filter] duration-200 ${stale ? "opacity-50 blur-[1px]" : ""}`}>
          <div className="flex items-baseline justify-between gap-4">
            <h3 className="font-heading text-2xl font-[650] tracking-[-0.02em] text-chalk">The plan</h3>
            <span className="text-sm text-chalk/50">{stale ? "Reading your sentence…" : plan.ok && !plan.empty ? "Order shown, not exact timing" : ""}</span>
          </div>

          {!plan.ok ? (
            <div role="alert" className="mt-5 flex gap-4 rounded-2xl bg-[#3a2410] p-6 text-[#ffd9b8]">
              <TriangleAlert className="mt-0.5 size-6 shrink-0 text-ember" />
              <div>
                <p className="text-lg font-semibold">Cue couldn’t turn this into a plan.</p>
                <p className="mt-1 max-w-[60ch]">{plan.reason}</p>
                <button type="button" onClick={() => { setText(plan.suggestion); setPlanned(plan.suggestion) }} className="mt-3 font-medium text-ember underline underline-offset-4">
                  Try: “{plan.suggestion}”
                </button>
              </div>
            </div>
          ) : plan.empty ? (
            <p className="mt-5 rounded-2xl bg-night-2 p-6 text-lg text-chalk/75">No sentence, no plan: the eyes, the head and the smile all move together from the first drawing to the last.</p>
          ) : (
            <>
            {!wide && <ol className="mt-5 grid gap-2" aria-label="Plan in reading order">
              {ordered.map((o) => (
                <li key={o.n} className={`flex items-center gap-3 rounded-xl px-3 py-3 ${o.e.added ? "border border-dashed border-chalk/30 text-chalk" : "bg-pink text-[#160a10]"}`}>
                  <span aria-hidden className="size-7 shrink-0 rounded-full ring-2 ring-[#160a10]/20" style={{ background: o.e.region === "gaze" ? "#f4f4f5" : o.e.region === "head" ? "#ff4f8b" : o.e.region === "hand" ? "#ff8a3d" : "conic-gradient(#ff4f8b,#ff8a3d,#8fe3cf,#ff4f8b)" }} />
                  <span className="leading-tight"><span className="block font-semibold">{colWord(o.si, n)}: {o.e.action}</span><span className={`block text-[13px] ${o.e.added ? "text-chalk/55" : "text-[#4a0a24]"}`}>{CAST[o.e.region].label} · {o.e.added ? "added by Cue" : SPEED[o.e.speed]}</span></span>
                </li>
              ))}
            </ol>}
            {wide && <div className="mt-5 overflow-x-auto rounded-2xl bg-night-2 ring-1 ring-chalk/10">
              <div className="min-w-[640px]">
                <div className="grid border-b border-chalk/10 text-sm text-chalk/50" style={{ gridTemplateColumns: `180px repeat(${n}, minmax(0,1fr))` }}>
                  <div className="px-5 py-3" />
                  {Array.from({ length: n }, (_, k) => <div key={k} className="border-l border-chalk/10 px-4 py-3">{colWord(k, n)}</div>)}
                </div>
                {LANES.map((lane) => {
                  const mine = ordered.filter((o) => o.e.region === lane)
                  return (
                    <div key={lane} className="grid min-h-[76px] border-b border-chalk/10 last:border-b-0" style={{ gridTemplateColumns: `180px repeat(${n}, minmax(0,1fr))` }}>
                      <div className="flex items-center gap-3 px-5"><LaneOrb lane={lane} /><span className="text-chalk/80">{CAST[lane].label}</span></div>
                      {mine.length === 0 ? (
                        <div className="relative flex items-center border-l border-chalk/10 px-4 text-sm text-chalk/45" style={{ gridColumn: `2 / span ${n}` }}>
                          {lane === "hand" ? "No change" : <><span aria-hidden className="absolute inset-x-4 top-1/2 border-t border-dashed border-chalk/20" /><span className="relative bg-night-2 pr-3">Follows the drawings across the clip</span></>}
                        </div>
                      ) : (
                        Array.from({ length: n }, (_, k) => (
                          <div key={k} className="flex items-center border-l border-chalk/10 p-2.5">
                            <AnimatePresence mode="popLayout">
                              {mine.filter((o) => o.si === k).map((o) => (
                                <motion.div
                                  key={planKey + o.n}
                                  initial={reduce ? false : { opacity: 0, x: -10 }}
                                  animate={{ opacity: 1, x: 0 }}
                                  transition={{ duration: 0.26, delay: reduce ? 0 : Math.min(o.n * 0.06, 0.36), ease: [0.23, 1, 0.32, 1] }}
                                  className={`flex w-full items-center gap-3 rounded-xl px-3 py-2.5 ${o.e.added ? "border border-dashed border-chalk/30" : "bg-pink text-[#160a10]"}`}
                                >
                                  <span className={`grid size-6 shrink-0 place-items-center rounded-full text-xs font-bold tabular-nums ${o.e.added ? "bg-chalk/15 text-chalk" : "bg-[#160a10] text-pink"}`}>{o.n}</span>
                                  <span className="leading-tight">
                                    <span className="block font-semibold">{o.e.action}</span>
                                    <span className={`block text-[13px] ${o.e.added ? "text-chalk/55" : "text-[#4a0a24]"}`}>{o.e.added ? "added by Cue" : SPEED[o.e.speed]}</span>
                                  </span>
                                </motion.div>
                              ))}
                            </AnimatePresence>
                          </div>
                        ))
                      )}
                    </div>
                  )
                })}
              </div>
            </div>}
            </>
          )}
          {plan.ok && !plan.empty && plan.added.length > 0 && <p className="mt-3 text-sm text-chalk/50">{plan.added.join(" ")}</p>}
        </div>
      </div>
    </section>
  )
}
