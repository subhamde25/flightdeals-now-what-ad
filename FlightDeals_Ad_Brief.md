# FlightDeals "Now what?" Ad: Creative Brief

## 1. Goal

Grab attention in the first two seconds and showcase three FlightDeals.in features: **Experiences, Transfers and Rent a car**. It's a short paid ad, so the message has to land even with the sound off.

| | |
| --- | --- |
| Brand | [FlightDeals.in](https://flightdeals.in/), "Compare flights, hotels & experiences" (tagline: COMPARE · DISCOVER · SAVE) |
| Format | 16:9, 1920×1080, 60 fps, 21.2 s |
| Placements | YouTube in-stream, the Meta feed (16:9), LinkedIn, X |
| Audience | People who have just booked, or are about to book, a flight and still have to plan the rest of the trip |
| Single-minded message | You've got the flight; FlightDeals has the rest of your trip covered. |
| Call to action | Book now (end card) |

## 2. The hook

**"You booked the flight. Now what?"**

Everyone knows the moment right after booking a flight: the trip plan still has empty slots for things to do, getting from the airport, and a car. The ad shows exactly that. A real-looking booking click turns into "Booked ✓", and then the empty trip slots pulse with a "?". Then "Now what?" slams in at 210 px over a blurred UI. It's a question the viewer answers in their head, and the brand answers it two seconds later on the music drop.

Why it works for an ad:

- The **first frame is already product UI in motion**, not a logo, so it doesn't read as an ad straight away.
- It's a **problem/solution in one breath**: the empty slots are the problem, and the three features fill them, one per scene.
- **Payoff symmetry**: the same trip card returns at 17.25 s with all four items ticked, which closes the loop.

## 3. Script (voiceover)

Voice: Fish Audio, **"Slax"** (calm, confident, professional male; a generic voice, not an impression of a real person). It was generated as one take and sped up to 1.05x without changing pitch. The timeline times below include the +0.25 s offset.

| Timeline (s) | Line | Burned-in caption |
| --- | --- | --- |
| 0.29–1.66 | You booked the flight. | yes |
| 1.97–2.81 | Now what? | no, shown as giant kinetic type instead |
| 3.31–5.99 | FlightDeals has the rest of your trip covered. | yes, in 2 chunks |
| 6.44–7.52 | Experiences: | no, the glass title shows it |
| 7.71–9.79 | tours and tickets, in a tap. | yes |
| 9.95–10.72 | Transfers: | no, the glass title shows it |
| 10.93–13.01 | a ride waiting the moment you land. | yes, in 2 chunks |
| 13.36–14.20 | Rent a car: | no, the glass title shows it |
| 14.41–16.83 | the right wheels, ready when you arrive. | yes, in 2 chunks |
| 17.25–18.19 | FlightDeals. | yes |
| 18.33–19.47 | More than flights. | no, the end-card tagline shows it |
| 19.64–20.37 | Book now. | no, the end-card button shows it |

The raw take is 21.3 s, and 20.3 s after the 1.05x speed-up. Word timings come from `tools/analyze_vo.py`, which finds the speech segments; words inside each segment are spread in proportion to their length.

## 4. Storyboard

The style reference is the "Frame by Frame launch video" by @notdwd on Prompt Motion: soft white, bright blue, glassy surfaces, an Apple-keynote feel. The camera never cuts on a still frame. Every shot enters already moving (exponential ease-out) and leaves on an accelerating move or a blur ramp, and the blur follows speed and direction.

| # | Time (s) | What you see | Motion and transitions |
| --- | --- | --- | --- |
| S1 | 0.00–3.25 | A light app window with the FlightDeals.in header: a boarding pass (LHR → BCN, FD 1204) on the left and a "Your trip" list on the right (Flight, Things to do, Airport transfer, Rental car). | The window rises out of a blue haze (0–0.5 s). The cursor glides in and clicks "Book flight", a mint ripple fills the button and it reads "Booked ✓" (0.93 s). The flight row gets a check. The three empty "?" slots pulse (1.42–1.66 s). The camera pushes in, the UI blurs, and "Now" (1.96 s) and "what?" (2.25 s) slam in. The scene whips up with a vertical blur into a light-blue flash, then a hard cut on the drop. |
| S2 | 3.25–6.25 | The FD logo on a white disc, with four tiles orbiting it: flights (white), Experiences (blue ticket), Transfers (cyan car), Rent a car (mint key). | The tiles spin in counter-clockwise and lock into a cross. The logo slides left as "FlightDeals.in" wipes in with its tagline. The white tile slips behind the logo, and the three colored tiles fly down and grow into labelled pills (4.61, 4.79, 4.97 s), which bounce on "covered". The camera zooms into the Experiences pill and blurs into the cut. |
| S3 | 6.25–9.75 | **Experiences.** A sunset catamaran illustration with the frosted-glass title "Experiences". It becomes a page with three cards: Sagrada Família, Sunset Catamaran and Montserrat Day Trip. | The hero rises in blurred, then shrinks into the middle card (7.27–7.89 s) as the side cards slide in. The cursor glides to "Book" and clicks at 9.21 s; the button turns mint ("Booked ✓"), the card lifts, and the toast "Booked · Sunset Catamaran, Sat 19:30" springs down. The scene whips left. |
| S4 | 9.75–13.25 | **Transfers.** A dark night-map hero with the title "Transfers". It becomes a map panel plus a right-hand panel with the flight status and driver card (Marco R., Premium van, 4821 LXB, €38 fixed, Meet & greet). | The hero comes in from the right with a horizontal smear, then shrinks into the map panel. A cyan route draws from BCN T1 to Barceloneta and the hotel pin drops. The driver card rises; "Waiting at Arrivals · Gate B" appears with a pulsing dot. A plane marker lands at the airport and the flight chip flips to "Landed 14:05 ✓" (12.75 s). The toast "Marco is waiting for you · Gate B" appears, then the scene zoom-blurs out. |
| S5 | 13.25–17.25 | **Rent a car.** A coastal road scene with an SUV and the title "Rent a car". It becomes a car carousel: Compact €24, SUV €39, Convertible €52, Electric €45 (partly off-screen). | The hero shrinks into the SUV card and the side cards slide in while the camera pans slowly. The cursor clicks "Select" (15.31 s) and the SUV lifts while the others dim. A frosted bottom sheet rises: "Ready on arrival · BCN Terminal 1 · Desk 12 · 14:30 · Confirmed", with a key icon that springs into place. The scene whips up. |
| S6 | 17.25–18.25 | **Payoff.** The "Your trip" card with the FD logo: Flight, Sunset Catamaran, Airport transfer and SUV rental, all filled in. | The card rises in; four mint checks pop at 17.45, 17.56, 17.67 and 17.78 s, then the card collapses accelerating into the cut. |
| S7 | 18.25–21.20 | **End card.** A black-navy radial background with the glowing FD logo and "FlightDeals.in", "More than flights.", the dots "• Experiences • Transfers • Rent a car", and a "Book now →" button. | The wordmark punches in with a horizontal zoom smear (16 copies) and settles with a slow continuous shrink. The tagline words land on the voice. "Book now" springs in at 19.64 s, the cursor clicks it at 20.55 s with a ring ripple and shine, and the film ends on a slow push. |

**Captions**: a dark frosted pill at the bottom centre (Inter 700, 44 px). The whole line shows dimmed, words light up white as they're spoken, and the current word is cyan `#7FD8FF`. There are no captions on the end card.

## 5. Sound design

**Music** (`audio/make_audio.py`, all synthesized)

- 120 BPM in D major. The intro pad is low-passed and brightens through the hook, then closes down for "Now what?" over the IV chord (G), with a snare build and riser. **The drop is at 3.25 s**, on D.
- Progression from the drop: D – Bm – G – A – D – Bm – G – A, two seconds per chord. At 18.25 s there's a big resolving D chord, with bells at 19.64 s for "Book now".
- Layers: a detuned-saw pad, a 16th-note pluck arpeggio with ping-pong delay (dotted eighth), a kick on every beat with sidechain pump, a clap on beats 2 and 4, off-beat and 16th hats, a sub bass on eighths, and crashes on every scene cut.

**SFX cue sheet** (all synthesized and cued to visual events)

| Time (s) | Event | Sound |
| --- | --- | --- |
| 0.00 | Window rises out of the haze | soft airy swell |
| 0.93 / 1.00 / 1.08 | "Book flight" click / booked / flight check | UI click / two-note chime / pop |
| 1.42–1.58 | "?" slots pulse | three descending pops |
| 1.96 / 2.25 | "Now" / "what?" slam | low thumps + boom |
| 2.25–3.25 | Build to the drop | riser + whoosh into the cut |
| 3.25 | **Drop**: logo on screen | sub boom + shimmer |
| 3.28 | Tiles orbit in | panning whoosh |
| 4.07 | Tiles lock | soft pop |
| 4.61 / 4.79 / 4.97 | Pills expand | rising pops |
| 5.55 | "covered" bounce | shimmer |
| 6.25, 9.75, 13.25, 17.25 | Scene cuts | whoosh into the cut + low boom |
| 7.10, 14.15 | Hero shrinks into the UI | soft swooshes |
| 9.21 / 9.24 / 9.25 | Book click / booked / toast | click / chime / short whoosh |
| 11.15 / 11.45 / 11.80 | Driver card rises / route draws / hotel pin | swish / gentle riser / pop |
| 12.75 / 12.79 | "Landed" / toast | three-note notification chime / whoosh |
| 15.31 / 15.34 / 15.50 / 15.72 | Select click / selected / sheet rises / key | click / chime / whoosh / key-jingle ticks |
| 17.45–17.78 | Four checks | ascending chimes |
| 18.25 | Hard cut to the end card | whoosh + deep boom + shimmer |
| 19.64 / 20.55 | "Book now" pops in / gets clicked | pop + shimmer / click + shimmer |

**Mix and master**

- The voice sits on top. The music ducks under it (envelope follower, about 8 dB of ducking) and comes up between lines.
- Levels measured per window during speech: voice ≈ −15.4 LUFS, music ≈ −26 LUFS (10–11 LU under), SFX −22 to −30 LUFS.
- The master uses two-pass `loudnorm` to **−14 LUFS integrated / −1 dBTP**, with a 60 ms fade at the end. The final file measures −13.9 LUFS with a −1.6 dB peak.

## 6. Brand

- **Logo**: the official FD monogram (a winged blue "F" merging into a "D", with a light-blue swoosh and a gold plane), from `https://flightdeals.in/logo512.png`. `tools/key_logo.py` makes its white background transparent. It appears in the S1 app header, the S2 lockup, the S6 trip card and the S7 end card.
- **Wordmark**: "FlightDeals" in Space Grotesk 600 with ".in" in teal `#239587`, and "COMPARE · DISCOVER · SAVE" underneath, matching the site header.
- **Ad palette**: page `#FDFDFB`, navy `#1E2F52`, blue `#2F6BFF` (Experiences), cyan `#3CC8F0` (Transfers), mint `#4ED6A0` (Rent a car and the "done" states). The site's own colours are navy `#0C1E45` / `#0A2342` and teal `#239587`.
- **Type**: Inter 400–800 for the UI and captions, Space Grotesk 600 for the wordmark.

## 7. Claims check

Checked against the live site on **15 Oct 2026**:

| Claim or element in the ad | Status |
| --- | --- |
| FlightDeals.in offers Experiences, Transfers and Car Rentals | ✅ All three are in the site's main navigation (along with Deals, Flights, Hotels, Visa, eSIM, Tours, Itineraries and AI Planner). |
| Logo, wordmark and tagline | ✅ Official assets and site styling. |
| In-app **"Book" / "Booked ✓" / "Selected ✓" / "Confirmed"** flows | ⚠️ **Review before running.** The site describes itself as "Metasearch · Compare · Book with partners" and says "Book on partner sites". The ad's UI suggests you book directly inside FlightDeals. Consider changing the wording to "Compare & book with partners", or label the UI "Illustrative". |
| Prices in **€** (flight €89, tours from €34/€49/€62, transfer €38, cars €24–€52/day) | ⚠️ Illustrative. The site shows prices in **₹ INR**, and most of its audience searches from India. Consider ₹ prices and an India-origin route such as DEL → BCN. |
| Trip details: London → Barcelona, flight FD 1204, 24–28 Oct, the driver "Marco R.", plate 4821 LXB, ratings and review counts, desk numbers | ⚠️ Illustrative placeholders. They aren't live data and aren't a real airline flight. |
| "No booking fees" | Not claimed in this ad. The site says it, so it could be added. |
| Voice | ✅ A generic Fish Audio voice, not an impersonation. |
| Music and SFX | ✅ Original and synthesized, so there's no licensing risk. |

## 8. Production log

| Date | Change |
| --- | --- |
| 15 Oct 2026 | v1: Brief from the user (16:9 ad; hook; motion graphics, SFX, BGM, captions; Fish Audio voice; reference video on Prompt Motion). The voice, voiceover tempo, composition, audio and render were all built. The music was rebalanced after measuring that it sat as loud as the voice; it now sits about 10 LU under it. |
| 15 Oct 2026 | v2: The placeholder logo was replaced with the **real FlightDeals.in logo** and wordmark, found on flightdeals.in and downloaded with the user's OK. |
| 30 Oct 2026 | The project was reorganized like `flightdeals-ad-studio` (h169 / audio / assets / deliverables / build), with docs, `final.sh` and npm scripts added. The pipeline was re-run and checked: −13.9 LUFS / −1.6 dB peak. |

Fish Audio usage: 299 credits for the voice take and 184 credits for a transcription check (the flash model). Render: 1,272 frames at about 3 fps, about 8 minutes on an 8 GB laptop.
