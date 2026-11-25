---
name: Ular Tangga Kuis
description: Snakes and ladders as a pasar malam game stall, painted on a terpal-blue tent, where a correct answer opens the dice.
colors:
  terpal: "#1C4A98"
  terpal-gelap: "#12326C"
  terpal-terang: "#285AAC"
  terpal-jahit: "#5C88CE"
  krem: "#F7F1E2"
  krem-gelap: "#DED2B8"
  kuning-pucat: "#FCE29E"
  kuning-cat: "#FFCC48"
  kuning-tua: "#C49214"
  merah-cat: "#CC2434"
  merah-tua: "#821220"
  hijau-cat: "#18844E"
  hijau-tua: "#0C5430"
  tinta: "#1A1E2E"
  tinta-lembut: "#54505C"
  bohlam-nyala: "#FFDE82"
  bohlam-inti: "#FFF8DC"
  bohlam-mati: "#5C4628"
  oren-jalur: "#FF841C"
  kayu: "#BA783C"
  kayu-gelap: "#603818"
  ular-badan: "#8E3496"
  ular-tua: "#46144E"
  ular-garis: "#FFCE54"
  pemain-merah: "#D62838"
  pemain-biru: "#2466DC"
  pemain-hijau: "#169654"
  pemain-kuning: "#F0B210"
  tombol-mati: "#283C68"
  garis-kolom: "#968C78"
  bayangan: "#060E24"
  letterbox: "#081022"
typography:
  display:
    fontFamily: "Bungee"
    fontSize: "68px"
    fontWeight: 400
    letterSpacing: "0em"
  headline:
    fontFamily: "Bungee"
    fontSize: "40px"
    fontWeight: 400
  title:
    fontFamily: "Bungee"
    fontSize: "28px"
    fontWeight: 400
  numeral:
    fontFamily: "Bungee"
    fontSize: "26px"
    fontWeight: 400
  button:
    fontFamily: "Bungee"
    fontSize: "22px"
    fontWeight: 400
  label:
    fontFamily: "Bungee"
    fontSize: "18px"
    fontWeight: 400
  question:
    fontFamily: "Atkinson Hyperlegible"
    fontSize: "24px"
    fontWeight: 700
  body:
    fontFamily: "Atkinson Hyperlegible"
    fontSize: "20px"
    fontWeight: 400
    lineHeight: "26px"
  body-strong:
    fontFamily: "Atkinson Hyperlegible"
    fontSize: "20px"
    fontWeight: 700
  small:
    fontFamily: "Atkinson Hyperlegible"
    fontSize: "18px"
    fontWeight: 400
  small-strong:
    fontFamily: "Atkinson Hyperlegible"
    fontSize: "18px"
    fontWeight: 700
rounded:
  chip: "4px"
  tag: "6px"
  field: "8px"
  answer: "9px"
  button: "10px"
  panel: "12px"
  frame: "14px"
  sign: "16px"
spacing:
  cell-gap: "8px"
  panel-gap: "10px"
  inset: "14px"
  inset-wide: "18px"
  edge: "24px"
  tile: "78px"
  board: "624px"
  board-frame: "18px"
  column-right: "560px"
components:
  button-primary:
    backgroundColor: "{colors.kuning-cat}"
    textColor: "{colors.tinta}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    height: "56px"
  button-secondary:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    height: "56px"
  button-danger:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
    height: "56px"
  button-disabled:
    backgroundColor: "{colors.tombol-mati}"
    textColor: "{colors.krem-gelap}"
    typography: "{typography.button}"
    rounded: "{rounded.button}"
  toggle-selected:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    height: "44px"
  toggle-unselected:
    backgroundColor: "{colors.krem-gelap}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    rounded: "{rounded.button}"
    height: "44px"
  answer-option:
    backgroundColor: "{colors.kuning-cat}"
    textColor: "{colors.tinta}"
    typography: "{typography.small-strong}"
    rounded: "{rounded.answer}"
    height: "46px"
  answer-option-correct:
    backgroundColor: "{colors.hijau-cat}"
    textColor: "{colors.krem}"
  answer-option-wrong:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
  answer-option-spent:
    backgroundColor: "{colors.krem-gelap}"
    textColor: "{colors.tinta-lembut}"
  answer-option-locked:
    backgroundColor: "{colors.kuning-pucat}"
    textColor: "{colors.tinta-lembut}"
  text-field:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.body-strong}"
    rounded: "{rounded.field}"
    height: "42px"
    width: "320px"
  text-field-readonly:
    backgroundColor: "{colors.krem-gelap}"
    textColor: "{colors.tinta}"
  panel-question:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.question}"
    rounded: "{rounded.panel}"
    padding: "18px"
    width: "{spacing.column-right}"
  panel-question-header:
    backgroundColor: "{colors.kuning-cat}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    height: "44px"
  panel-score:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    rounded: "{rounded.panel}"
    padding: "12px"
  score-row-active:
    backgroundColor: "{colors.kuning-cat}"
    textColor: "{colors.tinta}"
    typography: "{typography.small-strong}"
    rounded: "{rounded.field}"
    height: "48px"
  score-row-idle:
    backgroundColor: "{colors.krem-gelap}"
    textColor: "{colors.tinta-lembut}"
    typography: "{typography.small-strong}"
    rounded: "{rounded.field}"
    height: "48px"
  sound-pill:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    size: "150px 24px"
  karcis-log:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta-lembut}"
    typography: "{typography.small}"
    rounded: "{rounded.tag}"
  dialog-confirm:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    rounded: "{rounded.frame}"
    size: "400px 214px"
  tile-a:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    size: "{spacing.tile}"
  tile-b:
    backgroundColor: "{colors.kuning-pucat}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    size: "{spacing.tile}"
  tile-finish:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    size: "{spacing.tile}"
  marker-ladder:
    backgroundColor: "{colors.hijau-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    size: "49px 24px"
  marker-snake:
    backgroundColor: "{colors.ular-badan}"
    textColor: "{colors.krem}"
    typography: "{typography.label}"
    rounded: "{rounded.tag}"
    size: "49px 24px"
  board-frame:
    backgroundColor: "{colors.merah-cat}"
    rounded: "{rounded.frame}"
    padding: "{spacing.board-frame}"
  stall-sign:
    backgroundColor: "{colors.merah-cat}"
    textColor: "{colors.krem}"
    typography: "{typography.display}"
    rounded: "{rounded.sign}"
  stall-plaque:
    backgroundColor: "{colors.kuning-cat}"
    textColor: "{colors.tinta}"
    typography: "{typography.headline}"
    rounded: "{rounded.button}"
    size: "240px 66px"
  die:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    size: "52px"
  token:
    backgroundColor: "{colors.krem}"
    textColor: "{colors.tinta}"
    typography: "{typography.label}"
    size: "30px"
---

# Design System: Ular Tangga Kuis

## Overview

**Creative North Star: "Stan Pasar Malam"**

The whole game is a night-market game stall. The ground is a deep terpal-blue tent with stitched seams and soft folds; everything the player touches sits on top of it as a plywood board painted in flat sign-painter colours (red, yellow, cream, green) with a darker hand-painted rim and a thin gloss line along the top. Light is the stall's currency: strings of bulbs hang across the tent and frame the board, and heat is rationed. Most bulbs idle dim; the active player's tile, the route ahead of a moving token, and the winner's moment burn full.

The board is a lit stall table of 64 painted tiles (8x8), the question is a cream card at the ticket booth, the dice are thrown on the counter, the game log is a stack of paper karcis with a perforated stub and serial numbers. Snakes and ladders are painted props, drawn from primitives rather than imported art: a tapering purple snake with yellow bands and a forked red tongue, a wooden ladder with dark-edged rungs. Three difficulty levels (Mudah, Sedang, Sulit) change how many props stand on the table, never how they are painted. Signs speak in Bungee, a chunky sign-painter display face; questions, answers and data speak in Atkinson Hyperlegible so a student reads them at a glance.

The canvas is a fixed 1280x720 stage, scaled whole to the window. Density is moderate and game-like: one board on the left, one stacked column of painted planks on the right. The world refuses the cartoon jungle board and the dark neon gamer HUD.

**Key Characteristics:**
- Terpal-blue tent ground, never a flat fill: alternating 214px panels, central fold shading, dashed seam stitches, a darkened ground band at the bottom.
- Every surface is a painted plank: flat fill, 3px darker rim, 3px gloss strip, soft blurred drop shadow.
- Bulbs as the light and state system, with lit, idle and dead states.
- Bungee for signs, labels and numerals; Atkinson Hyperlegible for anything to be read.
- Players are a colour plus a number, always together.
- Motion is physical and eased: cards slide in, dice tumble, tokens hop, bulbs warm and cool.
- Difficulty changes the count of props and the bot's accuracy; the paint, sizes and layout stay the same.

## Colors

A sign-painter's tin set on a tent: one deep blue ground, warm cream and yellow boards, a single stall red, and the bulb ambers that carry state.

### Primary
- **Stall Red** (merah-cat): the stall's own colour. Board frame, the name sign, the scoreboard plank, the danger and "roll" call to action (KOCOK DADU, YA, KELUAR), every selected setup toggle, the finish tile, rule numerals, error messages, the wrong-answer status line and the low timer disc.
- **Sign Yellow** (kuning-cat): the primary button paint (MULAI, MULAI MAIN, KEMBALI on how-to-play, MAIN LAGI), the question card header, the active scoreboard row, live answer options and the winner's ranking row.

### Secondary
- **Ladder Green** (hijau-cat): correct. The correct answer option, the floating +10/+5 score pop, and ladder destination markers.
- **Deep Green** (hijau-tua): the "BENAR!" status line on the cream question card, where Ladder Green would read too light as text.
- **Snake Purple** (ular-badan) with **Snake Shadow** (ular-tua) outline and **Snake Band** (ular-garis) stripes: reserved for snakes and the snake destination markers.
- **Plywood** (kayu) and **Plywood Edge** (kayu-gelap): ladder rails and rungs only.

### Tertiary (light)
- **Lit Bulb** (bohlam-nyala), **Bulb Core** (bohlam-inti), **Dead Bulb** (bohlam-mati): one bulb interpolates from dead to lit by a 0 to 1 heat value; the core highlight appears above 0.3 heat. Lit Bulb also tints the route highlight wash.
- **Route Orange** (oren-jalur): the 4px rim on tiles along a moving token's route, blended from cream at low strength to full orange at the lead tile.
- **Medal Gold** (kuning-tua) and **Ribbon Red** (merah-tua): the winner's rosette only.

### Neutral
- **Terpal Blue** (terpal): the tent ground on every screen, and the perforation dots of the karcis. **Terpal Shade** (terpal-gelap) for folds and the ground band; **Terpal Light** (terpal-terang) for alternate panels; **Seam Stitch** (terpal-jahit) for the dashed seams.
- **Cream** (krem): the reading surface. Question card, full-screen rule and setup boards, confirm dialog, karcis log, die, token ring, and light text on red or green paint.
- **Dark Cream** (krem-gelap): idle and spent states. Unselected toggles, idle scoreboard rows, spent answer options, read-only (bot) name fields, karcis dotted separators.
- **Pale Yellow** (kuning-pucat): alternate board tiles in the checker, answer options while another player (or a bot) is answering, and the timer's countdown arc.
- **Ink** (tinta): primary text, die pips, token outline, focused field rim, the timer disc, answer letter badges.
- **Soft Ink** (tinta-lembut): secondary text, form labels, the question status line, inactive scoreboard rows, older log lines, log serial numbers.
- **Muted Tarp** (tombol-mati): disabled plank buttons, with Dark Cream text.
- **Field Rim** (garis-kolom): the idle rim of a text field.
- **Night Shadow** (bayangan): the tint of every drop shadow and the modal dim.
- **Letterbox** (letterbox): the bars around the scaled canvas.

Player colours are fixed by order and never reused for UI: **Merah** (pemain-merah), **Biru** (pemain-biru), **Hijau** (pemain-hijau), **Kuning** (pemain-kuning).

### Named Rules
**The Rationed Heat Rule.** Only three things burn bulbs at full: the eight-bulb ring around the active player's tile, the bulbs on the route ahead of a moving token, and the winner screen's string. Frame bulbs idle at most 0.55 heat with a slow sweep; the menu string chases. If everything is lit, nothing is.

**The Cream Reads Rule.** Anything meant to be read at length (a question, a rule, a log line) sits on Cream or Dark Cream in Ink. Red, yellow and green planks carry short sign words only.

**The Colour Plus Number Rule.** A player is never identified by colour alone; every token carries its player number in Bungee, Ink on Kuning, Cream on the other three.

## Typography

**Display Font:** Bungee (bundled Bungee-Regular.ttf; falls back to the pygame default font at 1.3x size only if the file is missing)
**Body Font:** Atkinson Hyperlegible (bundled Regular and Bold)

**Character:** Bungee is the stall's hand-painted sign lettering: all caps, chunky, used for every heading, button, label and numeral. Atkinson Hyperlegible is the plain booth card: a high-legibility humanist sans for questions, answers, names, rules and the log.

### Hierarchy
- **Display** (Bungee, 68px): the stall name sign "ULAR TANGGA" and "<NAME> MENANG!" on the winner sign; steps down to 40px then 28px when a long winner name would not fit.
- **Headline** (Bungee, 40px): screen titles on cream boards (CARA BERMAIN, DAFTAR PEMAIN), the KUIS plaque, the rosette "1".
- **Title** (Bungee, 28px): fallback step for the winner sign only.
- **Numeral** (Bungee, 26px): ranking positions on the winner table.
- **Button** (Bungee, 22px): plank button labels; wraps to two lines inside the plank with a 10px side inset.
- **Label** (Bungee, 18px): tile numbers, the MULAI start-tile word and the FINIS word, panel titles (PAPAN SKOR · SULIT, GILIRAN ..., RIWAYAT PERMAINAN), setup toggles and form labels, the sound pill, answer letters, timer digits and DETIK, log serials, marker digits, score pops, dialog titles.
- **Question** (Atkinson Hyperlegible Bold, 24px): the question text, up to two lines; a question needing more drops to Body Strong (20px), max three lines.
- **Body** (Atkinson Hyperlegible Regular, 20px, 26px line pitch): rules text on the how-to-play board, wrapped at 560px.
- **Body Strong** (Atkinson Hyperlegible Bold, 20px): the menu tagline, name fields, names in the ranking table, legend headings.
- **Small** (Atkinson Hyperlegible Regular, 18px): helper text (difficulty summary, question count), score lines ("Petak 17  ·  45 poin"), log lines, footer, dialog body.
- **Small Strong** (Atkinson Hyperlegible Bold, 18px): answer option text (two lines max, 20px pitch), player names on the scoreboard, the question status line, error messages, the newest log line.

### Named Rules
**The 18px Floor Rule.** No text renders below 18px on the 1280x720 canvas. Shrink by stepping down the ramp, never by inventing a size.

**The Sign and Card Rule.** Bungee is never used for a sentence; Atkinson is never used for a sign word. Headings, buttons, labels and numerals are Bungee; anything with a verb in it is Atkinson.

## Layout

A fixed 1280x720 logical canvas, drawn once per frame and scaled uniformly (smoothscale) into a resizable window, centred with Letterbox bars. The initial window takes the largest scale up to 1.0 that fits 94% of the desktop width and 86% of its height. There are no breakpoints; the composition never reflows.

**Game screen.** The board sits left at (30, 48): an 8x8 grid of 78px tiles (624px square), numbered zig-zag from 1 at bottom left to 64 at top left, wrapped in an 18px red bulb frame (660px outer). The right column starts at x 696 and is 560px wide, a stack of four planks separated by 10px: scoreboard (y 24, 140 tall), question card (y 174, 262 tall, the largest), dice counter (y 446, 56 tall and 484 wide, with the 52px die centred 30px from the column's right edge), karcis log (y 512, 192 tall, 7 rows at 23px).

**Tokens on the board.** A lone token sits 6px below its tile centre. Tokens sharing a tile spread to four fixed offsets (17px left or right, 11px up or 19px down) so all four fit inside one 78px tile.

**Menu.** A bulb string sags across the top (y 56, 46px sag, 27 bulbs); the 800x196 name sign hangs from two cords at y 128 with the 240x66 plaque straddling its bottom edge; the tagline sits at y 392; a centred stack of three 340x62 planks with 12px gaps starts at y 432. Painted props (a leaning ladder left, an upright snake right) stand at the stall's sides.

**Reading boards.** How-to-play and setup use a single full-height cream board (1040 or 1000 wide, 640 tall, 40px from the top) with a 48 to 50px inner margin; how-to-play splits into numbered rules left and a legend column 730px in.

**Setup grid.** Form labels in a column at x 190, controls from x 420. Rows: MODE (y 118), JUMLAH PEMAIN (y 170), KESULITAN (y 222, with a Small summary "N tangga · N ular", plus "· bot benar ±N%" against bots, 18px after the last toggle), NAMA PEMAIN (fields from y 282 at a 52px pitch), KATEGORI SOAL (y 500, question count below at y 562), footer planks at y 596. Toggles size to their word plus 26 to 34px and sit 8px apart.

**Rhythm.** 8px between sibling cells (scoreboard cells, toggles); 10px between answer options and between right-column planks; 12 to 18px panel insets; 24 to 30px from the canvas edge.

## Elevation & Depth

Depth is physical and soft: painted boards cast blurred shadows onto the tent, and tokens cast an ellipse onto the table. Shadows are Night Shadow tinted, made by downscaling and upscaling a filled shape (a real blur), always offset straight down. There are no hard offset blocks. Tonal layering does the rest: tiles inside the frame, cream cards on the tent, dim overlays for modals and for off-route tiles.

### Shadow Vocabulary
- **Plank** (offset 0 6px, blur 10, Night Shadow at 90/255): every painted board and button at rest.
- **Ticket** (offset 0 3px, blur 5, 70/255): the karcis log.
- **Counter** (offset 0 5px, blur 6, 80/255): the die.
- **Floor** (ellipse, black at 70/255, 10px tall, as wide as the token and narrowing as it lifts): under every token.
- **Spent** (none): answer options that are no longer clickable drop their shadow and sit flat.
- **Modal dim** (full-canvas Night Shadow at 160/255): behind the exit confirmation.
- **Route dim** (deep blue at 55/255 over each tile): off-route tiles while a token moves, so the lit route reads.

### Named Rules
**The Lift Means Live Rule.** Raised means interactive or current: hovered planks rise 2px, the active scoreboard row rises 3px, a moving token lifts in an arc. Spent things lose their shadow and sit flat.

## Shapes

Rounded rectangles throughout, with radius growing with the object: 4px for tile number chips and route rims, 6px for karcis, destination markers and the sound pill, 8px for fields and score rows, 9px for answer options, 10px for planks and the plaque, 12px for the right-column panels, 14px for the board frame, dialog and ranking table, 16px for the big signs and full-screen boards. Tiles themselves are square-cornered, butted edge to edge with a 1px seam darkened 18%. Circles carry identity and state: tokens, bulbs, the timer disc, answer letter badges, rule numbers. The finish tile carries a two-row cream checker band of 9px squares; the karcis carries a left stub with a perforation line of 2px dots every 7px. Destination markers carry a drawn triangle, never a glyph.

## Components

### Buttons (painted price planks)
Tactile and loud, like price boards nailed to a stall.
- **Shape:** rounded plank (10px), drawn by the painted-board routine: flat fill, 3px gloss strip, 3px rim 35% darker, Plank shadow.
- **Primary:** Sign Yellow with Ink text (MULAI, MULAI MAIN, KEMBALI on how-to-play, MAIN LAGI (RESTART)).
- **Secondary:** Cream with Ink text (CARA BERMAIN, KELUAR, BATAL, KEMBALI on setup, MENU UTAMA).
- **Danger / Roll:** Stall Red with Cream text (YA, KELUAR; KOCOK DADU).
- **Hover:** fill lightens 14% and the plank rises 2px. No hover on touch.
- **Disabled:** Muted Tarp with Dark Cream text, still legible; the label explains the wait (JAWAB SOAL DULU, BIDAK BERJALAN..., <NAME> MENGOCOK..., GILIRAN PINDAH..., PERMAINAN SELESAI).

### Toggles (setup choices)
- **Style:** plank buttons 44px tall in the 18px Label size, width fitted to the word.
- **State:** selected is Stall Red with Cream text; unselected is Dark Cream with Ink. Categories with no questions disable.
- **Rows:** MODE (PASS & PLAY, VS BOT), JUMLAH PEMAIN (2, 3, 4), KESULITAN (MUDAH, SEDANG, SULIT; Sedang preselected), KATEGORI SOAL (three subjects plus CAMPURAN). Each row may carry a Small Soft Ink note to its right.

### Answer Options
Four planks (9px) in a 2x2 grid at the bottom of the question card, each with a 28px letter badge and two lines of Small Strong text. The badge is a disc in the option's text colour with the letter in the plank's own colour.
- **Live:** Sign Yellow, hover lightens 25% and lifts 2px.
- **Waiting (other player or bot):** Pale Yellow with Soft Ink.
- **Resolved:** the key turns Ladder Green, a wrong pick turns Stall Red, the rest go Dark Cream; all lose their shadow.

### Question Card (ticket booth)
- **Corner Style:** 12px, Cream body, 3px rim 35% darker.
- **Header:** 44px Sign Yellow band with the active token, "GILIRAN <NAME>" in Label, DETIK in Label, and a timer disc (36px, Ink; Stall Red at 10 seconds or less) with a Pale Yellow countdown arc.
- **Status line:** while answering, "<kategori> · <materi>" in Small Strong Soft Ink (the materi part drops when a question has none), with "· <bot> sedang berpikir..." appended on a bot's turn; after answering, the result in Deep Green (BENAR) or Stall Red (SALAH, WAKTU HABIS, with the key).
- **Entry:** each new question slides in 40px from the right over 0.35s.

### Scoreboard Plank
- Stall Red panel; the title reads "PAPAN SKOR · <KESULITAN>" in Cream Label, so the chosen difficulty stays visible all game.
- A 150x24 sound pill top right ("SUARA: NYALA" / "SUARA: MATI" in Cream Label), Stall Red darkened 20% at rest and lightened 20% on hover.
- 2x2 player rows (48px): the active row is Sign Yellow with a 2px rim darkened 40% and raised 3px; idle rows are Dark Cream with Soft Ink. Each row has the token (17px radius), the name in Small Strong (with "(bot)" for bots, truncated to fit), and "Petak N  ·  S poin" in Small.
- Scores count toward their new value; gains float up as a Ladder Green "+10" or "+5" that fades over 1.2s.

### Karcis Log
- A cream ticket with a 64px stub column of three-digit serials ("010") under a "NO." head, a perforation of Terpal Blue dots, and dotted Dark Cream separators between rows.
- Newest line on top in Small Strong Ink; older lines Small Soft Ink; long lines truncate with "...". Scroll state shows as "GULIR n/m" in the head.

### Inputs / Fields
- **Style:** 320x42 Cream field, 8px radius, 2px Field Rim, Body Strong Ink text inset 14px; the player's token (17px radius) sits to its left.
- **Focus:** rim becomes Ink at 3px; a 2px Ink caret blinks at 2Hz; an "n/12" counter appears to the right.
- **Error:** rim becomes Stall Red at 3px and the message appears to the right in Small Strong red.
- **Read-only (bot):** Dark Cream fill with a "BOT" tag in Label Soft Ink at the right end.

### Board (lit stall table)
- 64 tiles of 78px alternating Cream and Pale Yellow, numbered zig-zag from the bottom left; each number sits in Label on a chip of the tile's own colour at the top left so it stays readable over props. Tile 1 reads MULAI instead of its number; tile 64 is the red FINIS tile with its number, the word FINIS in Label and a checker band.
- Ladder foot tiles carry a 12% green tint and snake head tiles a 12% purple tint. Both carry a 49x24 destination marker at the bottom right: a cream triangle (up for a ladder, down for a snake) and the destination number in Label Cream, on Ladder Green or Snake Purple.
- The frame is a Stall Red plank with bulbs every 36px around it.
- Difficulty sets the props: Mudah 6 ladders and 3 snakes, Sedang 5 and 5, Sulit 4 and 8 (positions in config.py KESULITAN). Paint, size and drawing order do not change.

### Painted Snake and Ladder
- **Snake:** a sine-wave body tapering to 38% of its head width, Snake Shadow outline 3px wider, Snake Band stripes every fifth segment, an oval head with cream and ink eyes and a forked red tongue. One routine draws them all; body thickness is 10 on the board (head 4px above the tile centre), 17 for the menu prop and 9 in the legend, and the head scales with it.
- **Ladder:** two rails (Plywood Edge 9px under Plywood 4px) 22px apart, with rungs (Plywood Edge 7px under Plywood 3px) every 18px, extending 12px past both tile centres. The menu prop and legend use the same two-tone rail and rung build at their own sizes.

### Bulb
- A 6px glass on a dark socket (5px on tile rings and route corners), interpolated from Dead Bulb to Lit Bulb by heat; a soft radial glow (4x radius) above 0.05 heat; a Bulb Core highlight above 0.3.
- **Active ring:** eight bulbs around the active player's tile, 8px inside its edge.
- **Route:** a Lit Bulb wash, the Route Orange rim and four corner bulbs on each tile ahead of a moving token.

### Token and Die
- **Token:** 15px radius on the board (17 in the scoreboard, setup and legend, 14 in the question header, 15 in the ranking table, 26 on the winner sign): Ink outline, Cream ring, player-colour body with a highlight, player number in Bungee 18.
- **Die:** 52px Cream rounded square (radius one sixth of its size), 3px Ink rim, Ink pips; the single pip of a one is Stall Red.

### Confirm Dialog
- A 400x214 Cream board (14px) over the Modal dim, title in Label Ink ("KELUAR DARI PERMAINAN?"), one Small Soft Ink line of consequence, then BATAL (secondary) beside YA, KELUAR (danger).

### Stall Sign and Prize
- A Stall Red sign hung on two cords with a 4px rim and an inner 2px light rule 10px in, Display text in Cream; the menu adds the yellow plaque, the winner sign adds the winner's token, a gold rosette with red ribbon tails and a "1".

## Do's and Don'ts

### Do:
- **Do** draw every surface with the painted-board treatment: flat fill, 3px gloss strip lightened 22%, rim darkened 35%, Plank shadow.
- **Do** put the tent behind every screen, panels and seams included; never a flat blue fill.
- **Do** ration bulb heat: full burn only for the active tile ring, the moving route, and the winner screen.
- **Do** keep a player's colour and number together on every token, in every list.
- **Do** use Bungee for signs, labels and numerals and Atkinson Hyperlegible for questions, answers, names and sentences, at 18px or larger.
- **Do** state why a button is disabled in its own label.
- **Do** ease motion out (cubic) and make game events visible: tumble, hop, slide, count, pop.
- **Do** let difficulty change only the rules (prop count, bot accuracy) and name it where the game is played (the score header).
- **Do** add new colour values to config.py and draw props with primitives; no external art.

### Don't:
- **Don't** use hard, unblurred offset shadows; shadows are soft and fall straight down.
- **Don't** light every bulb outside the winner screen.
- **Don't** identify a player by colour alone.
- **Don't** set a sentence in Bungee or a sign word in Atkinson.
- **Don't** reuse player colours, Snake Purple or Ladder Green for unrelated UI.
- **Don't** give a difficulty level its own palette, tile size or prop style.
- **Don't** reflow the layout per window size; scale the 1280x720 stage whole.
- **Don't** drift toward a cartoon jungle board or a dark neon gamer HUD.
