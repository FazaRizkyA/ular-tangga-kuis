---
version: 1
slug: "main-py"
primary_target: "main.py"
related_targets: []
---

# Surface: Ular Tangga Kuis game window (all four screens)

Mode: Experience (the game is the work; it leads from the first frame). Native desktop Pygame window, logical canvas 1280x720.

Audience & job: class XI students taking turns on one laptop, and the examining teacher. Answer a question, roll, move, see who leads, finish.

Constraints: PRODUCT.md rules (64 tiles 8x8; ladder/snake layout and bot accuracy per difficulty Mudah/Sedang/Sulit from config.py KESULITAN; bounce; 30 s timer; +10/+5). Player colours fixed: merah, biru, hijau, kuning, plus player number. Text >= 18 px. Bundled .ttf only. Offline.

## Direction contract

THESIS: Snakes and ladders as a pasar malam game stall: the board is a lit stall table, the question is bought at the ticket booth, the dice are thrown on the counter. Refuses the cartoon jungle board and the dark neon gamer HUD.

OWN-WORLD: Terpal-blue tent ground (deep tarp blue with stitched seam lines), plywood stall boards painted in flat sign-painter colours (red, green, yellow, cream), bulb strings with lit and unlit bulbs, paper karcis with a perforated edge and serial numbers. Hand-painted sign lettering for headings (bold condensed display), plain humanist sans for questions and data, tabular digits. Raises: heat rationed (only the active player's tile and bulbs burn full; the rest dim); the active scoreboard row lifts while others dim; score and dice changes are visible events; the log is a stack of karcis, newest on top; tabular numerals everywhere.

STORY: A player sees whose turn it is from the lit bulbs, reads the question on the booth's plain cream board, answers, watches the dice tumble on the counter, sees the route light ahead tile by tile, and the token hops. Ladders and snakes read as the stall's painted props. The finish is the stall's prize moment.

FIRST VIEWPORT: Menu: the stall's painted sign "ULAR TANGGA KUIS" under a bulb string across a tarp-blue field, three painted plank buttons (Mulai, Cara Bermain, Keluar) stacked like stall price boards. Game screen: left 624x624 board as a bulb-framed stall table (8x8 painted tiles, numbers in sign lettering, ladders as painted wood, snakes as painted bodies); right column: scoreboard plank (top), ticket booth question card (largest, primary), dice counter button, karcis log.

FORM: Grounded candidate 6 of 7 (Stan Pasar Malam), seed:3e2e8e3ad42359b7. Signature interaction: after a correct answer the dice tumble on the counter, then the bulbs along the path light one by one ahead of the token. Motion grammar: bulbs warm up and cool down (ease), tokens hop per tile, cards slide in like a ticket pushed under the booth window.

FINISH: unreviewed and undocumented is unfinished; this build ends with the finish review, the verdict, DESIGN.md, and every shipping raster carrying its provenance
