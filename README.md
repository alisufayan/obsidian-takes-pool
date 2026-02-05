**obsidian-takes-pool**


I write daily notes in Obsidian with a "Takes of the day" section random thoughts, insights, things I learned. But they were scattered across 100+ files.
So I wrote this script to pull all those takes into one pool file. It handles multi-line takes, skips short stuff, and adds Obsidian links so I can trace back to the original day.

**Works on & Dependency:** Linux, Mac, Windows (uses standard Python + glob patterns)
**Date formate must be:** Y/MM - MMMM/ddd DD MMM; 2026/02 - February/Thu 05 Feb


**What it does:**
- Extracts takes from `### The Takes of the day:` sections
- Joins multi-line takes into single entries
- Filters out hashtags and one-word bullets
- Sorts chronologically
- Appends `[[Day Month]]` links to each take
** Important:** This APPENDS to the pool file. Clear it first to avoid dupes:
```bash
truncate -s 0 "Daily Notes/The daily takes pool.md"
Or just use this alias:
alias takes='truncate -s 0 "Daily Notes/The daily takes pool.md" && python3 extract_daily_takes.py'
