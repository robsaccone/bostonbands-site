# Interactive Timeline Page — Design Spec

**Date:** 2026-04-05
**Status:** Approved
**Page:** `explore/timeline.html`

## Summary

A new standalone explore page presenting the 30-year history of Boston's local music scene (1996–2026) as a horizontally scrolling, interactive data visualization. A D3-rendered skyline chart of monthly gig activity runs along the bottom of the viewport, with 8 narrative era cards floating above it as the primary content. The skyline is the supporting visual backdrop; the narrative journey through the eras is the star.

## Architecture & Approach

- **D3-driven single canvas (Approach A):** The entire timeline is a single wide D3/SVG composition. Skyline bars, year markers, and era positions all share one x-scale. Era narrative cards are HTML overlays positioned absolutely using the same D3 coordinate system.
- **Tech stack:** Vanilla HTML/CSS/JS + D3.js v7 (already in the project from the Universe page). No build tools.
- **Data source:** New `data/timeline-extended.json` with monthly gig/band/venue counts spanning full date range (1996–2026).

## Page Layout

### Viewport Structure

```
┌──────────────────────────────────────────────────────┐
│  ← Back to BostonBands    THE TIMELINE      [2013]   │  ← Fixed header + year indicator
├──────────────────────────────────────────────────────┤
│                                                      │
│         ┌─────────────┐                              │
│         │  ERA CARD    │        ┌─────────────┐      │  ← Upper 60%: era narrative cards
│         │  1997        │        │  ERA CARD    │      │    (alternating vertical position)
│         │  The Rat     │        │  2009        │      │
│         │  Closes      │        │  Death of    │      │
│         └─────────────┘        │  Radio       │      │
│                                └─────────────┘      │
│                                                      │
│  ▁▂▁▁▁▂▃▃▂▂▃▃ ▂▂▂▂▂▂▂▂▂▂▂▁▁▁▁▁▁▁▁▁▁▂█████████████ │  ← Bottom 30%: D3 skyline
│  1996  1998  2000  2002  2004  2006  2008  2010  ... │    (sqrt scale, amber bars)
├──────────────────────────────────────────────────────┤
│  ℹ Explainer card                    → Swipe hint    │
└──────────────────────────────────────────────────────┘
```

### Fixed Elements

- **Header:** Same pattern as other explore pages — back link, page title, consistent nav
- **Year indicator:** Fixed top-right, updates as you scroll to show the current year in view. Barlow Condensed, amber text.
- **Scroll hint:** Pulsing horizontal arrow + "Swipe to explore" text. Fades after first scroll interaction. Appears on first visit only.
- **Explainer card:** Bottom-left overlay (same pattern as Universe page). Brief description: "30 years of Boston's music scene. Scroll to explore."

### Scroll Container

- `overflow-x: scroll`, `overflow-y: hidden`, fills remaining viewport height below header
- Contains a single wide container (~6500–7200px) holding the D3 SVG and positioned era cards
- Free horizontal scroll — mouse wheel maps to horizontal movement, native touch swipe on mobile
- No scroll-jacking, no snap points

## The Skyline Visualization

### Data & Scale

- **X-scale:** `d3.scaleLinear()` mapping month index (0–359 for 360 months) to pixel position
- **Y-scale:** `d3.scaleSqrt()` mapping gig count to bar height (sqrt balances early organic era visibility with import-era drama)
- **Bar dimensions:** ~16–20px width with 2px gap per month
- **Skyline height:** Bottom 30% of viewport (~200–250px)

### Bar Rendering

| Gig Count | Color | Opacity | Effect |
|-----------|-------|---------|--------|
| 0 | `#8a6a2a` | 0.3 | 1px baseline stub (skyline never breaks) |
| 1–20 | `#8a6a2a` | 0.4 | — |
| 21–100 | `#d4a03a` | 0.55 | — |
| 101–300 | `#d4a03a` | 0.65 | — |
| 301–700 | `#e8b84a` | 0.8 | — |
| 700+ | `#e8b84a` | 0.9 | Subtle amber glow (drop-shadow filter) |

- Year separator lines: faint vertical lines (`#222`) with year label below in `#777`
- Bars use `rx="1"` for slightly rounded tops (architectural feel)

### Tooltips

- **Desktop:** Hover triggers a floating div above the bar
- **Mobile:** Tap to show, tap elsewhere to dismiss
- **Content:** "March 2017 — 1,206 gigs · 984 bands · 170 venues"
- **Style:** Dark background (`#1a1a1a`), amber border accent, Barlow font, compact

### Pre-2012 Data

Months before the existing `timeline.json` range will have sparse or zero data. This is intentional and visually powerful — the flat skyline says "the data wasn't being collected yet" while the era cards carry the narrative for those years. The skyline comes alive in 2012 and the contrast reinforces the story.

## Era Narrative Cards

### 8 Era Stops

| # | Year | Title | Anchor Events |
|---|------|-------|---------------|
| 1 | 1996 | **The Heyday** | The Rat's final years, Dropkick Murphys form, WBCN era, Telecom Act begins radio consolidation |
| 2 | 2000 | **The Transition** | Letters to Cleo split, DIY culture rises, Dresden Dolls form, Great Scott goes live |
| 3 | 2006 | **The Unraveling Begins** | Infrastructure crumbling, Passion Pit at Emerson, WFNX signal boost |
| 4 | 2009 | **The Death of Radio** | WBCN dies after 41 years, WFNX sold (2012), Billy Ruane dies (2010) |
| 5 | 2013 | **Last One Standing** | Boston Phoenix final issue, Marathon bombing, Boston Calling born from the ashes |
| 6 | 2017 | **The Archive Opens** | BostonBands import spike, Boston Calling moves to Harvard, peak data years |
| 7 | 2020 | **The Silence** | COVID shuts live music, Great Scott closes permanently, scene devastated |
| 8 | 2022 | **Rebuilding** | Roadrunner opens (named for Jonathan Richman), Boston Calling returns, new venues |

### Card Design

- **Year:** Archivo Black, `clamp(2rem, 4vw, 3rem)`, amber color
- **Title:** Barlow Condensed 600, uppercase, 0.8rem, letter-spacing 0.1em
- **Summary:** 1–2 paragraphs, Barlow 400, `--text-body` color, line-height 1.7
- **Key events:** 2–4 compact bullet points, Barlow 300, `--text-dim` color
- **Optional image:** Era photo, 16:9 aspect, border-radius 4px, hover glow (same style as current timeline images)
- **Max-width:** 400px
- **Background:** Semi-transparent dark surface (`rgba(10,10,10,0.85)`) with subtle border and backdrop-blur

### Card Positioning

- Placed by the D3 x-scale at their anchor year's pixel position
- Alternate vertical position (upper-third / middle-third of the viewport) for visual rhythm
- Scroll-reveal animation: `opacity: 0 → 1`, `translateY(20px) → 0`, transition 0.7s ease-out-expo, triggered by IntersectionObserver on the horizontal scroll container

## Mobile Adaptations

- Skyline height increases to ~40% of viewport (larger touch targets)
- Minimum bar width of 12px
- Era cards go full-width with reduced padding and slightly smaller text
- Tooltips appear on tap with explicit close affordance
- Year indicator remains fixed top-right
- Horizontal swipe is native touch scroll — no special gesture handling needed
- Scroll hint adapted: "Swipe →" instead of arrow animation

## Data Pipeline Changes

### export_data.py

- **`export_timeline()`:** Remove the `g.gigdate >= '2012-01-01'` filter. Expand to full date range available in database. Write to `data/timeline-extended.json`.
- Keep existing `data/timeline.json` for backwards compatibility (nothing else uses it currently, but no reason to break it).

### New Data Files

- **`data/timeline-extended.json`:** Same schema as `timeline.json` — array of `{year, month, gigs, bands, venues}` — but spanning 1996–2026.
- **`data/eras.json`:** The 8 era definitions as a JSON file — `{year, title, summary, events[], image}`. Keeps content separate from layout code and makes future editing easy without touching HTML.

## Homepage Integration

- The current `#timeline` section in `index.html` gets replaced with an explore card that links to `explore/timeline.html`
- The explore grid expands from 4 to 5 cards: **Timeline** joins Universe, Map, Radio, Leaderboard
- Timeline card gets a prominent position (first card) since it tells the overarching story
- Card design: preview image of the skyline silhouette, title "The Timeline," subtitle "30 years of Boston music"

## Design Language Consistency

All styling follows existing site patterns:

- **Colors:** `--amber`, `--amber-glow`, `--surface-1` through `--surface-4`, `--text-body`, `--text-dim`
- **Fonts:** Archivo Black (display), Barlow Condensed (labels/nav), Barlow (body)
- **Animations:** `--ease-out-expo`, reveal classes with IntersectionObserver, 0.7–0.9s transitions
- **Effects:** Noise texture overlay, amber glow box-shadows, backdrop-filter blur on overlays
- **Page structure:** Fixed header with back link, explainer card bottom-left, full-bleed dark background

## Out of Scope

- Multi-layer data visualization (genre breakdowns, toggleable overlays) — keep it simple, skyline bars only
- Audio integration (linking to Radio from timeline events)
- Band/venue deep links from tooltips
- Animated transitions between eras (keep it as continuous scroll)

These could be future enhancements once the base timeline is solid.
