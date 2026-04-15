# Eli Researcher

**Autonomous Intelligence Gathering for Developers & Security Teams**

Researcher continuously monitors 30+ RSS feeds across security, AI, cloud, and developer ecosystems. It detects opportunities, identifies threats, and generates daily digests — all running as a lightweight daemon.

## What It Does

- **News Scanning** — 30+ curated RSS feeds across 8 categories (security, AI/ML, cloud, DevOps, Web3, startup, open source, enterprise)
- **Opportunity Detection** — Identifies skill-relevant opportunities, security service needs, and emerging trends
- **System Improvement** — Analyzes your own codebase and suggests improvements
- **Research Journal** — Maintains a structured log of all findings
- **Daemon Mode** — Run it in the background with configurable scan intervals

## Quick Start

```bash
git clone https://github.com/thenot-lab/eli-researcher.git
cd eli-researcher
pip install -r requirements.txt

# Scan news feeds
python researcher.py --scan

# Detect opportunities
python researcher.py --opportunities

# Generate daily digest
python researcher.py --digest

# Full research cycle
python researcher.py --full-cycle

# Run as daemon (background)
python researcher.py --daemon
```

## Architecture

| Component | Purpose |
|-----------|---------|
| `researcher.py` | Core engine — NewsScanner, OpportunityDetector, SystemImprover, ResearchPipeline |
| `scheduler.py` | Task scheduler — hourly news, 6-hour opportunities, daily improvements, weekly synthesis |
| `feeds.json` | 30+ RSS feeds with priority keywords and categories |

## Scan Intervals (Daemon Mode)

- **Hourly** — News feed scanning
- **Every 6 hours** — Opportunity detection
- **Daily** — System improvement analysis
- **Weekly** — Full synthesis and trend report

## Built By

[Dominion Labs](https://dominionlabs.dev) — Intelligence that works while you sleep.

## License

MIT
