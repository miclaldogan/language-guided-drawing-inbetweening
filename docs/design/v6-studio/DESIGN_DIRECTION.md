# Cue Studio — V6 design direction

## Intent

Make the drawing-to-animation workflow feel like a considered creative instrument: quiet enough for careful image review, distinctive enough to feel authored, and direct enough that a first-time user can complete the sequence without learning a new metaphor.

## Visual system

- **Surface:** mineral white and warm gray, with a graphite navigation rail and dark art stage only where image contrast benefits from it.
- **Accent:** oxide red is reserved for the next action, selected frame, or a tiny mark in the engraving study.
- **Typography:** editorial serif for major screen titles; neutral sans-serif for instructions; monospaced metadata for frame IDs, status, dimensions, and technical labels.
- **Geometry:** square image stages, fine rules, compact status marks, and deliberately limited corner rounding.
- **Density:** broad drawing stages and clear whitespace; compact metadata sits at the edge of the content rather than becoming dashboard cards.

## Reference translation

| Reference | Borrow | Keep out of Cue |
|---|---|---|
| [Pixelismo / AVAU](https://www.pixelismo.it/avau.html) | One coherent atmosphere, controlled color/material shifts, transitions that reveal a state | Fragrance-store navigation and six unrelated 3D scenes |
| [Director's Lookbook Wave-Line](https://directorslookbook.app/tools/wave-line/) | Per-pixel tone mapping into weighted, horizontally flowing lines; tune line spacing and motion independently | Applying the effect to a user's source or result image, where it would distort evaluation |
| [Codrops sketch effect](https://tympanus.net/codrops/2022/11/29/sketchy-pencil-effect-with-three-js-post-processing/) | A future route for rendering true scene contours from normal/depth buffers | Adding a 3D rendering pipeline before the core product calls for one |
| [Awwwards](https://www.awwwards.com/) | Typographic hierarchy and visual confidence | Treating an award-winning landing-page interaction as a product workflow |
| [Mesh3D](https://www.mesh3d.gallery/) / [Shadertoy](https://www.shadertoy.com/) | Technical studies and interaction references for the isolated shader lab | A permanent always-on WebGL canvas on every screen |

## Screen sequence

1. **Sign in:** identity and a restrained etching study; one clear entry point.
2. **Library:** editorial archive of actual animation jobs and their real states.
3. **Keyframes:** two equal 8:5 image stages with a clear A → B reading.
4. **Motion plan:** English instruction beside the interpreted cue sequence; approval is visible and explicit.
5. **Generation:** source drawings and a 16-tick activity strip; no invented percentage or ETA.
6. **Result:** largest available area for the generated clip, frame stepping, and reproducibility details.
7. **Wave-Line lab:** isolated, adjustable shader study that is visually distinct from the product workflow.

## Boundaries and open facts

- Real account, file, model, and media services are not connected in this mockup.
- Upload size and exact image constraints remain unstated until the project decides them.
- The interface copy is Turkish; the motion instruction remains English to match the current project requirement.
- The sample result is illustrative and does not claim a specific model version, seed, FPS, or measured generation duration.
- WebGL effects are optional decoration. HTML owns all product meaning and navigation; reduced-motion users get a still composition.

## Next design pass

Review this direction at desktop and mobile sizes. If it reads as a professional drawing workspace, refine individual states (empty, uploading, unsupported instruction, queued, failed, and result loading) before connecting any production frontend or choosing a rendering framework.
