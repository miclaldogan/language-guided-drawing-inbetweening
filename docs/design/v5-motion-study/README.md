# Cue — Motion Study (V5)

An independent visual prototype for the Cue web studio. This direction starts from the product flows and the verified database/job lifecycle; it does not reuse the V1–V4 paper/atelier styling.

The parent [`docs/design/README.md`](../README.md) marks this as the active visual direction and links the product flow references.

## Open it

Open `index.html` directly in a modern browser, or serve this folder locally:

```bash
python -m http.server 8000 --directory docs/design/v5-motion-study
```

Then visit `http://localhost:8000`.

## What is in the prototype

- Six linked product screens: sign in, library, keyframes, motion plan, generation status, and result.
- A real-time GLSL engraving study with sliders for line pitch, relief, motion, and pointer influence.
- A raymarched 3D form rendered on the GPU, with a static SVG fallback when WebGL is unavailable.
- Simulated navigation, keyframe swap, instruction examples, approval invalidation, job cancellation, frame stepping, playback, and download affordance.
- Responsive layouts and `prefers-reduced-motion` handling.

The application data is illustrative. No API, authentication, upload, model inference, or MP4 is connected. File limits and inference metadata are intentionally omitted until the project's open decisions are resolved.

## Visual direction

**Movement as ink.** A quiet, pale mineral interface frames near-black drawing stages; signal orange marks the action that moves the work forward, while electric blue marks system activity. The hero is an abstract folded volume whose contour lines change with light, time, and pointer position. This keeps the expressive graphics attached to the product's core idea: transforming two drawings into an ordered sequence.

## Interaction map

`Welcome → Library → Keyframes → Motion plan → Generation → Result`

The top navigation and keyboard-accessible screen switcher also let reviewers jump between screens. The “Field study” button opens the shader parameter panel.

## Known design questions

- Whether the user-facing interface should be English or Turkish is not settled by the submitted requirements. This prototype keeps the English product copy used in the previous requirements-to-UI mapping.
- The motion-plan vocabulary, upload rules, maximum file size, output frame rate, account/session copy, and model metadata display depend on decisions recorded in `docs/architecture/database-and-diagrams-v2/reports/07_OPEN_APPROVALS.md`.
- The hero canvas is a visual study, not an effect applied to uploaded artwork or generated output.
