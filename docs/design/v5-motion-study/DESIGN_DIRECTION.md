# Cue V5 — Movement as Ink

## Product reading

Cue is a private, authenticated web studio for turning two user drawings into an ordered, short animation. The central product question is not “what can this model do?” but “what movement did the user ask for, what did the system understand, and what frames came back?” The interface makes those three things visible in order.

The visual motif is a moving contour field: light and movement translated into engraved lines. It is generated in the browser in one small, isolated WebGL scene and can be tuned through a field-study drawer. The same motif is reduced to static line illustrations on the workflow screens. User drawings and generated frames remain the main content; the shader is never applied to those images and never carries product information.

## Direction

- **Mineral surface:** flat pale gray-green surfaces, without paper grain, beige sheets, or heavy texture.
- **Ink stage:** near-black framing around drawings and the shader study. Uploads are shown on a neutral, high-value surface so line art remains legible.
- **Signal colors:** persimmon orange marks the next action. Mint/blue indicate interpretation and work in progress. Color never carries a status alone.
- **Graphic language:** careful ruled lines, frame ticks, pin marks A/B, and custom line drawings. They refer to timing and endpoints instead of adding unrelated decoration.
- **Typography:** compact technical labels, expressive but restrained display headlines, readable body copy.
- **Interaction:** the interface moves only to explain a change. The hero relief responds to a nearby pointer; it is paused when hidden, quality-capped for smaller screens, and replaced by a static vector if WebGL is unavailable.

## Requirement-to-screen mapping

| Product concern | Screen treatment | Source of truth |
|---|---|---|
| Private account, sign-in and sign-out | Welcome/auth entry and persistent account affordance | FR-01, `act-01-authentication`, `sd-01-authentication` |
| Own jobs, ordered newest first; five states; delete only terminal jobs | Gallery of studies with state labels and poster art | FR-02, FR-09, `sd-05-status-and-result`, `sd-06-cancel-failure-delete` |
| Two distinct drawings, independently replaceable | Side-by-side A/B stages with a directional bridge | FR-03, `sd-02-keyframe-upload`, composite owner foreign keys in the physical ERD |
| Optional English instruction; plan preview is transient | Instruction field and numbered cue sequence; blank instruction skips plan interpretation | FR-04, FR-05, `sd-03-plan-preview`, `act-02-animation-creation` |
| Plan approval is required only when a plan exists; editing invalidates approval | Explicit approval checkbox and “out of date” state | FR-05, `animation_job` plan/approval constraints, `sd-03-plan-preview` |
| Generation is asynchronous; no progress percentage or ETA is invented | Running state, elapsed time, activity-only frame strip, cancel action | FR-06, FR-07, `sm-01-job-state-machine`, `sd-04a`, `sd-04b`, `sd-06` |
| Done jobs store MP4 and one archive of 2–16 PNG frames | Frame-step player/scrubber, MP4 download action, archive metadata | FR-08, D-09, `sd-05-status-and-result`, `media_asset` and `animation_job` schema |
| Reproducibility metadata belongs to the job | Record panel has slots for model, seed, duration and created time; unknown model metadata stays unknown | FR-10, `model_version`, `animation_job`, `sd-05-status-and-result` |
| Research scripts are not user-facing | No training or evaluation controls in the studio | FR-11, FR-12 and `ai-01-pipeline` |

## Visual-technique placement

| Technique | Use in the mockup | Product boundary |
|---|---|---|
| Procedural GLSL engraving | Interactive hero relief and parameter study | Decorative exploration only; not the generated drawing style |
| 3D form and light | Signed-distance volume raymarched in the fragment shader | Avoids a model download for the concept; a real asset pipeline is a later choice |
| Pointer response | Bends the relief field around the cursor | Disabled under reduced motion; no pointer-only control is required to navigate |
| Scroll-linked cinematic movement | Not used in the authenticated workflow | The main task has discrete steps; scroll theatrics would compete with upload, plan review and the result |
| Non-photorealistic rendering | Static line-art studies and shader-based cross-hatching exploration | A full normal/depth post-process belongs only if actual product imagery benefits from it |

## Implementation notes and limits

The prototype is plain HTML, CSS, JavaScript and WebGL so it can be reviewed without selecting a frontend build chain. It uses no React, Three.js, React Three Fiber or GSAP package yet. The current experiment proves the desired visual behavior and screen relationships; it is not the production frontend architecture. The renderer caps pixel ratio, stops when off-screen or when the page is hidden, follows `prefers-reduced-motion`, and has a static fallback.

No shader has been applied to uploaded or generated frames. The design does not rely on the hero for page text, navigation, accessibility, or product comprehension. A real implementation can keep content in React/HTML and load an isolated WebGL stage only when visible and supported.

## Open decisions inherited from the project

1. UI locale and translated copy.
2. PNG/JPEG limits, dimensions and upload size.
3. Plan vocabulary/JSON schema and when simultaneous cues are valid.
4. Output FPS and exact duration display.
5. Whether all recorded inference parameters are user-visible.
6. Account/session policy and error copy.

The defaults are listed in `docs/architecture/database-and-diagrams-v2/reports/07_OPEN_APPROVALS.md`; the mockup does not silently settle them.
