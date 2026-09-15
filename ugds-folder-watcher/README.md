# UGDS Patient Outreach Folder Watcher

A standalone, lightweight Windows/Python daemon that monitors legacy hospital folder tracker `.txt` files, extracts patient phone numbers, filters out landlines, prevents duplicates, and sends automated SMS survey links via **Arkesel**.

---

## 🚀 Quick Start (Hospital PC)

### 1. Configure Settings
Open `.env` in Notepad:
```ini
ARKESEL_API_KEY=your_real_arkesel_api_key_here
ARKESEL_SENDER_ID=UGDS
DRY_RUN=False

# Folder where your folder tracker .txt files appear
WATCH_FOLDER=./incoming_files

# Survey link sent to patients
SURVEY_BASE_URL=https://ugds-customer-experience.vercel.app/feedback
```
*(Keep `DRY_RUN=True` while testing so it won't consume SMS credits!)*

### 2. Run the Watcher
- Simply double-click `run_watcher.bat`  
  *OR*  
- From PowerShell / Command Prompt:
  ```cmd
  python watcher.py
  ```

---

## ⚙️ How It Works
1. **File Watcher**: Scans `WATCH_FOLDER` (or tails an appended file).
2. **Parser**: Handles `'`-delimited tracker lines:
   ```
   'MR-1A-A1-1'K/13 5622'SINTIM'YABBEY'YSINT12011964-1'0273920899 0549554089'KASOA'ESTHER SARBENG'
   ```
3. **Ghanaian Phone Cleaning**:
   - Accepts MTN (`024, 054, 055, 059`), Telecel (`020, 050`), AT (`027, 057, 026, 056`), Glo (`028`).
   - Normalizes to international format `233XXXXXXXXX`.
   - Rejects landlines (`030...`) and invalid inputs.
4. **Duplicate Ledger (`sent_history.db`)**:
   - Tracks sent messages in a local SQLite database.
   - Prevents sending to the same folder or phone within `COOLDOWN_DAYS` (default 7 days).
5. **Arkesel API v2**:
   - Dispatches SMS directly to `https://sms.arkesel.com/api/v2/sms/send`.

---

## 🛠️ CLI Options
- Run once and exit:
  ```cmd
  python watcher.py --once
  ```
- Process a specific single file:
  ```cmd
  python watcher.py --process-file "C:\path\to\tracker.txt"
  ```
- Force full re-processing (bypassing checkpoints):
  ```cmd
  python watcher.py --force-full --once
  ```
