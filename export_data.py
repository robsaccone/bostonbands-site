#!/usr/bin/env python3
"""Export BostonBands database to static JSON files for GitHub Pages."""

import json
import os
import psycopg2
import psycopg2.extras
from datetime import date, datetime
from decimal import Decimal

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

PG_CONFIG = {
    "host": "localhost",
    "port": 5433,
    "user": "postgres",
    "password": "newpassword",
    "dbname": "bostonbands",
}

# Filters for active, non-deleted records
BAND_FILTER = "(b.isdeleted = false OR b.isdeleted IS NULL)"
VENUE_FILTER = "(v.isdeleted = false OR v.isdeleted IS NULL)"
GIG_FILTER = "(g.isdeleted = false OR g.isdeleted IS NULL)"


def json_serial(obj):
    """JSON serializer for types not handled by default."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError(f"Type {type(obj)} not serializable")


def write_json(filename, data):
    path = os.path.join(DATA_DIR, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, default=json_serial, ensure_ascii=False)
    size = os.path.getsize(path)
    print(f"  {filename}: {size:,} bytes")


def export_on_this_date(cur):
    """Export gigs grouped by month-day for 'On This Date' feature."""
    print("\n=== On This Date ===")
    cur.execute(f"""
        SELECT EXTRACT(MONTH FROM g.gigdate)::int as month,
               EXTRACT(DAY FROM g.gigdate)::int as day,
               g.gigdate::date as gig_date,
               b.bandname, v.venuename, v.city,
               g.gigname,
               COALESCE(b.poprank, 0) + COALESCE(v.poprank, 0) as score
        FROM gigs g
        JOIN bands b ON g.bandid = b.bandid
        JOIN venues v ON g.venueid = v.venueid
        WHERE {GIG_FILTER} AND g.gigdate IS NOT NULL
          AND g.gigdate >= '2012-01-01' AND g.gigdate < '2021-01-01'
        ORDER BY g.gigdate
    """)

    by_day = {}
    for row in cur.fetchall():
        key = f"{row['month']:02d}-{row['day']:02d}"
        if key not in by_day:
            by_day[key] = []
        by_day[key].append({
            "date": row["gig_date"].isoformat(),
            "band": row["bandname"],
            "venue": row["venuename"],
            "city": row["city"],
            "gigname": row["gigname"],
            "score": float(row["score"]),
        })

    os.makedirs(os.path.join(DATA_DIR, "on-this-date"), exist_ok=True)
    for key, gigs in by_day.items():
        write_json(f"on-this-date/{key}.json", {
            "date": key,
            "total_gigs": len(gigs),
            "gigs": gigs,
        })
    print(f"  Total: {len(by_day)} day files")


def export_venue_leaderboard(cur):
    """Export venue rankings by gig count."""
    print("\n=== Venue Leaderboard ===")
    cur.execute(f"""
        SELECT v.venueid, v.venuename, v.city, v.state, v.address,
               v.locationlatitude as lat, v.locationlongitude as lng,
               v.facebookurl,
               COUNT(g.gigid) as gig_count,
               COUNT(DISTINCT g.bandid) as band_count,
               MIN(g.gigdate)::date as first_gig,
               MAX(g.gigdate)::date as last_gig
        FROM venues v
        JOIN gigs g ON v.venueid = g.venueid
        WHERE {VENUE_FILTER} AND {GIG_FILTER}
        GROUP BY v.venueid, v.venuename, v.city, v.state, v.address,
                 v.locationlatitude, v.locationlongitude, v.facebookurl
        HAVING COUNT(g.gigid) >= 5
        ORDER BY gig_count DESC
    """)
    venues = []
    for row in cur.fetchall():
        venues.append(dict(row))
    write_json("venue-leaderboard.json", venues)


def export_venue_map(cur):
    """Export geocoded venues as GeoJSON."""
    print("\n=== Venue Map (GeoJSON) ===")
    cur.execute(f"""
        SELECT v.venueid, v.venuename, v.city, v.state, v.address,
               v.locationlatitude::float as lat, v.locationlongitude::float as lng,
               COUNT(g.gigid) as gig_count,
               MIN(g.gigdate)::date as first_gig,
               MAX(g.gigdate)::date as last_gig
        FROM venues v
        LEFT JOIN gigs g ON v.venueid = g.venueid AND {GIG_FILTER}
        WHERE {VENUE_FILTER}
          AND v.locationlatitude IS NOT NULL AND v.locationlatitude != ''
          AND v.locationlongitude IS NOT NULL AND v.locationlongitude != ''
        GROUP BY v.venueid, v.venuename, v.city, v.state, v.address,
                 v.locationlatitude, v.locationlongitude
        ORDER BY gig_count DESC
    """)
    features = []
    for row in cur.fetchall():
        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row["lng"], row["lat"]],
            },
            "properties": {
                "id": row["venueid"],
                "name": row["venuename"],
                "city": row["city"],
                "state": row["state"],
                "address": row["address"],
                "gig_count": row["gig_count"],
                "first_gig": row["first_gig"].isoformat() if row["first_gig"] else None,
                "last_gig": row["last_gig"].isoformat() if row["last_gig"] else None,
            },
        })
    geojson = {"type": "FeatureCollection", "features": features}
    write_json("venue-map.geojson", geojson)


def export_venue_network(cur):
    """Export venue connection graph (shared bands between top venues)."""
    print("\n=== Venue Network ===")
    cur.execute(f"""
        WITH top_venues AS (
            SELECT venueid, venuename FROM venues v
            WHERE {VENUE_FILTER} AND venueid IN (
                SELECT venueid FROM gigs g WHERE {GIG_FILTER}
                GROUP BY venueid ORDER BY COUNT(*) DESC LIMIT 30
            )
        )
        SELECT v1.venuename as source, v2.venuename as target,
               COUNT(DISTINCT g1.bandid) as shared_bands
        FROM gigs g1
        JOIN gigs g2 ON g1.bandid = g2.bandid AND g1.venueid < g2.venueid
        JOIN top_venues v1 ON g1.venueid = v1.venueid
        JOIN top_venues v2 ON g2.venueid = v2.venueid
        WHERE (g1.isdeleted = false OR g1.isdeleted IS NULL)
          AND (g2.isdeleted = false OR g2.isdeleted IS NULL)
        GROUP BY v1.venuename, v2.venuename
        HAVING COUNT(DISTINCT g1.bandid) >= 10
        ORDER BY shared_bands DESC
    """)
    nodes = set()
    links = []
    for row in cur.fetchall():
        nodes.add(row["source"])
        nodes.add(row["target"])
        links.append(dict(row))
    write_json("venue-network.json", {
        "nodes": [{"id": n} for n in sorted(nodes)],
        "links": links,
    })


def export_timeline(cur):
    """Export monthly gig counts for heatmap/timeline."""
    print("\n=== Timeline ===")
    cur.execute(f"""
        SELECT EXTRACT(YEAR FROM g.gigdate)::int as year,
               EXTRACT(MONTH FROM g.gigdate)::int as month,
               COUNT(*) as gigs,
               COUNT(DISTINCT g.bandid) as bands,
               COUNT(DISTINCT g.venueid) as venues
        FROM gigs g
        WHERE {GIG_FILTER} AND g.gigdate >= '2012-01-01' AND g.gigdate < '2021-01-01'
        GROUP BY year, month ORDER BY year, month
    """)
    write_json("timeline.json", [dict(r) for r in cur.fetchall()])


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


def export_band_cards(cur):
    """Export band stats cards for notable bands."""
    print("\n=== Band Cards ===")
    cur.execute(f"""
        SELECT b.bandid, b.bandname, b.genre, b.city, b.state, b.bio,
               b.bandurl, b.facebookurl, b.twitterurl,
               b.defaultphoto, b.dateregistered::date as registered,
               COUNT(DISTINCT g.gigid) as gig_count,
               COUNT(DISTINCT g.venueid) as venue_count,
               MIN(g.gigdate)::date as first_gig,
               MAX(g.gigdate)::date as last_gig,
               (SELECT COUNT(*) FROM songs s WHERE s.bandid = b.bandid
                AND s.filename IS NOT NULL AND s.filename != '') as song_count,
               (SELECT COUNT(*) FROM bandphotos bp WHERE bp.bandid = b.bandid) as photo_count
        FROM bands b
        LEFT JOIN gigs g ON b.bandid = g.bandid AND {GIG_FILTER}
        WHERE {BAND_FILTER}
          AND (b.bio IS NOT NULL AND LENGTH(b.bio) > 20
               OR EXISTS (SELECT 1 FROM gigs g2 WHERE g2.bandid = b.bandid
                          AND (g2.isdeleted = false OR g2.isdeleted IS NULL)))
        GROUP BY b.bandid, b.bandname, b.genre, b.city, b.state, b.bio,
                 b.bandurl, b.facebookurl, b.twitterurl,
                 b.defaultphoto, b.dateregistered
        HAVING COUNT(DISTINCT g.gigid) >= 3
        ORDER BY COUNT(DISTINCT g.gigid) DESC
    """)
    bands = []
    for row in cur.fetchall():
        band = dict(row)
        # Truncate bio for index (full bio can be separate files if needed)
        if band["bio"] and len(band["bio"]) > 300:
            band["bio_short"] = band["bio"][:300] + "…"
        else:
            band["bio_short"] = band["bio"]
        bands.append(band)
    write_json("bands.json", bands)
    print(f"  {len(bands)} bands exported")


def export_genre_index(cur):
    """Export bands grouped by genre."""
    print("\n=== Genre Index ===")
    cur.execute(f"""
        SELECT b.genre, COUNT(*) as band_count
        FROM bands b
        WHERE {BAND_FILTER} AND b.genre IS NOT NULL AND b.genre != ''
        GROUP BY b.genre
        HAVING COUNT(*) >= 5
        ORDER BY band_count DESC
    """)
    write_json("genres.json", [dict(r) for r in cur.fetchall()])


def export_stats(cur):
    """Export aggregate stats for the homepage."""
    print("\n=== Site Stats ===")
    cur.execute(f"""
        SELECT
            (SELECT COUNT(*) FROM bands b WHERE {BAND_FILTER}) as total_bands,
            (SELECT COUNT(*) FROM venues v WHERE {VENUE_FILTER}) as total_venues,
            (SELECT COUNT(*) FROM gigs g WHERE {GIG_FILTER}) as total_gigs,
            (SELECT COUNT(*) FROM songs WHERE filename IS NOT NULL AND filename != '') as total_songs,
            (SELECT COUNT(*) FROM photos WHERE (isdeleted = false OR isdeleted IS NULL)) as total_photos,
            (SELECT COUNT(*) FROM reviews WHERE isapproved = true) as total_reviews,
            (SELECT MIN(gigdate)::date FROM gigs g WHERE {GIG_FILTER} AND gigdate >= '2000-01-01') as earliest_gig,
            (SELECT MAX(gigdate)::date FROM gigs g WHERE {GIG_FILTER} AND gigdate < '2025-01-01') as latest_gig
    """)
    write_json("stats.json", dict(cur.fetchone()))


def export_busiest_nights(cur):
    """Export the busiest nights in Boston music history."""
    print("\n=== Busiest Nights ===")
    cur.execute(f"""
        SELECT g.gigdate::date as date,
               COUNT(*) as gigs,
               COUNT(DISTINCT g.venueid) as venues,
               COUNT(DISTINCT g.bandid) as bands
        FROM gigs g
        WHERE {GIG_FILTER} AND g.gigdate IS NOT NULL AND g.gigdate < '2025-01-01'
        GROUP BY g.gigdate::date
        ORDER BY gigs DESC
        LIMIT 50
    """)
    write_json("busiest-nights.json", [dict(r) for r in cur.fetchall()])


def main():
    print("Connecting to PostgreSQL...")
    conn = psycopg2.connect(**PG_CONFIG, cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()

    export_stats(cur)
    export_on_this_date(cur)
    export_venue_leaderboard(cur)
    export_venue_map(cur)
    export_venue_network(cur)
    export_timeline(cur)
    export_timeline_extended(cur)
    export_band_cards(cur)
    export_genre_index(cur)
    export_busiest_nights(cur)

    cur.close()
    conn.close()
    print("\nAll exports complete!")


if __name__ == "__main__":
    main()
