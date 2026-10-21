#!/usr/bin/env python3
import datetime
import subprocess
import sys

# uses notesmd-cli to automatically add a new daily note when triggered via launchd

def main():
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    tomorrow = today + datetime.timedelta(days=1)

    # Format dates
    date_str = today.strftime("%Y-%m-%d")
    yesterday_str = yesterday.strftime("%Y-%m-%d")
    tomorrow_str = tomorrow.strftime("%Y-%m-%d")

    # Format header date: "Saturday, September 19th, 2026"
    day_num = today.day
    if 11 <= day_num <= 13:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day_num % 10, "th")

    formatted_header_date = today.strftime(f"%A, %B {day_num}{suffix}, %Y")

    # Build note body content
    note_content = f"""---
file_icon: ✏️
tags:
    - log
    - 
---
⇦  [[{yesterday_str}]] | {date_str} | [[{tomorrow_str}]]  ⇨ 
# {formatted_header_date}
 
 
"""

    # Destination path relative to vault root
    note_path = f"01_daily_operations/log/{date_str}.md"

    # Execute notesmd-cli command to create note
    cmd = ["/opt/homebrew/bin/notesmd-cli", "create", note_path, "-c", note_content]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Successfully created note: {note_path}")
        if result.stdout:
            print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error executing notesmd CLI: {e}", file=sys.stderr)
        if e.stderr:
            print(e.stderr, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
