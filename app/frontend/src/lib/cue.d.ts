export type Pose = { gaze: number; head: number; smile: number; hand: number }
export type Region = "gaze" | "head" | "smile" | "hand"
export type CueEvent = { region: Region; action: string; speed: "slow" | "normal" | "fast"; added?: boolean }
export type Plan =
  | { ok: true; empty?: boolean; steps: { events: CueEvent[] }[]; added: string[] }
  | { ok: false; reason: string; suggestion: string }
export type DrawOptions = { stroke?: string; paper?: string; width?: number; onion?: Pose | null; onionColor?: string; label?: string }
export declare const Cue: {
  FRAME_COUNT: number
  START: Pose
  END: Pose
  REGIONS: { id: Region; label: string }[]
  EXAMPLES: string[]
  drawFigure(p: Pose, opts?: DrawOptions): string
  parseInstruction(text: string): Plan
  framesFromPlan(plan: Plan): Pose[]
}
export default Cue
