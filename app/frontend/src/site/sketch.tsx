import { useEffect, useMemo, useRef, useState } from "react"
import { Cue, type Plan, type Pose } from "@/lib/cue"

/** The four hands a frame can be drawn in. Each is a stroke/paper pair plus an SVG filter. */
export type Hand = "pencil" | "ink" | "chalk" | "gouache"

const HANDS: Record<Hand, { stroke: string; paper: string; ground: string; width: number; filter: string }> = {
  pencil: { stroke: "#2a2430", paper: "#f3eee6", ground: "#f3eee6", width: 2.1, filter: "url(#cue-pencil)" },
  ink: { stroke: "#0d0a0f", paper: "#efe7d8", ground: "#efe7d8", width: 4.4, filter: "url(#cue-ink)" },
  chalk: { stroke: "#f6f0f8", paper: "#2a0d22", ground: "#2a0d22", width: 3.2, filter: "url(#cue-chalk)" },
  gouache: { stroke: "#1a0a14", paper: "#ffd7e6", ground: "#ff4f8b", width: 3.6, filter: "url(#cue-gouache)" },
}

/** Shared SVG filters. Mount once near the root. */
export function SketchFilters() {
  return (
    <svg width="0" height="0" aria-hidden className="absolute">
      <defs>
        {/* graphite: a slight hand wobble and a grainy line */}
        <filter id="cue-pencil" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3" result="w" />
          <feDisplacementMap in="SourceGraphic" in2="w" scale="2.2" result="d" />
          <feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="1" seed="8" result="g" />
          <feColorMatrix in="g" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -1.4 1.35" result="ga" />
          <feComposite in="d" in2="ga" operator="in" result="grainy" />
          <feMerge><feMergeNode in="grainy" /><feMergeNode in="grainy" /></feMerge>
        </filter>
        {/* sumi ink: a heavy brush that swells and bleeds a little */}
        <filter id="cue-ink" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="3" seed="11" result="w" />
          <feDisplacementMap in="SourceGraphic" in2="w" scale="4.5" result="d" />
          <feMorphology in="d" operator="dilate" radius="0.4" result="m" />
          <feGaussianBlur in="m" stdDeviation="0.35" />
        </filter>
        {/* chalk on a dark board: broken, dusty strokes */}
        <filter id="cue-chalk" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.04" numOctaves="2" seed="5" result="w" />
          <feDisplacementMap in="SourceGraphic" in2="w" scale="2.6" result="d" />
          <feTurbulence type="fractalNoise" baseFrequency="1.6" numOctaves="1" seed="2" result="n" />
          <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 -2.2 1.7" result="na" />
          <feComposite in="d" in2="na" operator="in" />
        </filter>
        {/* gouache: soft, flat and slightly misregistered */}
        <filter id="cue-gouache" x="-5%" y="-5%" width="110%" height="110%">
          <feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="2" seed="9" result="w" />
          <feDisplacementMap in="SourceGraphic" in2="w" scale="3" />
        </filter>
      </defs>
    </svg>
  )
}

export function drawPose(p: Pose, hand: Hand = "pencil", onion?: Pose | null) {
  const h = HANDS[hand]
  let svg = Cue.drawFigure(p, { stroke: h.stroke, paper: h.paper, width: h.width, onion, onionColor: "#ff4f8b" })
  // the frame's ground can differ from the fill inside the face (gouache)
  const rect = `<rect width="320" height="200" fill="${h.paper}"/>`
  svg = svg.replace(rect, `<rect width="320" height="200" fill="${h.ground}"/><g filter="${h.filter}">`).replace(/<\/svg>$/, "</g></svg>")
  return svg
}

/** A single frame, drawn in one hand. */
export function Sketch({ pose, hand = "pencil", onion, className, label }: { pose: Pose; hand?: Hand; onion?: Pose | null; className?: string; label?: string }) {
  const html = useMemo(() => drawPose(pose, hand, onion), [pose, hand, onion])
  return (
    <div
      role="img"
      aria-label={label ?? "Drawing"}
      className={className}
      // the engine returns a trusted SVG string built from numbers only
      dangerouslySetInnerHTML={{ __html: html.replace("<svg ", '<svg width="100%" height="100%" preserveAspectRatio="xMidYMid slice" ') }}
    />
  )
}

/** Plays a plan's sixteen frames at 12 fps on twos while `playing` is true. */
export function useFrames(plan: Plan, playing: boolean, holdEnds = 4) {
  const frames = useMemo(() => Cue.framesFromPlan(plan), [plan])
  const [i, setI] = useState(0)
  const hold = useRef(0)
  useEffect(() => {
    if (!playing) return
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches
    if (reduce) return
    const t = setInterval(() => {
      setI((cur) => {
        if ((cur === 15 || cur === 0) && hold.current < holdEnds) {
          hold.current++
          return cur
        }
        hold.current = 0
        return (cur + 1) % 16
      })
    }, 167)
    return () => clearInterval(t)
  }, [playing, holdEnds])
  return { frames, i, setI }
}
