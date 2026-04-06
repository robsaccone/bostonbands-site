# BostonBands Archive — Roadmap & Ideas

## Assets Available
- **4,353 song files** (mp3/m4a) with metadata (title, artist, duration)
- **Photos** — band photos, venue photos, gig photos, promo images
- **SQL database** — 13,564 bands, 6,783 venues, 36,001 gigs, 8,028 members with full relational data

---

## Music Player / Radio
- **"BostonBands Radio"** — shuffle player that randomly picks tracks. Hit play and discover something you've never heard.
- **Curated playlists** — "First uploads (2000-2005)", "Most prolific bands", "One-song wonders" (bands that only uploaded a single track)
- **Song-of-the-day** — rotate a featured track based on the date. Zero maintenance once built.

## Photo Showcase
- **Infinite scroll gallery** — lazy-load from the full photo archive, filterable by band/venue.
- **"Random band" button** — show a random band's photo + name + stats. Addictive, simple to build.
- **Before & after** — venue photos paired with Google Street View of the same address today. Many of these places are gone.

## Data-Driven Features
- **"On this date"** — pull gig history by today's date. "On March 28, 2015: 12 bands played 8 venues across Boston." Changes daily.
- **Venue leaderboard** — sortable table of top venues by gig count. Middle East's 4,763 gigs is a staggering number.
- **Band stats cards** — pick 50-100 notable bands, generate a card for each with photo, gig count, venues played, years active. Like baseball cards.
- **The web of music** — which bands played the same venues? Which venues hosted the most genres? Could be a simple table or a visual graph.
- **Timeline heatmap** — how many gigs per month, per year? Shows the rise and peak of the scene visually.

## Search & Explore
- **Explore page** with search over band/venue data (SQLite + lightweight API, or client-side JSON)
- **Featured band/venue rotation** on homepage — swap highlights cards weekly via a simple JSON file

## Community
- **"I Was There" guestbook** — let people submit memories tied to a band or venue
- **Band alumni network** — map the web of musicians across bands using the BandMembers table

---

## Technical Notes
- Song and photo files recovered from Azure Blob Storage to local backup
- Database can be exported from SQL Server to SQLite for lightweight querying
- Current site is vanilla HTML/CSS/JS — can add Astro or similar if dynamic features warrant it
- Hosting on GitHub Pages (free), media files would need separate hosting (R2, S3, or similar)
