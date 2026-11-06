# Cue — front end

The public site for Cue, and the base for the studio app. It is built with Vite, React 19, TypeScript, Tailwind CSS v4 and shadcn/ui (`components.json`, components in `src/components/ui`).

```bash
npm install
npm run dev      # http://localhost:5173
npm run build    # type-check + production build in dist/
```

## What is on the page

| Section | Made with |
|---|---|
| Hero | The `GlyphBackground` from 21st.dev / animate-ui is the dark field; it is made of letters, and clicking it sends a ripple. The cast is four `LiveOrb`s from 21st.dev, one per lane of the cue sheet (gaze, head, expression, hand). Their eyes follow the pointer. The start and end drawings are pinned to the table. |
| Type the middle | A live cue sheet: type an English sentence, and the plan lanes and the 16 frames update, with onion skin and frame stepping. The engine is `src/lib/cue.js`. |
| Every in-between was drawn by hand | A Blender render of a light table at night, with sheets that carry Cue's own frames (`scripts/render-lighttable.py`). |
| One sentence, four hands | The same plan drawn as graphite, sumi ink, chalk and gouache. SVG filters are applied to the line only (`src/site/sketch.tsx`). |
| Six sheets of sixteen | A flat-lay Blender render of frames 1, 4, 7, 10, 13 and 16. |
| Inbetweening, since 1833 | Archival pictures and Cohl's *Fantasmagorie* (1908), all public domain or CC0. Credits are in `public/archive/credits.json`. |
| Where the research stands | The ten-week roadmap and the dataset targets from the project README. |

Nothing on the page is model output. The frames come from the sketch engine, and the room is a render.

## Integrated 21st.dev components

- `src/components/ui/live-orb.tsx`: copied as supplied. Two broken `"\n"` escapes from the paste were fixed, and the dev check uses `import.meta.env.DEV`.
- `src/components/ui/backgrounds-glyph.tsx`: copied as supplied. `cn` comes from `@/lib/utils` (shadcn) instead of the separate `cn` npm package. Its dependencies are `motion` and `@animate-ui/react`.

Each `LiveOrb` holds a WebGL context, and browsers allow about 16. The page mounts either the desktop cast or the phone cast, never both (`src/site/use-media.ts`), and keeps the total around 12.

## Making the pictures again

```bash
# 1. the engine's frames as transparent pencil PNGs
node scripts/frames-to-svg.mjs /tmp/tex && for s in /tmp/tex/*.svg; do rsvg-convert -w 1600 -h 1000 -b none "$s" -o "${s%.svg}.png"; done
# 2. the light table, headless (OptiX on the NVIDIA GPU)
prime-run blender --background --factory-startup --python scripts/render-lighttable.py -- /tmp/tex /tmp/renders 256
# 3. optional: Nano Banana artwork (needs a Gemini key with billing; the free tier allows 0 image requests)
python3 -I scripts/generate-art.py public/art   # reads ~/.config/gemini/key
```

## Studio

The six studio screens (S1–S6) are still the v11 static mockup in `public/studio/`, linked as `/studio/app.html`. Porting them to React components is the next step.
