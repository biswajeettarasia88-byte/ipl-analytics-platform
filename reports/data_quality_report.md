# Data Quality & Profiling Report

## 1. Overview
- **Total Matches Profiled**: 1243
- **Total Innings**: 2514
- **Total Deliveries**: 295732
- **Unique Teams**: 19
- **Unique Venues**: 60
- **Unique Players**: 966

## 2. Issues Identified

### [CRITICAL] Malformed Records
- Found 0 malformed JSON files.

### [CRITICAL] Suspicious Values
- Found 0 suspicious deliveries (e.g. negative runs or >8 runs).

### [WARNING] Missing Values
- **Missing City**: 51 matches
- **Missing Winner/Result**: 0 matches
- **Missing Toss Info**: 0 matches

### [WARNING] Inconsistent Team Names
The following teams likely have legacy/duplicate names:
- Chennai Super Kings
- Deccan Chargers
- Delhi Capitals
- Delhi Daredevils
- Gujarat Lions
- Gujarat Titans
- Kings XI Punjab
- Kochi Tuskers Kerala
- Kolkata Knight Riders
- Lucknow Super Giants
- Mumbai Indians
- Pune Warriors
- Punjab Kings
- Rajasthan Royals
- Rising Pune Supergiant
- Rising Pune Supergiants
- Royal Challengers Bangalore
- Royal Challengers Bengaluru
- Sunrisers Hyderabad

### [INFORMATIONAL] Inconsistent Venue Names
Many venues have multiple naming conventions (e.g., 'M Chinnaswamy Stadium' vs 'M.Chinnaswamy Stadium').
Total distinct venues parsed: 60