# Visual-technique references

- [Engraving Trace — shader.gallery](https://shader.gallery/engraving/) — GLSL ES fragment shader example with adjustable line pitch, wrap, relief, ink and slow breathing; MIT-labeled source. Used as technique reference, not copied into the prototype.
- [Sketchy Pencil Effect with Three.js Post-Processing — Codrops](https://tympanus.net/codrops/2022/11/29/sketchy-pencil-effect-with-three-js-post-processing/) — working example of post-processing with a diffuse image, normal buffer, Sobel edge detection and noise. This is a heavier NPR path for testing against actual generated frames later.
- [Bruno Simon folio-2025 source — GitHub](https://github.com/brunosimon/folio-2025) — example of an elaborate Three.js/WebGPU scene, assets and interactions. It is a portfolio and useful implementation study, not a product UI to copy.

## What was taken into this visual prototype

The prototype uses an original signed-distance form and line field: light changes hatch density, the pointer bends the contours locally, and motion changes the relief slowly. This tests the graphic behavior without adding a Three.js, React Three Fiber or GSAP dependency to the mockup package. The 3D portfolio source is retained as a reference for a later real-asset scene; its mechanics are beyond what a screen mockup needs.

For an app workflow, the critical handoff remains semantic HTML and actual controls. The WebGL scene is a local, lazy visual study with static fallback; it is not the place where account actions, prompt meaning, status, or result controls live.
