# Daily Ranking System Documentation

## Overview
The system now generates daily ranking files with simplified timestamps (YYMMDD format only) that get updated each time a new contest is added to the same day.

## File Naming Convention

### Contest Files
- `contests_YYMMDD.yml` - Contains all contests for a specific date
- Multiple contests on the same day append to the same file

### Daily Ranking Files  
- `ranking_YYMMDD.txt` - Daily ranking for specific date (YYMMDD format only)
- **Updated automatically** each time a contest is added to that day
- **Overwrites** the existing file for the same day

### Global Ranking Files
- User-specified filename (e.g., `global_ranking.txt`)
- **Saved in results directory**: `results/global_ranking.txt`
- **Automatic backups**: Previous versions saved to `results/bkp/` with full timestamp
- Contains comprehensive statistics from all contest files
- Generated on-demand using `--update-global` option

## Workflow Example

1. **Run First Contest of the Day:**
   ```bash
   python comvida.py --dist 4 --colonies 0 1
   ```
   - Creates: `results/contests_251005.yml`
   - Creates: `results/ranking_251005.txt`

2. **Run Second Contest Same Day:**
   ```bash  
   python comvida.py --dist 3 --colonies 2 4
   ```
   - Appends to: `results/contests_251005.yml`
   - **Updates**: `results/ranking_251005.txt` (overwrites with new stats)

3. **Generate Global Ranking:**
   ```bash
   python comvida.py --update-global global_ranking.txt
   ```
   - Processes all `contests_*.yml` files
   - Creates/updates: `results/global_ranking.txt`

## File Structure Example
```
results/
├── contests_251004.yml            # Yesterday's contests (Oct 4, 2025)
├── contests_251005.yml            # Today's contests (Oct 5, 2025)
├── ranking_251004.txt             # Yesterday's ranking
├── ranking_251005.txt             # Today's ranking (updated with each contest)
├── global_ranking.txt             # Global ranking (all-time)
├── season1_rankings.txt           # Custom global ranking file
└── bkp/                           # Backup directory
    ├── global_ranking_251005_114710.txt    # Backup with full timestamp
    └── season1_rankings_251005_114739.txt  # Backup of custom ranking
```
