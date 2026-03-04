# Lunar Calendar Reminder ICS Generator (Optimized + Bilingual + Configurable)

## Objective

Build a lightweight system that generates a public **`.ics` calendar feed** containing reminders on the **1st (初一)** and **15th (十五)** days of every Chinese lunar month.

The system will:

* generate events **20–50 years into the future**
* include **bilingual titles (Chinese + English)**
* allow **configurable reminder times**
* be hosted publicly using GitHub Pages on GitHub
* use **Python with the `uv` package manager**

Users will be able to subscribe using:

* Apple Calendar
* Google Calendar
* Microsoft Outlook

---

# System Architecture

```
Python Generator
     │
     ▼
lunar_reminder.ics
     │
     ▼
GitHub Repository
     │
     ▼
GitHub Pages
     │
     ▼
Public ICS Feed
     │
     ▼
Calendar Apps
```

Optional automation:

```
GitHub Actions
      │
      ▼
Run generator
      │
      ▼
Update ICS file
```

---

# Core Design Principle

The generator **must not scan every Gregorian date**.

Instead:

1. Iterate through **lunar months**
2. Convert lunar dates directly:

```
LunarDate(year, month, 1)
LunarDate(year, month, 15)
```

3. Convert them to Gregorian dates
4. Generate events

Benefits:

* ~30× faster
* cleaner code
* deterministic output

---

# Functional Requirements

## Events Generated

For each lunar month:

| Lunar Day | Event Title            |
| --------- | ---------------------- |
| 1         | 初一 / Lunar Month Start |
| 15        | 十五 / Full Moon Day     |

---

# Bilingual Event Titles

Event titles must include both languages.

Format:

```
初一 · Lunar Month Start
十五 · Full Moon Day
```

Alternative format (configurable):

```
Lunar Month Start (初一)
Full Moon Day (十五)
```

Implementation should allow switching between formats via configuration.

---

# Calendar Range

Default:

```
START_YEAR = 2024
END_YEAR = 2045
```

Configurable via settings file.

Expected events per year:

```
~24–26 events
```

---

# Reminder Configuration

Reminders should be configurable.

Example configuration:

```
REMINDER_HOURS_BEFORE = 9
```

Meaning:

```
Reminder triggers 9 hours before the event
```

ICS alarm format:

```
BEGIN:VALARM
TRIGGER:-PT9H
ACTION:DISPLAY
DESCRIPTION:Lunar calendar reminder
END:VALARM
```

Possible values:

| Value | Meaning       |
| ----- | ------------- |
| 1     | 1 hour before |
| 9     | default       |
| 24    | 1 day before  |

The configuration must allow future support for **multiple reminders**.

Example:

```
REMINDERS = [9, 24]
```

---

# Stable UID Requirement

Each event must have a **deterministic UID** to prevent duplicate events when the calendar updates.

Format:

```
lunar-{year}-{month}-{day}@lunar-calendar
```

Example:

```
lunar-2026-8-15@lunar-calendar
```

---

# Timezone-Safe All-Day Events

Use timezone-neutral all-day events:

```
DTSTART;VALUE=DATE:YYYYMMDD
```

Do **not include timezones**.

This prevents day shifting in iOS.

---

# Python Implementation

## Package Manager

Use **`uv`** for dependency management and project execution.

Reference tool:

uv

Advantages:

* extremely fast
* modern Python project manager
* deterministic environments

---

# Project Initialization

Create project:

```
uv init lunar-calendar-ics
```

Install dependencies:

```
uv add lunardate
uv add ics
```

---

# Project Structure

```
lunar-calendar-ics/
│
├── pyproject.toml
├── uv.lock
│
├── src/
│   └── lunar_calendar/
│       ├── __init__.py
│       ├── generator.py
│       └── config.py
│
├── generate.py
├── lunar_reminder.ics
│
├── README.md
│
└── .github/
    └── workflows/
        └── generate.yml
```

---

# Configuration Module

Create:

```
src/lunar_calendar/config.py
```

Example:

```python
START_YEAR = 2024
END_YEAR = 2045

TITLE_FORMAT = "zh-first"

REMINDERS = [9]
```

Title format options:

```
zh-first
en-first
parentheses
```

---

# Generator Responsibilities

Create:

```
src/lunar_calendar/generator.py
```

Responsibilities:

1. Iterate through lunar years
2. Convert lunar days → Gregorian dates
3. Generate bilingual titles
4. Apply reminder configuration
5. Create stable UID
6. Export `.ics`

---

# Example Core Algorithm

```python
from lunardate import LunarDate
from datetime import date
from ics import Calendar, Event

calendar = Calendar()

for year in range(START_YEAR, END_YEAR + 1):

    for month in range(1, 13):

        for day in [1, 15]:

            try:

                lunar = LunarDate(year, month, day)
                solar = lunar.toSolarDate()

                event = Event()

                event.name = build_title(day)

                event.begin = solar
                event.make_all_day()

                event.uid = f"lunar-{year}-{month}-{day}@lunar-calendar"

                add_reminders(event)

                calendar.events.add(event)

            except ValueError:
                pass
```

---

# Title Builder

Example implementation:

```
def build_title(day):
    if day == 1:
        zh = "初一"
        en = "Lunar Month Start"
    else:
        zh = "十五"
        en = "Full Moon Day"

    if TITLE_FORMAT == "zh-first":
        return f"{zh} · {en}"

    if TITLE_FORMAT == "en-first":
        return f"{en} · {zh}"

    if TITLE_FORMAT == "parentheses":
        return f"{en} ({zh})"
```

---

# Reminder Generator

```
def add_reminders(event):

    for hours in REMINDERS:

        alarm = DisplayAlarm(
            trigger=timedelta(hours=-hours),
            display_text="Lunar calendar reminder"
        )

        event.alarms.append(alarm)
```

---

# Main Entry Script

Create:

```
generate.py
```

Purpose:

* run generator
* export `.ics`

Example:

```
uv run python generate.py
```

Output:

```
lunar_reminder.ics
```

---

# GitHub Pages Hosting

Enable GitHub Pages:

```
Repository Settings
→ Pages
→ Deploy from branch
→ main
→ root
```

Public feed:

```
https://<username>.github.io/lunar-calendar-ics/lunar_reminder.ics
```

---

# GitHub Actions Automation

Create workflow:

```
.github/workflows/generate.yml
```

Example:

```yaml
name: Generate Lunar ICS

on:
  workflow_dispatch:
  schedule:
    - cron: "0 0 1 1 *"

jobs:
  generate:

    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: astral-sh/setup-uv@v3

      - run: uv sync
      - run: uv run python generate.py

      - name: Commit ICS
        run: |
          git config --global user.name github-actions
          git config --global user.email actions@github.com
          git add lunar_reminder.ics
          git commit -m "Update lunar calendar" || echo "No change"
          git push
```

---

# Example Output Event

```
BEGIN:VEVENT
UID:lunar-2026-8-15@lunar-calendar
SUMMARY:十五 · Full Moon Day
DTSTART;VALUE=DATE:20260402
DESCRIPTION:Chinese Lunar Calendar Reminder
BEGIN:VALARM
TRIGGER:-PT9H
ACTION:DISPLAY
DESCRIPTION:Lunar calendar reminder
END:VALARM
END:VEVENT
```

---

# Testing

Subscribe from Apple Calendar:

```
Settings → Calendar → Accounts → Add Subscription Calendar
```

Paste:

```
https://<username>.github.io/lunar-calendar-ics/lunar_reminder.ics
```

Verify:

* bilingual titles appear
* reminders trigger
* no duplicate events appear after updates

---

# Acceptance Criteria

Implementation is complete when:

* `.ics` file generates without errors
* bilingual titles appear correctly
* reminders follow configuration
* stable UID prevents duplicates
* GitHub Pages serves the calendar
* Apple Calendar subscription works

---
