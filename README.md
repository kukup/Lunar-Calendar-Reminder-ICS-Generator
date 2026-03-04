# Lunar Calendar Reminder ICS Generator

Generate a public `.ics` calendar feed containing reminders for the **1st (初一)** and **15th (十五)** day of each Chinese lunar month.

The generated feed is designed for subscription from:

- Apple Calendar
- Google Calendar
- Microsoft Outlook

## Features

- Direct lunar-to-Gregorian conversion using `lunardate`
- Bilingual event titles
- Configurable title format
- Configurable reminders with support for multiple alarms
- Stable deterministic UIDs to avoid duplicate subscribed events
- Timezone-neutral all-day ICS events
- GitHub Pages-friendly output
- Optional GitHub Actions automation

## Project Structure

```text
.
├── .github/workflows/generate.yml
├── generate.py
├── lunar_reminder.ics
├── pyproject.toml
├── README.md
├── src/lunar_calendar/
│   ├── __init__.py
│   ├── config.py
│   └── generator.py
└── uv.lock
```

## Requirements

- Python 3.10+
- `uv` installed: https://docs.astral.sh/uv/

## Quick Start

### 1. Install dependencies

```bash
uv sync
```

### 2. Generate the calendar feed

```bash
uv run python generate.py
```

This writes the ICS file to:

- `lunar_reminder.ics`

Expected console output:

```text
Generated 544 events -> lunar_reminder.ics
```

## Configuration

Edit [src/lunar_calendar/config.py](src/lunar_calendar/config.py) to customize behavior.

### Available settings

- `START_YEAR` – first lunar year to generate
- `END_YEAR` – last lunar year to generate
- `TITLE_FORMAT` – bilingual title style
- `REMINDERS` – list of reminder offsets in hours before the event
- `INCLUDE_LEAP_MONTHS` – include leap lunar months when available
- `CALENDAR_NAME` – feed name shown by calendar apps
- `EVENT_DESCRIPTION` – event description text
- `ALARM_DESCRIPTION` – reminder text shown by clients

### Example

```python
START_YEAR = 2024
END_YEAR = 2045

TITLE_FORMAT = "zh-first"
REMINDERS = [9]
INCLUDE_LEAP_MONTHS = True
```

### Title format options

- `zh-first` → `初一 · Lunar Month Start`
- `en-first` → `Lunar Month Start · 初一`
- `parentheses` → `Lunar Month Start (初一)`

### Reminder examples

- `REMINDERS = [1]` → 1 hour before
- `REMINDERS = [9]` → 9 hours before
- `REMINDERS = [24]` → 1 day before
- `REMINDERS = [9, 24]` → multiple alarms per event

## How It Works

The generator does **not** scan every Gregorian day.

Instead it:

1. Iterates through lunar years and months
2. Converts lunar day `1` and `15` directly to Gregorian dates
3. Builds a timezone-neutral all-day ICS event
4. Applies deterministic UIDs and reminder alarms
5. Writes a single public `.ics` file

This keeps generation simple, fast, and deterministic.

## Event Format

Each event includes:

- `UID`
- `SUMMARY`
- `DTSTART;VALUE=DATE`
- `DESCRIPTION`
- one or more `VALARM` blocks

Example:

```ics
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

## Stable UIDs

UIDs are deterministic so subscribed calendars do not duplicate events after updates.

- Regular month: `lunar-{year}-{month}-{day}@lunar-calendar`
- Leap month: `lunar-{year}-{month}-leap-{day}@lunar-calendar`

## Publish with GitHub Pages

After pushing this repository to GitHub:

1. Open the repository on GitHub
2. Go to **Settings** → **Pages**
3. Under **Build and deployment**, choose:
	- **Source**: `Deploy from a branch`
	- **Branch**: `main`
	- **Folder**: `/ (root)`

Your public ICS URL will be:

```text
https://<username>.github.io/<repository-name>/lunar_reminder.ics
```

For this repository, it should be:

```text
https://kukup.github.io/Lunar-Calendar-Reminder-ICS-Generator/lunar_reminder.ics
```

## GitHub Actions Automation

The workflow file [.github/workflows/generate.yml](.github/workflows/generate.yml) regenerates the calendar on demand and once per year.

Workflow behavior:

- installs `uv`
- syncs dependencies
- runs `uv run python generate.py`
- commits updated `lunar_reminder.ics`
- pushes changes back to `main`

To allow workflow commits:

1. Open **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select **Read and write permissions**
3. Save changes

You can also run the workflow manually from the **Actions** tab.

## Local Update Workflow

Whenever you change configuration or want to refresh the feed:

```bash
uv run python generate.py
git add lunar_reminder.ics src/lunar_calendar/config.py README.md
git commit -m "Update lunar calendar feed"
git push
```

## Subscribe in Calendar Apps

### Apple Calendar

1. Open **Calendar**
2. Go to **File** → **New Calendar Subscription** or use iPhone/iPad Calendar subscription settings
3. Paste the public ICS URL
4. Save

### Google Calendar

1. Open Google Calendar
2. Next to **Other calendars**, choose **From URL**
3. Paste the public ICS URL
4. Add calendar

### Microsoft Outlook

1. Open Outlook
2. Add calendar from internet / subscribe from web
3. Paste the public ICS URL
4. Save

## Development Notes

- Events are all-day and intentionally timezone-neutral to avoid iOS day shifting
- Leap months are included by default
- The generated event count depends on the configured year range and leap months

## Troubleshooting

### `uv run python generate.py` fails

- run `uv sync` again
- confirm Python version is 3.10+

### `git push` asks for authentication

- sign in through Git Credential Manager when prompted, or
- configure a GitHub personal access token, or
- configure SSH authentication

### GitHub Pages URL returns 404

- verify Pages is enabled on `main` root
- confirm `lunar_reminder.ics` exists in the repository root
- wait a minute for the first Pages deployment to complete

## License

Add a license if you plan to distribute the project publicly.
