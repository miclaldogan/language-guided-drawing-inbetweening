import { Cue } from "../src/lib/cue.js";
import fs from "node:fs";
const out = process.argv[2];
const plan = Cue.parseInstruction(Cue.EXAMPLES[2]);
const f = Cue.framesFromPlan(plan);
// graphite on transparent so Blender can composite it onto paper
for (const i of [0, 3, 6, 9, 12, 15]) {
  let svg = Cue.drawFigure(f[i], { stroke: "#2a2430", paper: "none", width: 2.2 });
  svg = svg.replace('<rect width="320" height="200" fill="none"/>', "");
  fs.writeFileSync(`${out}/f${String(i + 1).padStart(2, "0")}.svg`, svg);
}
console.log("ok");
