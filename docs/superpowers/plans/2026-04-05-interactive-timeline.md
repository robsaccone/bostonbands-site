# Interactive Timeline Page — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a horizontally scrolling, D3-driven timeline page at `explore/timeline.html` that visualizes 30 years of Boston music history as a skyline bar chart with narrative era cards.

**Architecture:** Single-page D3 + vanilla JS app. A sqrt-scaled SVG skyline of monthly gig data spans 1996–2026 along the bottom 30% of the viewport. Eight HTML era narrative cards float above, positioned by the same D3 x-scale. Free horizontal scroll, tooltips on hover/tap.

**Tech Stack:** HTML, CSS, JavaScript, D3.js v7 (already loaded in project via CDN)

**Spec:** `docs/superpowers/specs/2026-04-05-interactive-timeline-design.md`

---

## File Structure

| Action | File | Responsibility |
|--------|------|----------------|
| Create | `data/eras.json` | 8 era definitions (year, title, summary, events, image) |
| Create | `explore/timeline.html` | Complete timeline page (HTML + CSS + JS) |
| Modify | `export_data.py:188-201` | Add `export_timeline_extended()` function |
| Modify | `export_data.py:291-308` | Wire new export into `main()` |
| Modify | `index.html:1370-1441` | Replace inline timeline with link to explore page |
| Modify | `index.html:1549-1573` | Add Timeline card to explore grid |
| Generate | `data/timeline-extended.json` | Output of running updated export script |

---

### Task 1: Create Era Content Data

**Files:**
- Create: `data/eras.json`

- [ ] **Step 1: Create `data/eras.json`**

This file contains the 8 narrative era definitions. Each era has a year anchor, title, summary paragraph, key events list, and optional image path. The summary text draws from the user's research document.

```json
[
  {
    "year": 1996,
    "title": "The Heyday",
    "summary": "The Rat ruled Kenmore Square, WBCN owned the airwaves, and the Dropkick Murphys formed in a Quincy barbershop basement. The Telecommunications Act of 1996 began the slow corporate takeover of radio that would eventually gut local music coverage. But for now, the scene was electric — Letters to Cleo, Mighty Mighty Bosstones, and Morphine were all in their prime.",
    "events": [
      "Dropkick Murphys form in Quincy, MA",
      "The Rat in its final years as punk ground zero",
      "WBCN and the golden age of Boston rock radio",
      "Telecom Act triggers nationwide radio consolidation"
    ],
    "image": null
  },
  {
    "year": 2000,
    "title": "The Transition",
    "summary": "The Rat closed in '97. Mark Sandman died onstage in '99. The old guard was fading, but something new was taking root — DIY house shows filled the gaps left by shrinking venues, the Dresden Dolls invented 'Brechtian punk cabaret' in a Boston loft, and Great Scott started its transformation into an every-night live music room in Allston.",
    "events": [
      "The Rat closes after 23 years (1997)",
      "Mark Sandman's death onstage (July 1999)",
      "Dresden Dolls form — Amanda Palmer's rise begins",
      "DIY house show culture takes root"
    ],
    "image": null
  },
  {
    "year": 2006,
    "title": "The Unraveling Begins",
    "summary": "Dropkick Murphys' 'I'm Shipping Up to Boston' exploded via Scorsese's The Departed and became the sound of Boston sports. But beneath the surface, the infrastructure was crumbling. WFNX got a signal boost in 2006, buying time, while Passion Pit formed at Emerson College — proof the scene still had creative fire even as the ground shifted.",
    "events": [
      "'Shipping Up to Boston' goes national via The Departed",
      "Passion Pit forms at Emerson College (2007)",
      "WFNX signal boost — last stand of indie radio",
      "The Abbey closes in Inman Square (2008)"
    ],
    "image": null
  },
  {
    "year": 2009,
    "title": "The Death of Radio",
    "summary": "WBCN signed off on August 11, 2009, after 41 years — its last song was Pink Floyd's 'Shine On You Crazy Diamond.' Three years later, WFNX was sold to Clear Channel for $14.5 million, its last song The Cure's 'Let's Go to Bed.' Billy Ruane — the man who helped build the Middle East into a music venue and championed everyone from Nirvana to local unknowns — died in October 2010. The connective tissue was tearing.",
    "events": [
      "WBCN dies after 41 years (August 2009)",
      "Billy Ruane dies — irreplaceable scene catalyst (2010)",
      "WFNX sold to Clear Channel for $14.5M (May 2012)",
      "RadioBDC launches as digital successor"
    ],
    "image": null
  },
  {
    "year": 2013,
    "title": "Last One Standing",
    "summary": "The Boston Phoenix published its final issue in March 2013 — 47 years of music listings, band coverage, and local culture, gone. The Rat was gone. WBCN was gone. WFNX was gone. The Phoenix was gone. BostonBands was the last one standing. Then, on April 15, the Marathon bombing shook the city. Six weeks later, Boston Calling launched at City Hall Plaza — co-founded by former WFNX staffers — and became the first major public gathering post-bombing. A cathartic moment from the ashes.",
    "events": [
      "Boston Phoenix publishes final issue (March 2013)",
      "Boston Marathon bombing (April 15, 2013)",
      "Boston Calling launches at City Hall Plaza (May 2013)",
      "BostonBands — the last one standing"
    ],
    "image": null
  },
  {
    "year": 2017,
    "title": "The Archive Opens",
    "summary": "In late 2016, BostonBands began importing gig data from external sources — SongKick, BandsInTown, TicketWeb — and the archive exploded. Monthly gig counts jumped from dozens to over a thousand. Boston Calling moved to the Harvard Athletic Complex, tripling its footprint. For three years the data painted a portrait of the full Boston music ecosystem: every bar band, every open mic, every sold-out headliner.",
    "events": [
      "BostonBands bulk import — data explodes (late 2016)",
      "Boston Calling moves to Harvard Athletic Complex (2017)",
      "Peak data years: 900–1,200 gigs per month",
      "Dropkick Murphys' 11 Short Stories debuts at #8"
    ],
    "image": null
  },
  {
    "year": 2020,
    "title": "The Silence",
    "summary": "COVID-19 shut down live music in March 2020 and devastated Boston's already-fragile small venue ecosystem. Great Scott — 44 years in Allston, the room where countless bands got their start — closed permanently. McGreevy's shuttered. Boston Calling was canceled. The silence was deafening, and for many venues and musicians, it was permanent.",
    "events": [
      "COVID-19 shuts down all live music (March 2020)",
      "Great Scott closes permanently after 44 years",
      "McGreevy's closes (August 2020)",
      "Boston Calling canceled — won't return until 2022"
    ],
    "image": null
  },
  {
    "year": 2022,
    "title": "Rebuilding",
    "summary": "On March 15, 2022, Roadrunner opened in Brighton — 3,500 capacity, the largest indoor GA venue in New England, named after Jonathan Richman's 'Roadrunner.' Billy Strings played opening night. Two months later, Boston Calling returned with a stage devoted exclusively to local talent. MGM Music Hall opened at Fenway. The scene wasn't what it was — but it was alive, and building something new.",
    "events": [
      "Roadrunner opens — named for Jonathan Richman (March 2022)",
      "Boston Calling returns with local music stage (May 2022)",
      "MGM Music Hall at Fenway opens (2022)",
      "Noah Kahan rises from the New England scene"
    ],
    "image": null
  }
]
```

- [ ] **Step 2: Verify the JSON is valid**

Run:
```bash
python -c "import json; json.load(open('data/eras.json')); print('Valid JSON, 8 eras')"
```
Expected: `Valid JSON, 8 eras`

- [ ] **Step 3: Commit**

```bash
git add data/eras.json
git commit -m "Add era content data for interactive timeline (8 eras, 1996-2022)"
```

---

### Task 2: Extend Data Export for Full Date Range

**Files:**
- Modify: `export_data.py:188-201` (add new function after existing `export_timeline`)
- Modify: `export_data.py:291-308` (add call in `main()`)
- Generate: `data/timeline-extended.json`

- [ ] **Step 1: Add `export_timeline_extended()` to `export_data.py`**

Insert this function directly after the existing `export_timeline` function (after line 201):

```python
def export_timeline_extended(cur):
    """Export monthly gig counts for full-range timeline (1996-2026)."""
    print("\n=== Timeline Extended ===")
    cur.execute(f"""
        SELECT EXTRACT(YEAR FROM g.gigdate)::int as year,
               EXTRACT(MONTH FROM g.gigdate)::int as month,
               COUNT(*) as gigs,
               COUNT(DISTINCT g.bandid) as bands,
               COUNT(DISTINCT g.venueid) as venues
        FROM gigs g
        WHERE {GIG_FILTER} AND g.gigdate >= '1996-01-01' AND g.gigdate < '2027-01-01'
        GROUP BY year, month ORDER BY year, month
    """)
    write_json("timeline-extended.json", [dict(r) for r in cur.fetchall()])
```

- [ ] **Step 2: Wire into `main()`**

In the `main()` function, add the call after `export_timeline(cur)`:

```python
    export_timeline(cur)
    export_timeline_extended(cur)
```

- [ ] **Step 3: Verify database connectivity**

Run:
```bash
cd D:\myrepos\bostonbands
.venv\Scripts\activate
python -c "import psycopg2; conn = psycopg2.connect(host='localhost', port=5433, user='postgres', password='newpassword', dbname='bostonbands'); print('Connected'); conn.close()"
```
Expected: `Connected`

If this fails, the database isn't running — start it before proceeding.

- [ ] **Step 4: Run the export**

Run:
```bash
cd D:\myrepos\bostonbands
.venv\Scripts\activate
python export_data.py
```
Expected: Output includes `=== Timeline Extended ===` line with a file size. Check the output file:
```bash
python -c "import json; d=json.load(open('data/timeline-extended.json')); print(f'{len(d)} months, {d[0][\"year\"]}-{d[-1][\"year\"]}')"
```
Expected: Something like `N months, 1996-2026` (or whatever the earliest gig date is). The exact count depends on available data — pre-2012 months may be sparse or absent.

- [ ] **Step 5: Commit**

```bash
git add export_data.py data/timeline-extended.json
git commit -m "Add extended timeline export spanning 1996-2026 for interactive timeline"
```

---

### Task 3: Create Timeline Page — HTML Shell & CSS

**Files:**
- Create: `explore/timeline.html`

This task creates the full page structure with all CSS. JavaScript is added in Task 4.

- [ ] **Step 1: Create `explore/timeline.html` with HTML structure and all CSS**

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Timeline — BostonBands Archive</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Barlow:wght@300;400;500;600&family=Barlow+Condensed:wght@400;600;700&display=swap" rel="stylesheet">
<style>
:root {
  --black: #050505;
  --surface-1: #0a0a0a;
  --surface-2: #111111;
  --surface-3: #1a1a1a;
  --surface-4: #222222;
  --text-dim: #777777;
  --text-muted: #999999;
  --text-body: #c0c0c0;
  --text-bright: #e8e8e8;
  --white: #f5f5f0;
  --amber: #d4a03a;
  --amber-glow: #e8b84a;
  --amber-dim: #8a6a2a;
  --font-display: 'Archivo Black', sans-serif;
  --font-condensed: 'Barlow Condensed', sans-serif;
  --font-body: 'Barlow', sans-serif;
  --ease-out-expo: cubic-bezier(0.16, 1, 0.3, 1);
}
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: var(--font-body);
  font-weight: 300;
  color: var(--text-body);
  background: var(--black);
  overflow: hidden;
  height: 100vh;
}
body::before {
  content: '';
  position: fixed;
  inset: 0;
  z-index: 9999;
  pointer-events: none;
  opacity: 0.03;
  background: url("data:image/svg+xml,%3Csvg viewBox='0 0 256 256' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)'/%3E%3C/svg%3E");
}
a { color: var(--amber); text-decoration: none; }
a:hover { color: var(--amber-glow); }

/* === HEADER === */
.page-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1rem 1.5rem;
  background: rgba(5,5,5,0.92);
  backdrop-filter: blur(8px);
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid var(--surface-3);
}
.page-title {
  font-family: var(--font-display);
  font-size: 1rem;
  color: var(--white);
}
.page-title span { color: var(--amber); }
.page-back {
  font-family: var(--font-condensed);
  font-weight: 600;
  font-size: 0.8rem;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--text-dim);
}
.page-back:hover { color: var(--amber); }

/* === YEAR INDICATOR === */
.year-indicator {
  position: fixed;
  top: 0.85rem;
  right: 6rem;
  z-index: 1001;
  font-family: var(--font-condensed);
  font-weight: 700;
  font-size: 1.1rem;
  color: var(--amber);
  letter-spacing: 0.05em;
  transition: opacity 0.3s;
}

/* === SCROLL CONTAINER === */
.scroll-container {
  position: absolute;
  top: 52px; /* below header */
  left: 0;
  right: 0;
  bottom: 0;
  overflow-x: scroll;
  overflow-y: hidden;
  scrollbar-color: var(--surface-4) var(--black);
}
.scroll-container::-webkit-scrollbar { height: 6px; }
.scroll-container::-webkit-scrollbar-track { background: var(--black); }
.scroll-container::-webkit-scrollbar-thumb { background: var(--surface-4); border-radius: 3px; }

.timeline-canvas {
  position: relative;
  height: 100%;
  /* width set by JS based on data */
}

/* === SKYLINE SVG === */
.skyline-svg {
  position: absolute;
  bottom: 0;
  left: 0;
}

/* === ERA CARDS === */
.era-card {
  position: absolute;
  max-width: 400px;
  background: rgba(10,10,10,0.85);
  backdrop-filter: blur(8px);
  border: 1px solid var(--surface-4);
  border-radius: 6px;
  padding: 1.5rem 1.75rem;
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.7s var(--ease-out-expo), transform 0.7s var(--ease-out-expo);
}
.era-card.visible {
  opacity: 1;
  transform: translateY(0);
}
.era-card-year {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3rem);
  color: var(--amber);
  line-height: 1;
  margin-bottom: 0.25rem;
}
.era-card-title {
  font-family: var(--font-condensed);
  font-weight: 600;
  font-size: 0.8rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--text-muted);
  margin-bottom: 0.75rem;
}
.era-card-summary {
  font-size: 0.9rem;
  line-height: 1.7;
  color: var(--text-body);
  margin-bottom: 0.75rem;
}
.era-card-events {
  list-style: none;
  padding: 0;
}
.era-card-events li {
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--text-dim);
  padding-left: 0.75rem;
  position: relative;
  margin-bottom: 0.25rem;
}
.era-card-events li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0.55em;
  width: 4px;
  height: 4px;
  background: var(--amber-dim);
  border-radius: 50%;
}

/* === TOOLTIP === */
.bar-tooltip {
  position: fixed;
  z-index: 2000;
  background: var(--surface-3);
  border: 1px solid var(--amber-dim);
  border-radius: 4px;
  padding: 0.5rem 0.75rem;
  pointer-events: none;
  opacity: 0;
  transition: opacity 0.15s;
  white-space: nowrap;
}
.bar-tooltip.visible { opacity: 1; }
.bar-tooltip-date {
  font-family: var(--font-condensed);
  font-weight: 700;
  color: var(--white);
  font-size: 0.85rem;
}
.bar-tooltip-stats {
  font-family: var(--font-condensed);
  font-weight: 600;
  color: var(--amber);
  font-size: 0.8rem;
}

/* === EXPLAINER CARD === */
.explainer-card {
  position: fixed;
  bottom: 3rem;
  left: 1.5rem;
  z-index: 1000;
  background: rgba(10,10,10,0.85);
  backdrop-filter: blur(8px);
  border: 1px solid var(--surface-4);
  border-radius: 4px;
  padding: 1.25rem 1.5rem;
  max-width: 280px;
}
.explainer-title {
  font-family: var(--font-condensed);
  font-weight: 700;
  font-size: 0.75rem;
  letter-spacing: 0.15em;
  text-transform: uppercase;
  color: var(--amber);
  margin-bottom: 0.5rem;
}
.explainer-card p {
  font-size: 0.8rem;
  line-height: 1.5;
  color: var(--text-muted);
  margin-bottom: 0.5rem;
}
.explainer-hint {
  font-family: var(--font-condensed);
  font-size: 0.7rem;
  letter-spacing: 0.1em;
  color: var(--text-dim);
}

/* === SCROLL HINT === */
.scroll-hint {
  position: fixed;
  bottom: 3rem;
  right: 2rem;
  z-index: 1000;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-condensed);
  font-weight: 600;
  font-size: 0.75rem;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: var(--text-dim);
  transition: opacity 0.5s var(--ease-out-expo);
}
.scroll-hint-arrow {
  animation: scrollPulse 2s infinite;
  font-size: 1.2rem;
  color: var(--amber-dim);
}
@keyframes scrollPulse {
  0%, 100% { transform: translateX(0); opacity: 0.5; }
  50% { transform: translateX(6px); opacity: 1; }
}

/* === MOBILE === */
@media (max-width: 768px) {
  .explainer-card { display: none; }
  .era-card {
    max-width: 300px;
    padding: 1.25rem;
  }
  .era-card-summary { font-size: 0.85rem; }
  .year-indicator { right: 1rem; }
}
</style>
</head>
<body>

<header class="page-header">
  <div class="page-title">The <span>Timeline</span></div>
  <a href="../index.html#explore" class="page-back">&larr; Back</a>
</header>

<div class="year-indicator" id="yearIndicator">1996</div>

<div class="scroll-container" id="scrollContainer">
  <div class="timeline-canvas" id="timelineCanvas">
    <!-- D3 SVG and era cards injected by JS -->
  </div>
</div>

<div class="bar-tooltip" id="tooltip">
  <div class="bar-tooltip-date"></div>
  <div class="bar-tooltip-stats"></div>
</div>

<div class="explainer-card">
  <div class="explainer-title">The Timeline</div>
  <p>30 years of Boston's music scene. Each bar is one month of gigs. The taller the bar, the more music was happening.</p>
  <div class="explainer-hint">Scroll to explore &middot; Hover for details</div>
</div>

<div class="scroll-hint" id="scrollHint">
  Scroll to explore <span class="scroll-hint-arrow">&rarr;</span>
</div>

<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
// JS added in Task 4
</script>
</body>
</html>
```

- [ ] **Step 2: Open in browser to verify the shell renders**

Open `explore/timeline.html` in a browser. You should see:
- Fixed header with "The Timeline" and back link
- Year indicator top-right showing "1996"
- Explainer card bottom-left
- Scroll hint bottom-right with pulsing arrow
- Empty dark canvas (no data yet)

- [ ] **Step 3: Commit**

```bash
git add explore/timeline.html
git commit -m "Add timeline page HTML shell and CSS"
```

---

### Task 4: Implement D3 Skyline Visualization

**Files:**
- Modify: `explore/timeline.html` (replace the `// JS added in Task 4` comment with full JS)

- [ ] **Step 1: Replace the script placeholder with the full D3 visualization**

In `explore/timeline.html`, replace:
```javascript
// JS added in Task 4
```

With:
```javascript
(async function() {
  // --- Config ---
  const BAR_WIDTH = 18;
  const BAR_GAP = 2;
  const SKYLINE_RATIO = 0.30; // bottom 30% of viewport
  const PADDING_LEFT = 60;
  const PADDING_RIGHT = 60;

  const MONTH_NAMES = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  // --- Load data ---
  const [timelineData, erasData] = await Promise.all([
    d3.json('../data/timeline-extended.json'),
    d3.json('../data/eras.json')
  ]);

  // --- Build full month array (1996-01 through 2026-12) ---
  const dataMap = new Map();
  timelineData.forEach(d => dataMap.set(`${d.year}-${d.month}`, d));

  const allMonths = [];
  for (let y = 1996; y <= 2026; y++) {
    for (let m = 1; m <= 12; m++) {
      const key = `${y}-${m}`;
      allMonths.push(dataMap.get(key) || { year: y, month: m, gigs: 0, bands: 0, venues: 0 });
    }
  }

  // --- Dimensions ---
  const container = document.getElementById('scrollContainer');
  const viewportH = container.clientHeight;
  const skylineH = Math.round(viewportH * SKYLINE_RATIO);
  const canvasW = PADDING_LEFT + allMonths.length * (BAR_WIDTH + BAR_GAP) + PADDING_RIGHT;

  const canvas = document.getElementById('timelineCanvas');
  canvas.style.width = canvasW + 'px';

  // --- Scales ---
  const xScale = d3.scaleLinear()
    .domain([0, allMonths.length - 1])
    .range([PADDING_LEFT, canvasW - PADDING_RIGHT]);

  const maxGigs = d3.max(allMonths, d => d.gigs);
  const yScale = d3.scaleSqrt()
    .domain([0, maxGigs])
    .range([0, skylineH - 30]); // 30px top margin within skyline

  // --- Create SVG ---
  const svg = d3.select('#timelineCanvas').append('svg')
    .attr('class', 'skyline-svg')
    .attr('width', canvasW)
    .attr('height', skylineH);

  // --- Year separator lines & labels ---
  allMonths.forEach((d, i) => {
    if (d.month === 1) {
      const x = xScale(i);
      svg.append('line')
        .attr('x1', x).attr('y1', 0)
        .attr('x2', x).attr('y2', skylineH - 20)
        .attr('stroke', '#222')
        .attr('stroke-width', 0.5);
      svg.append('text')
        .attr('x', x + (BAR_WIDTH + BAR_GAP) * 6)
        .attr('y', skylineH - 6)
        .attr('text-anchor', 'middle')
        .attr('fill', '#555')
        .attr('font-family', 'Barlow Condensed, sans-serif')
        .attr('font-size', '10px')
        .text(d.year);
    }
  });

  // --- Bar color/opacity helper ---
  function barStyle(gigs) {
    if (gigs === 0) return { color: '#8a6a2a', opacity: 0.3 };
    if (gigs <= 20) return { color: '#8a6a2a', opacity: 0.4 };
    if (gigs <= 100) return { color: '#d4a03a', opacity: 0.55 };
    if (gigs <= 300) return { color: '#d4a03a', opacity: 0.65 };
    if (gigs <= 700) return { color: '#e8b84a', opacity: 0.8 };
    return { color: '#e8b84a', opacity: 0.9 };
  }

  // --- SVG filter for glow ---
  const defs = svg.append('defs');
  const glowFilter = defs.append('filter').attr('id', 'barGlow');
  glowFilter.append('feGaussianBlur').attr('stdDeviation', '3').attr('result', 'blur');
  glowFilter.append('feComposite').attr('in', 'SourceGraphic').attr('in2', 'blur').attr('operator', 'over');

  // --- Render bars ---
  const bars = svg.selectAll('.bar')
    .data(allMonths)
    .enter()
    .append('rect')
    .attr('class', 'bar')
    .attr('x', (d, i) => xScale(i))
    .attr('y', d => skylineH - 20 - Math.max(yScale(d.gigs), 1))
    .attr('width', BAR_WIDTH)
    .attr('height', d => Math.max(yScale(d.gigs), 1))
    .attr('rx', 1)
    .attr('fill', d => barStyle(d.gigs).color)
    .attr('opacity', d => barStyle(d.gigs).opacity)
    .attr('filter', d => d.gigs > 700 ? 'url(#barGlow)' : null)
    .style('cursor', 'pointer');

  // --- Tooltip ---
  const tooltip = document.getElementById('tooltip');
  const tooltipDate = tooltip.querySelector('.bar-tooltip-date');
  const tooltipStats = tooltip.querySelector('.bar-tooltip-stats');

  bars.on('mouseenter', function(event, d) {
    const rect = this.getBoundingClientRect();
    tooltipDate.textContent = `${MONTH_NAMES[d.month - 1]} ${d.year}`;
    tooltipStats.textContent = `${d.gigs.toLocaleString()} gigs \u00B7 ${d.bands.toLocaleString()} bands \u00B7 ${d.venues.toLocaleString()} venues`;
    tooltip.style.left = (rect.left + rect.width / 2) + 'px';
    tooltip.style.top = (rect.top - 45) + 'px';
    tooltip.classList.add('visible');

    d3.select(this).attr('opacity', 1).attr('fill', '#e8b84a');
  })
  .on('mouseleave', function(event, d) {
    tooltip.classList.remove('visible');
    const style = barStyle(d.gigs);
    d3.select(this).attr('opacity', style.opacity).attr('fill', style.color);
  });

  // --- Mobile tap support ---
  let lastTapped = null;
  bars.on('touchstart', function(event, d) {
    event.preventDefault();
    if (lastTapped === this) {
      tooltip.classList.remove('visible');
      lastTapped = null;
      return;
    }
    lastTapped = this;
    const rect = this.getBoundingClientRect();
    tooltipDate.textContent = `${MONTH_NAMES[d.month - 1]} ${d.year}`;
    tooltipStats.textContent = `${d.gigs.toLocaleString()} gigs \u00B7 ${d.bands.toLocaleString()} bands \u00B7 ${d.venues.toLocaleString()} venues`;
    tooltip.style.left = (rect.left + rect.width / 2) + 'px';
    tooltip.style.top = (rect.top - 45) + 'px';
    tooltip.classList.add('visible');
  }, { passive: false });

  // --- Era cards ---
  function monthIndex(year, month) {
    return (year - 1996) * 12 + (month - 1);
  }

  erasData.forEach((era, i) => {
    const idx = monthIndex(era.year, 1);
    const xPos = xScale(idx);
    // Alternate vertical position: upper third vs middle third
    const topPercent = (i % 2 === 0) ? 8 : 28;

    const card = document.createElement('div');
    card.className = 'era-card';
    card.style.left = xPos + 'px';
    card.style.top = topPercent + '%';

    card.innerHTML = `
      <div class="era-card-year">${era.year}</div>
      <div class="era-card-title">${era.title}</div>
      <div class="era-card-summary">${era.summary}</div>
      <ul class="era-card-events">
        ${era.events.map(e => `<li>${e}</li>`).join('')}
      </ul>
    `;

    canvas.appendChild(card);
  });

  // --- Scroll-triggered era card reveals ---
  const eraCards = document.querySelectorAll('.era-card');
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
      }
    });
  }, {
    root: container,
    threshold: 0.1
  });
  eraCards.forEach(card => observer.observe(card));

  // --- Year indicator ---
  const yearIndicator = document.getElementById('yearIndicator');
  container.addEventListener('scroll', () => {
    const scrollLeft = container.scrollLeft;
    // Find which month index is at the center of the viewport
    const centerX = scrollLeft + container.clientWidth / 2;
    const idx = Math.round(xScale.invert(centerX));
    const clampedIdx = Math.max(0, Math.min(idx, allMonths.length - 1));
    yearIndicator.textContent = allMonths[clampedIdx].year;
  });

  // --- Scroll hint: fade on first scroll ---
  const scrollHint = document.getElementById('scrollHint');
  let hintDismissed = false;
  container.addEventListener('scroll', () => {
    if (!hintDismissed && container.scrollLeft > 50) {
      scrollHint.style.opacity = '0';
      hintDismissed = true;
    }
  });

  // --- Mouse wheel → horizontal scroll ---
  container.addEventListener('wheel', (e) => {
    if (Math.abs(e.deltaY) > Math.abs(e.deltaX)) {
      e.preventDefault();
      container.scrollLeft += e.deltaY;
    }
  }, { passive: false });

})();
```

- [ ] **Step 2: Open in browser and verify**

Open `explore/timeline.html` in a browser. Verify:
- Skyline bars render across the full width, sqrt-scaled
- Year labels appear along the bottom
- Hovering a bar shows a tooltip with month/year and stats
- Era cards appear at their correct year positions
- Era cards fade in as you scroll to them
- Year indicator updates as you scroll
- Mouse wheel scrolls horizontally
- Scroll hint fades after first scroll

- [ ] **Step 3: Commit**

```bash
git add explore/timeline.html
git commit -m "Implement D3 skyline visualization and era cards for timeline page"
```

---

### Task 5: Homepage Integration

**Files:**
- Modify: `index.html:1370-1441` (replace timeline section)
- Modify: `index.html:1554-1570` (add Timeline card to explore grid)

- [ ] **Step 1: Replace the inline timeline section with a simpler link**

In `index.html`, replace the entire timeline section (lines 1370–1441) — from `<!-- ========== THROUGH THE YEARS ========== -->` through the closing `</section>` — with:

```html
<!-- ========== THROUGH THE YEARS ========== -->
<section class="section timeline-section" id="timeline">
  <div class="reveal" style="text-align:center;">
    <div class="section-label">Through the Years</div>
    <h2 class="section-heading"><span class="line">30 Years of</span><span class="line">Boston Music</span></h2>
    <hr class="section-divider" style="margin-left:auto; margin-right:auto;">
    <p style="max-width:600px; margin:1.5rem auto 2rem; color:var(--text-muted); font-size:1rem; line-height:1.7;">From the Rat to Roadrunner, from WBCN to the silence of COVID&mdash;explore the full story of Boston's local music scene.</p>
    <a href="explore/timeline.html" class="explore-card reveal" style="display:inline-block; max-width:400px; margin:0 auto;">
      <div class="explore-card-name">Explore the Timeline</div>
      <div class="explore-card-desc">A scrolling journey through 30 years of bands, venues, and the moments that shaped the scene.</div>
    </a>
  </div>
</section>
```

- [ ] **Step 2: Add Timeline card to the explore grid**

In `index.html`, find the explore grid `<div class="explore-grid">` (line 1554) and add the Timeline card as the first item, before the Radio card:

```html
      <a href="explore/timeline.html" class="explore-card reveal">
        <div class="explore-card-name">The Timeline</div>
        <div class="explore-card-desc">30 years of Boston music — from The Rat to Roadrunner, told through data and stories.</div>
      </a>
```

The existing cards shift: Radio gets `reveal-delay-1`, Venue Map gets `reveal-delay-2`, Leaderboard gets `reveal-delay-3`, and The Universe gets `reveal-delay-4` (add this class — it will need a `0.4s` delay). Or keep the existing delay structure and just let Timeline have no delay (first card, no stagger needed).

Update the existing cards' delay classes:
- Radio: `reveal reveal-delay-1`
- Venue Map: `reveal reveal-delay-2`
- Leaderboard: `reveal reveal-delay-3`
- The Universe: keep `reveal reveal-delay-3` (no need for a 5th delay tier)

- [ ] **Step 3: Verify in browser**

Open `index.html` and verify:
- The "Through the Years" section shows the new simplified content with a link to the timeline
- The explore grid now has 5 cards with Timeline as the first
- Clicking "The Timeline" card navigates to `explore/timeline.html`
- The back link on the timeline page returns to `index.html#explore`

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "Integrate timeline page into homepage — replace inline timeline, add explore card"
```

---

### Task 6: Polish & Mobile Testing

**Files:**
- Modify: `explore/timeline.html` (CSS and JS tweaks as needed)

- [ ] **Step 1: Test and fix horizontal scroll on mobile viewport**

Open `explore/timeline.html` in Chrome DevTools responsive mode (375px width). Verify:
- Touch/swipe scrolls horizontally
- Era cards don't overflow the viewport width (max-width constrains them)
- Tooltip positioning doesn't go off-screen on narrow viewports
- Bars are tappable (touch targets are adequate at 18px width)
- Year indicator is visible and doesn't overlap the back button

If tooltips go off-screen on mobile, add this to the tooltip positioning logic in the `mouseenter`/`touchstart` handlers:

```javascript
// Clamp tooltip to viewport
const tooltipRect = tooltip.getBoundingClientRect();
const maxLeft = window.innerWidth - tooltipRect.width - 10;
if (parseFloat(tooltip.style.left) > maxLeft) {
  tooltip.style.left = maxLeft + 'px';
}
if (parseFloat(tooltip.style.top) < 52) {
  tooltip.style.top = '52px';
}
```

- [ ] **Step 2: Test era card visibility across full scroll**

Scroll through the entire timeline and verify all 8 era cards:
1. 1996 — The Heyday (visible near start)
2. 2000 — The Transition
3. 2006 — The Unraveling Begins
4. 2009 — The Death of Radio
5. 2013 — Last One Standing
6. 2017 — The Archive Opens
7. 2020 — The Silence
8. 2022 — Rebuilding (visible near end)

Each should fade in smoothly as it enters the viewport. Cards should alternate vertical position (upper/middle) and not overlap each other.

- [ ] **Step 3: Verify the skyline data story**

Scroll through and confirm the visual narrative makes sense:
- 1996–2011: flat/empty skyline (pre-data era)
- 2012–2015: modest organic-era bars
- Late 2016: dramatic spike as imports begin
- 2017–mid 2019: towering skyline (peak data)
- Late 2019: cliff drop (site winding down)
- 2020: near-silence (COVID)

- [ ] **Step 4: Commit any polish fixes**

```bash
git add explore/timeline.html
git commit -m "Polish timeline page — mobile fixes and visual refinements"
```

---

## Summary

| Task | What | Key Files |
|------|------|-----------|
| 1 | Era content data | `data/eras.json` |
| 2 | Extended data export | `export_data.py`, `data/timeline-extended.json` |
| 3 | Page HTML shell & CSS | `explore/timeline.html` |
| 4 | D3 skyline + era cards JS | `explore/timeline.html` |
| 5 | Homepage integration | `index.html` |
| 6 | Polish & mobile testing | `explore/timeline.html` |
