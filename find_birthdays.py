import re
import glob

matches = []
seen_folders = set()

for filename in ['user_batch_531.txt', 'user_batch_533.txt']:
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith('<')]
            print(f"{filename}: {len(lines)} records")
            for line in lines:
                m = re.search(r'([0-3]\d)([0-1]\d)(\d{4})-\d', line)
                if m:
                    day, month, year = m.group(1), m.group(2), m.group(3)
                    if day == '15' and month == '09':
                        parts = [p.strip() for p in line.split("'") if p.strip()]
                        folder = parts[1] if len(parts) > 1 else line
                        if folder not in seen_folders:
                            seen_folders.add(folder)
                            matches.append((day, month, year, parts, line))
    except Exception as e:
        print(f"Error reading {filename}: {e}")

print(f"\n=== Found {len(matches)} Celebrants for September 15 ===")
for day, month, year, parts, line in matches:
    print("--------------------------------------------------")
    print(f"DOB: {day}/09/{year} (Age {2026 - int(year)})")
    print(f"Parts: {parts}")
    print(f"Raw: {line}")

