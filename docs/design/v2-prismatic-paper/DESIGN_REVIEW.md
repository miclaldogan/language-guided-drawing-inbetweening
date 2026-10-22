# Design Review (V2)

Reviewer stance: critical creative director. Evidence: seven rendered screens and two tiles, contrast calculations, pixel shares. Nothing here has been tested with users.

| Question | Verdict |
|---|---|
| Does the yellow feel energetic or exhausting? | In the renders it reads energetic, not harsh: the gold is amber (hue 40°) rather than lemon, is dimmer than the cream panels, and carries no text below 5.3:1. The risk is S1, S3 and S5 where gold fills 40%+ of the frame for a whole task. Unproven for long sessions. If it tires people, switch to Direction B, which changes no tokens. |
| Does the background feel paper-inspired? | Yes in cream panels; on gold the fibre layer reads slightly like linen or wood. Reduce `fiber-opacity` if that distracts. |
| Traditional and modern balanced? | Mostly. The serif and ink outlines are traditional; the layout, Manrope and flat purple buttons are modern. No ornament crept in. |
| Does the purple feel like rich ink? | Yes: `#4F0964` is the reference pixel, and flat. The S1 swash is the only painted gesture and is small. |
| Do blue and orange support it? | Orange works as a small motion accent. Blue appears only in chips and could be removed from most screens without loss; that is acceptable as it is functional. |
| Recognisable as Cue? | Wordmark, 16-tick strip, CueSheet and gold plus purple. Honest caveat: cream background plus serif headline plus warm accent is a very common current look. Gold dominance, ink print shadow, the film strip and the CueSheet are what separate it. |
| Are generated animations still the focus? | S6 yes (largest element, dark viewer). On S2 the gold shell competes with thumbnails; thumbnails use paper tints to hold up. |
| Texture subtle enough? | Yes; inputs and text blocks are flat. Not verified on real displays. |
| Six screens consistent? | Yes: same shell, stepper, panel, action row. |
| Typography distinctive but usable? | Fraunces is distinctive; use is limited to headings. Risk: webfont weight and flash; mitigated by swap and a static instance. |
| Accessible? | Calculated AA passes for all used pairs; forbidden pairs listed. No assistive-tech test yet. |
| Realistic for one developer? | Mostly. Cheap: tokens, panels, chips, buttons, cards. Moderate: CueSheet, scrubber strip. Optional and cuttable: the S1 swash, S5 film-strip sprockets (fall back to the plain 16-tick strip), texture. |
| Decorative element distracting from tasks? | The hatched pending frames on S5 and the ruled lane lines on S4 are the busiest bits; both are low contrast. The S1 swash is large relative to the form; it is on the brand side only. |
| Every screen justified by requirements? | Yes; traceability unchanged. |

## Problems found and fixed during rendering
- Film-strip sprocket holes overlapped frame numbers; geometry changed.
- Chip text clipped on the right; chip width formula corrected.
- S1 bristle lines leaked outside the swash; contained.
- All thumbnails looked identical; face turn exaggerated and hair fill varied.
- Account chevron collided with the email; layout shifted.
- Start keyframe was cropped in S3 and S6; drawing scale reduced.
- S2 had a large cream block; cards now sit directly on gold in A.
- S4 right panel had slack space; added the plain-words summary line.

## Remaining weaknesses
- Gold share is 33–43%, not 60% (V2-D1).
- Preview faces are generic stand-ins; real drawings will vary and the paper-white matte may look stark next to gold.
- CueSheet block positions imply an equal split of time; the caption says order only. If the plan schema has no speed field, remove the chevrons.
- The 10 MB limit, formats, region names and speed levels are placeholders.

## Decisions for the user
| ID | Question |
|---|---|
| V2-D1 | Accept A at about 40% gold, or push toward 60% with narrower panels and bigger margins? |
| V2-D2 | Keep the S1 painted swash, or use a plain strip? |
| V2-D3 | Keep Fraunces, or fall back to Newsreader if it feels too playful? |
| V2-D4 | Texture on gold: keep fibre, or grain only? |
| V1 items D2–D5, R1–R9 | still open (cancel, plan vocabulary, upload limits, preset plan picker) |
