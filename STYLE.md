# House style: "cut paper v9" (the current definition of good)

Reference scene: `scenes/founder-v9.svg`. Git tag: `save-v9-good`.

## Look
- **Medium.** Digital cut paper. Every shape is a flat, filled paper piece, with no outlines. Torn rough edges, a small navy shadow under each shape, and paper grain with fibers on everything.
- **Palette.** Brand colors for the set: a sky-blue wall (#8CBDDC), two darker blue floor strips, navy (#182A46) for hair and pants, cream (#F6EEDC), orange (#ED7239 / #FF5600), red (#DE4A30), skin #FAC496. Clothes can use colors outside the palette so that the characters look different from each other.
- **Background.** A paper wall with visible fibers, a torn paper floor, and nothing else.

## Characters
- **Proportions.** Big round heads, about half of the body height. A front view with a slight lean.
- **Faces.** Made of paper shapes. Cream eye whites with navy pupils, bar eyebrows, a small oval nose. A skeptic has heavy lids and one raised eyebrow. A grin is a red mouth with cream teeth (a big navy mouth reads as a beard).
- **Bodies.** A rounded torso with a clear shoulder line. Thick limbs with round ends. Arms bend at the elbow and start at the shoulder corner. Hands are skin circles with a thumb, and a hand grips the edge of an object.
- **Wardrobe.** Modern casual: hoodies, jeans, white sneakers. No suits.

## Motion
- 24 fps, shot on twos. 4.5 seconds. A slow 4% camera push.
- The edges boil every 2 frames (3 edge versions). The background boils at half strength, with a 1px jitter and a slight light flicker.
- Moving parts swing on pivots: "snap" (jerky, opens and holds) or "sine" (smooth). Typical: an arm pumps, a head bobs, an eyebrow rises, a foot taps.

## Composition
- Square, 1080x1080. The scene is at 60% scale and centered. The floor line is at about 70% of the height.
- A full-frame cutaway. No text, arrows, circles, or labels.

## Prompt template
> Cut-paper v9 scene: **[who]** **[doing what]** **[where, if it matters]**.
> Moving parts: **[part]: [motion]**, ...
> Feeling: **[one word]**.

Example:
> Cut-paper v9 scene: a founder in a hoodie sits alone at a laptop at 2am, with a coffee mug.
> Moving parts: head nods off and snaps up; hand taps the mouse.
> Feeling: exhausted.

---

# Alternate saved style: "Malevich-lite" (no boil)

Reference scenes: `scenes/malevich-lite-pitch.svg` (video) and `scenes/malevich-lite-cafe.svg` (still). Git tag: `save-malevich-lite`.

- **Look.** Geometric bodies (trapezoid torsos, rectangular limbs) with soft gradients from a light tint to full color on every form, in the manner of Malevich's "Haymaking," toned down for LinkedIn. One skin tone with soft shading, simple calm faces, navy jeans, white sneakers. A plain room: a cream wall, one window, a navy floor. Brand palette plus character colors. A light painted grain over the whole frame.
- **Motion.** Smooth, 24 fps, with no boil, no jitter, and no paper shadows (root: `data-step="1" data-jitter="0" data-shadow="0"`, no `data-finish`). Slow sine swings: an arm pushes, a head nods, a head tilts.
- **Prompt.** "Malevich-lite scene: [who] [doing what] [where]. Moving parts: ... Feeling: ..."
