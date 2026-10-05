---
name: Elecciones 29N
description: Atlas estadístico de las generales del 29 de noviembre de 2026; cada página es una lámina numerada con folio, leyenda y fuente.
colors:
  paper: "oklch(98.6% 0.003 250)"
  paper-2: "oklch(96.4% 0.005 250)"
  ink: "oklch(23% 0.03 258)"
  ink-2: "oklch(42% 0.025 258)"
  ink-3: "oklch(54% 0.02 258)"
  rule: "oklch(87% 0.01 258)"
  rule-strong: "oklch(70% 0.015 258)"
  sepia: "oklch(70% 0.11 68)"
  sepia-ink: "oklch(47% 0.1 58)"
  sepia-wash: "oklch(95% 0.03 75)"
  seq-0: "oklch(96% 0.025 78)"
  seq-1: "oklch(89% 0.055 74)"
  seq-2: "oklch(80% 0.085 70)"
  seq-3: "oklch(70% 0.105 64)"
  seq-4: "oklch(58% 0.11 56)"
  seq-5: "oklch(45% 0.095 50)"
  focus: "oklch(55% 0.16 250)"
  ok: "oklch(52% 0.11 155)"
  warn: "oklch(55% 0.14 40)"
typography:
  display:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(2.3rem, 1.4rem + 4.2vw, 4.4rem)"
    fontWeight: 800
    lineHeight: 1.02
    letterSpacing: "-0.035em"
    fontVariation: "'wdth' 82"
  headline:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(2rem, 1.3rem + 3.4vw, 3.6rem)"
    fontWeight: 800
    lineHeight: 1.12
    letterSpacing: "-0.03em"
    fontVariation: "'wdth' 88"
  title:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "clamp(1.45rem, 1.25rem + 0.9vw, 1.9rem)"
    fontWeight: 700
    lineHeight: 1.12
    letterSpacing: "-0.02em"
    fontVariation: "'wdth' 92"
  lead:
    fontFamily: "Source Serif 4, Georgia, serif"
    fontSize: "clamp(1.0625rem, 1rem + 0.35vw, 1.25rem)"
    fontWeight: 400
    lineHeight: 1.6
  body:
    fontFamily: "Source Serif 4, Georgia, serif"
    fontSize: "1.0625rem"
    fontWeight: 400
    lineHeight: 1.6
  data:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.9375rem"
    fontWeight: 600
    lineHeight: 1.2
    fontFeature: "'tnum' 1"
  figure:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "1.5rem"
    fontWeight: 750
    lineHeight: 1.1
    letterSpacing: "-0.01em"
    fontFeature: "'tnum' 1"
  label:
    fontFamily: "Archivo, ui-sans-serif, system-ui, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.06em"
rounded:
  tile: "2px"
  control: "3px"
spacing:
  s-1: "0.25rem"
  s-2: "0.5rem"
  s-3: "0.75rem"
  s-4: "1rem"
  s-5: "1.5rem"
  s-6: "2rem"
  s-7: "3rem"
  s-8: "4.5rem"
  s-9: "6.5rem"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.data}"
    rounded: "{rounded.control}"
    padding: "0.55rem 1.1rem"
    height: "2.75rem"
  button-primary-hover:
    backgroundColor: "oklch(31% 0.03 258)"
    textColor: "{colors.paper}"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    padding: "0.55rem 1.1rem"
    height: "2.75rem"
  button-ghost-hover:
    backgroundColor: "{colors.paper-2}"
  segmented-option:
    backgroundColor: "transparent"
    textColor: "{colors.ink-2}"
    padding: "0.4rem 0.8rem"
    height: "2.25rem"
  segmented-option-pressed:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
  input-percent:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    rounded: "{rounded.control}"
    width: "4.6rem"
  answer-box:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    padding: "1rem 1.5rem 1.5rem"
    width: "50rem"
  plate:
    backgroundColor: "{colors.paper}"
    textColor: "{colors.ink}"
    padding: "1rem"
  cartogram-tile:
    backgroundColor: "{colors.seq-2}"
    textColor: "{colors.ink}"
    rounded: "{rounded.tile}"
    padding: "0.18rem 0.25rem"
  folio-strip:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.paper}"
    typography: "{typography.label}"
---

# Design System: Elecciones 29N

## Overview

**Creative North Star: "La lámina numerada"**

The site is an electoral atlas printed by a statistics office. Every page is a plate: a hairline-framed box with a numbered head, a body of data, and a foot that carries the legend and the official source. Trust comes from precision and composition, not ornament. Paper white, blue-black ink, and one ochre accent taken from the real Senate ballot carry the whole identity; party colours appear only inside the data.

Density is that of a good statistical yearbook: tabular figures, thin rules, key facts in ruled grids, labels set small in Archivo. Reading prose switches to Source Serif 4 at a 40rem measure. Interaction is quiet and mechanical: a tile lifts, a seat dot re-colours, a segmented control inverts to ink.

The system rejects the newspaper election-special register: giant headline over candidate photos, front-page red, party colours used as page decoration.

**Key Characteristics:**
- Ink-framed plates (1px ink border) with head, body and source foot.
- One accent, the Senate sepia, used as a mark (current item, list markers, dates, the highlighted word), never as a surface.
- Archivo variable width: condensed (82–92% wdth) in headings, normal in UI and data.
- Tabular numerals everywhere a number appears.
- Sequential sepia ramp (six steps) for quantitative fills; party colours only in charts.
- Flat paper; depth only on hover of interactive tiles.

## Colors

A cool, near-neutral paper and blue-black ink, with a single warm ochre family that doubles as the data ramp.

### Primary
- **Senate Ballot Sepia** (sepia): the accent mark. Current-page underline in the nav, folio countdown figures, selection highlight, hover underline on index titles. Used as a line or small fill, never as body text on paper.
- **Sepia Ink** (sepia-ink): the readable form of the accent on paper. Brand wordmark suffix, the emphasised word in the home H1, list markers, dates in indexes, the answer-box legend, quiz topic.
- **Sepia Wash** (sepia-wash): the faint tint behind the next upcoming entry in the timeline, fading out by 70%.

### Neutral
- **Atlas Paper** (paper): page background and the fill of every plate, tool and answer box.
- **Margin Paper** (paper-2): secondary ground for the footer, blockquotes, majority line, bar tracks and hover states.
- **Blue-Black Ink** (ink): text, plate frames, the folio strip, primary buttons, pressed states, the 2px rules that open key-fact grids, TOC and footer.
- **Ink 2** (ink-2): deks, secondary copy, nav links at rest.
- **Ink 3** (ink-3): metadata, table heads, plate numbers, legends, crumbs.
- **Hairline** (rule): row dividers, section separators inside prose, quiz track.
- **Strong Hairline** (rule-strong): control borders (ghost button, segmented control, inputs), link underlines at rest, dashed inset frame.

### Data ramp and states
- **Sepia sequence** (seq-0 to seq-5): six-step quantitative ramp for the cartogram, light to dark. Tiles at steps 4 and 5 switch to near-white text.
- **Focus Blue** (focus): the 2px focus outline only.
- **Ok / Warn** (ok, warn): status figures in tools (warn colours the off-total sum line).

Dark mode inverts paper and ink through the same token names and reverses the ramp's lightness; components must read colours from tokens to inherit it.

### Named Rules
**The One Ochre Rule.** The only non-data hue on the page is the Senate sepia family. Any other hue must come from a party or a data scale.

**The Party Colours Stay In The Data Rule.** Party colours appear only as chart fills, seat dots and legend swatches; never as backgrounds, borders, buttons or headings.

## Typography

**Display Font:** Archivo (with ui-sans-serif, system-ui), variable width 62–125 and weight 400–800.
**Body Font:** Source Serif 4 (with Georgia), optical sizing on.
**Label/Data Font:** Archivo with tabular numerals.

**Character:** An institutional grotesque condensed for headings and set plain for every label, number and control, paired with a sturdy reading serif for the prose a voter actually reads.

### Hierarchy
- **Display** (800, clamp 2.3–4.4rem, 1.02, 82% width): the home H1 only.
- **Headline** (800, clamp 2–3.6rem, 1.12, 88% width, max 22ch): page H1 on guides, tools and provinces.
- **Title** (700, clamp 1.45–1.9rem, 92% width): prose H2 and FAQ heading; index section H2 runs slightly larger (to 2.2rem, 88% width).
- **Lead** (Source Serif 4, clamp 1.0625–1.25rem): the dek under H1 and the answer-box first paragraph (to 1.3rem, 1.5 line-height).
- **Body** (Source Serif 4, 1.0625rem, 1.6): prose at a 40rem measure.
- **Data** (Archivo 600, 0.875–0.9375rem, tabular): tables, bars, seat lists, controls, buttons.
- **Figure** (Archivo 750, 1.5rem, tabular): key-fact values in province stat rows; home key facts use 700 at 1.15rem.
- **Label** (Archivo 700, 0.75rem, 0.06em, uppercase): table heads, key-fact terms, rail and footer group titles, the answer-box legend.

### Named Rules
**The Tabular Rule.** Every number (seats, percentages, dates, countdowns, votes) is set in Archivo with tabular figures.

**The Condensed Headings Rule.** Width narrows as size grows: 92% at title, 88% at headline, 82% at display. UI and data stay at normal width.

## Layout

Content sits in a 74rem wrap with 1rem gutters. Reading columns hold a 40rem measure; answer boxes and stat rows cap at 50rem. On wide screens (64rem and up) guide pages split into content plus a 17rem sticky rail (TOC and ad slot); the home hero splits 0.9fr / 1.1fr with the cartogram plate on the right. Tools split 0.85fr / 1.15fr from 56rem; below that the result panel (hemicycle and seat list) moves above the controls and sticks under the masthead.

Spacing follows a nine-step scale from 0.25rem to 6.5rem; sections breathe at 3rem, layout gaps at 3–4.5rem, inside plates 1rem. The masthead is sticky with a 1px ink bottom rule; above it, a dark folio strip carries the date and countdown. Navigation collapses to a two-column drawer below 62rem.

## Elevation & Depth

Flat paper. Hierarchy comes from rules of different weight: 1px hairline between rows, 1px ink around plates and tools, 2px ink opening a block (key facts, TOC, FAQ, footer). Tonal layering with Margin Paper marks secondary ground.

### Shadow Vocabulary
- **Tile lift** (`box-shadow: 0 6px 16px -6px oklch(20% 0.03 258 / 0.45)`): only on hover or focus of a cartogram tile, together with a 1.08 scale.

### Named Rules
**The Ruled, Not Raised Rule.** Containers are separated by rules and paper tone. Shadows exist only as a response to pointer or focus on a data tile.

## Shapes

Near-square. Controls carry a 3px corner; cartogram tiles 2px; seat-list swatches are circles; plates, tools, answer boxes and sections are square-cornered. Insets (Ceuta, Melilla, islands) sit in a dashed strong-hairline frame. The current nav item drops its corner and uses an inset 2px sepia underline.

## Components

### Buttons
- **Shape:** gently squared (3px), minimum 2.75rem tall.
- **Primary:** ink fill, paper text, Archivo 650 at 0.9375rem, 0.55rem 1.1rem padding.
- **Hover / Active:** fill lightens by 0.08 L; press scales to 0.97 on the ease-out curve (cubic-bezier(0.16, 1, 0.3, 1)) over 120ms. Disabled at 45% opacity.
- **Ghost:** transparent with a strong-hairline border; hover fills with Margin Paper.

### Segmented control and answer scale
- **Style:** options inside one strong-hairline frame (3px); ink-2 text at rest.
- **State:** the pressed option inverts to ink fill and paper text. Quiz answer buttons follow the same inversion, border to ink on hover.

### Inputs / Fields
- **Style:** percentage field framed in strong hairline (3px) on paper, right-aligned tabular 600 figure with a muted % suffix; range sliders take ink as accent colour.
- **Focus:** the global 2px Focus Blue outline, 2px offset.

### Navigation
- **Style:** Archivo 0.9375rem in ink-2; hover darkens to ink on Margin Paper; current page is ink with an inset 2px sepia underline. Mobile: a bordered "menu" button opens a two-column drawer of ruled links.

### Answer box
A 1px ink-framed box whose legend ("Respuesta rápida") sits on the top border like a fieldset legend, uppercase label type in Sepia Ink. The first paragraph is set in lead size; following paragraphs drop to 1rem ink-2. It appears directly under the page head on every guide and province.

### Plate (lámina)
1px ink frame on paper. Head: title (Archivo 700) left, plate number or count (ink-3, tabular) right, ink rule below. Body padded 1rem. Foot: legend and source in 0.75rem ink-3 above a hairline. Hosts the cartogram, hemicycle and results bars.

### Tile cartogram
A 10-column grid of square tiles, 3px gaps, each tile a link carrying the provincial licence-plate code (top left, 600) and the seat count (bottom right, 750 tabular), filled from the sepia sequence. Hover or focus lifts the tile (see Elevation).

### Hemicycle and seat list
A 350-dot SVG hemicycle whose fills transition over 350ms as the simulation recalculates; beside it a ruled seat list with circular party swatches, tabular counts and deltas, and a majority line on Margin Paper.

### Key-fact grid
A definition list opened by a 2px ink rule, cells divided by hairlines; uppercase label terms over bold tabular values.

## Do's and Don'ts

### Do:
- **Do** put every chart, map and tool inside a plate with a numbered head and a source foot.
- **Do** set every number in Archivo with tabular figures.
- **Do** use Sepia Ink (sepia-ink) for accent text on paper and keep Senate Ballot Sepia (sepia) for lines, small fills and the dark folio strip.
- **Do** separate blocks with rules: 1px hairline between rows, 1px ink around containers, 2px ink to open a group.
- **Do** read every colour from tokens so dark mode carries through.

### Don't:
- **Don't** use party colours outside the data (backgrounds, buttons, borders, headings).
- **Don't** introduce a second accent hue; the sepia family and the data scales are the full palette.
- **Don't** raise containers with shadows; the tile lift on hover is the only shadow.
- **Don't** round containers; plates, tools, answer boxes and sections stay square, controls stop at 3px.
- **Don't** build the newspaper election special: giant headline over candidate photos or front-page red.
