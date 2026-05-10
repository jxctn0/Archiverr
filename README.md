# Archiverr

A modular, cross-platform music archival framework designed to preserve your music library independently of streaming services.

Archiverr ingests Apple Music libraries, resolves metadata across multiple providers, downloads archival-quality audio, verifies integrity, and builds a self-healing local music archive.

---

# Philosophy

Archiverr is built around three ideas:

```text
services are temporary
metadata is repairable
hashes are forever
```

Streaming platforms change.
APIs disappear.
Links die.
Licensing changes.

Archiverr separates:

* canonical identity
* metadata
* download sources
* local files
* verification
* manifests

This allows your library to survive:

* service shutdowns
* metadata drift
* dead URLs
* file corruption
* future migrations
* platform lock-in

---

# Features

## Library Ingestion

Supports:

* Apple Music `Library.xml`
* playlist `.txt` files
* future extensible importers

Extracts:

* title
* artist
* album
* year
* play counts
* Apple IDs
* local paths
* embedded metadata

---

## Canonical Track Identity

Archiverr creates deterministic internal track IDs.

Never rely solely on:

* Spotify IDs
* YouTube URLs
* Apple Music IDs

Instead:

```text
normalized metadata
+ duration
+ hashing
→ canonical identity
```

This enables:

* deduplication
* source replacement
* reproducibility
* long-term portability

---

# Metadata Resolution

## Spotify

Used for:

* broad search coverage
* ISRC extraction
* artist normalization
* release metadata

Stores:

* Spotify ID
* URI
* URL
* album ID
* artist ID
* popularity
* release data

---

## MusicBrainz

Used for:

* canonical metadata verification
* release relationships
* MusicBrainz IDs
* cover art references

Supports:

* local database dumps
* local metadata caches
* live API fallback

---

## YouTube

Used for:

* official audio discovery
* source fallback
* download acquisition

Archiverr attempts to prioritize:

* official uploads
* topic channels
* artist channels
* VEVO uploads

Rejects:

* live recordings
* lyric videos
* nightcore
* unofficial remasters

---

# Download System

Powered by:

* yt-dlp
* ffmpeg

Supports:

* FLAC
* Opus
* AAC
* MP3

Output structure:

```text
{library}/{artist}/{album}/{track}.{ext}
```

Example:

```text
Archive/
└── My Chemical Romance/
    └── The Black Parade/
        ├── Welcome to the Black Parade.flac
        ├── manifest.json
        ├── cover.jpg
        └── metadata.json
```

---

# Metadata Warehouse

Archiverr stores extensive metadata locally.

## Stored Metadata

### Core Metadata

* title
* artist
* album
* genre
* composer
* year
* duration

### Apple Metadata

* Apple Music ID
* iTunes ID
* Persistent ID
* play counts
* skip counts
* dates added

### Spotify Metadata

* Spotify ID
* URI
* URL
* album IDs
* artist IDs
* popularity

### MusicBrainz Metadata

* recording MBID
* release MBID
* artist MBID
* work MBID

### Industry IDs

* ISRC
* UPC
* EAN

### YouTube Metadata

* video ID
* channel ID
* upload date
* view count

### Audio Metadata

* codec
* bitrate
* channels
* sample rate
* hashes

### Fingerprinting

* Chromaprint
* AcoustID

---

# Analytics

Archiverr can analyze imported libraries before downloading.

## Included Analysis

* year distributions
* genre distributions
* artist distributions
* metadata quality
* duplicate detection
* outlier detection

## Heatmaps

Generate:

* release year heatmaps
* genre timelines
* artist activity charts

Example:

```text
2004 ████████
2005 ███████████
2006 ███████████████
2007 █████████████
```

---

# Self-Healing Design

Archiverr treats download sources as replaceable.

Metadata remains independent from:

* YouTube
* Spotify
* Apple Music

If a source disappears:

* metadata survives
* manifests survive
* hashes survive
* alternate sources can replace files later

---

# Verification

Every downloaded file can be verified using:

* SHA256 hashes
* BLAKE3 hashes
* audio fingerprints
* metadata reconciliation

This enables:

* corruption detection
* duplicate detection
* archive auditing
* future migrations

---

# Architecture

```text
Apple Music Library
        ↓
Metadata Parser
        ↓
Canonical Identity Generator
        ↓
Spotify Resolution
        ↓
ISRC Extraction
        ↓
MusicBrainz Verification
        ↓
Metadata Warehouse
        ↓
Source Discovery
        ↓
Download Scheduler
        ↓
yt-dlp Download Workers
        ↓
Verification Layer
        ↓
Tagging + Artwork
        ↓
Manifest Generation
        ↓
Final Archive
```

---

# Project Structure

```text
archiverr/
│
├── archiverr/
│   ├── core/
│   ├── parser/
│   ├── analysis/
│   ├── metadata/
│   ├── database/
│   ├── download/
│   ├── tagging/
│   ├── manifests/
│   ├── workers/
│   ├── cli/
│   └── api/
│
├── tests/
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

# Installation

## Requirements

* Python 3.11+
* ffmpeg
* yt-dlp

---

## Linux

```bash
sudo apt install ffmpeg
pip install -r requirements.txt
```

---

## macOS

```bash
brew install ffmpeg
pip install -r requirements.txt
```

---

## Windows

Install:

* Python 3.11+
* ffmpeg

Then:

```powershell
pip install -r requirements.txt
```

---

# Environment Variables

```bash
export SPOTIFY_CLIENT_ID="your_client_id"
export SPOTIFY_CLIENT_SECRET="your_client_secret"
```

---

# Usage

## Import Apple Music Library

```bash
python -m archiverr.cli.app ingest ~/Music/Library.xml
```

---

## Download Archive

```bash
python -m archiverr.cli.app archive \
  ~/Music/Library.xml \
  --output ~/Archive
```

---

## Analyze Library

```bash
python -m archiverr.cli.app analyze ~/Music/Library.xml
```

---

# Recommended Storage Strategy

## Archive Master

Use:

```text
FLAC
```

---

## Portable Copies

Generate:

```text
Opus
AAC
```

from archival masters.

---

# Recommended Deployment

## Suggested Hardware

Ideal:

* NAS
* RAID/ZFS storage
* SSD metadata cache
* large HDD archive pool

---

## Suggested Filesystem

Recommended:

* ZFS
* Btrfs

Benefits:

* checksums
* snapshots
* corruption detection
* compression

---

# Database Design

Archiverr stores:

* canonical track identities
* service IDs
* hashes
* manifests
* metadata versions
* source history

This allows complete reconstruction later.

---

# Future Features

## Planned Metadata Sources

* Discogs
* Deezer
* TIDAL
* Qobuz
* Last.fm
* Bandcamp

---

## Planned Download Sources

* Soulseek
* torrents
* Usenet
* local CD rips

---

## Planned Features

* web UI
* distributed workers
* metadata repair jobs
* waveform matching
* duplicate clustering
* archive health checks
* automatic source upgrades

---

# Legal Notes

Users are responsible for complying with:

* local copyright laws
* platform terms of service
* licensing restrictions

Archiverr is intended for:

* personal archival
* metadata preservation
* library migration
* interoperability

---

# Recommended Workflow

```text
1. Import Apple Music library
2. Analyze metadata
3. Detect outliers
4. Resolve Spotify metadata
5. Extract ISRCs
6. Verify via MusicBrainz
7. Build local metadata warehouse
8. Discover sources
9. Download audio
10. Verify integrity
11. Generate manifests
12. Store redundant backups
```

---

# Core Design Principles

## Metadata First

Downloads are replaceable.
Metadata is the archive.

---

## Deterministic Identity

Track identities should survive service shutdowns.

---

## Reproducibility

Every archive should be reconstructable.

---

## Extensibility

Sources and metadata providers should be swappable.

---

# Contributing

Contributions are welcome.

Areas especially useful:

* metadata reconciliation
* async optimization
* additional source providers
* fingerprinting
* archival verification
* UI development
* testing
* packaging

---

# License

Recommended:

* MIT
* GPLv3

---

# Acknowledgements

Built using:

* Spotify API
* MusicBrainz
* yt-dlp
* ffmpeg
* mutagen
* AcoustID
* Chromaprint

---

# Final Goal

Archiverr aims to create:

```text
a permanent, service-independent,
reproducible music archive
```

that remains usable decades into the future regardless of:

* streaming services
* licensing changes
* platform shutdowns
* metadata drift
* source availability.
