from __future__ import annotations

from datetime import date, datetime, timedelta
from pathlib import Path

from lunardate import LunarDate

from .config import (
    ALARM_DESCRIPTION,
    CALENDAR_NAME,
    END_YEAR,
    EVENT_DESCRIPTION,
    INCLUDE_LEAP_MONTHS,
    REMINDERS,
    START_YEAR,
    TITLE_FORMAT,
)


def build_title(day: int, title_format: str = TITLE_FORMAT) -> str:
    if day == 1:
        zh, en = "初一", "Lunar Month Start"
    elif day == 15:
        zh, en = "十五", "Full Moon Day"
    else:
        raise ValueError(f"Unsupported lunar day: {day}")

    if title_format == "zh-first":
        return f"{zh} · {en}"
    if title_format == "en-first":
        return f"{en} · {zh}"
    if title_format == "parentheses":
        return f"{en} ({zh})"

    raise ValueError(f"Invalid TITLE_FORMAT: {title_format}")


def build_uid(year: int, month: int, day: int, is_leap_month: bool = False) -> str:
    if is_leap_month:
        return f"lunar-{year}-{month}-leap-{day}@lunar-calendar"
    return f"lunar-{year}-{month}-{day}@lunar-calendar"


def _validate_reminders(reminders: list[int] = REMINDERS) -> None:
    for hours in reminders:
        if hours <= 0:
            raise ValueError("Reminder hours must be positive")


def _iter_month_variants() -> tuple[bool, ...]:
    return (False, True) if INCLUDE_LEAP_MONTHS else (False,)


def _escape_ics_text(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace(";", "\\;")
        .replace(",", "\\,")
        .replace("\n", "\\n")
    )


def _format_date(value: date) -> str:
    return value.strftime("%Y%m%d")


def build_calendar(start_year: int = START_YEAR, end_year: int = END_YEAR) -> str:
    if end_year < start_year:
        raise ValueError("END_YEAR must be >= START_YEAR")

    _validate_reminders()
    dtstamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    lines = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//lunar-calendar-ics//Lunar Calendar Reminder//EN",
        "CALSCALE:GREGORIAN",
        f"X-WR-CALNAME:{_escape_ics_text(CALENDAR_NAME)}",
    ]

    for year in range(start_year, end_year + 1):
        for month in range(1, 13):
            for is_leap_month in _iter_month_variants():
                for day in (1, 15):
                    try:
                        lunar = LunarDate(year, month, day, isLeapMonth=is_leap_month)
                        solar = lunar.toSolarDate()
                    except ValueError:
                        continue

                    event_title = build_title(day)
                    event_uid = build_uid(year, month, day, is_leap_month)

                    lines.extend(
                        [
                            "BEGIN:VEVENT",
                            f"UID:{event_uid}",
                            f"DTSTAMP:{dtstamp}",
                            f"SUMMARY:{_escape_ics_text(event_title)}",
                            f"DTSTART;VALUE=DATE:{_format_date(solar)}",
                            f"DTEND;VALUE=DATE:{_format_date(solar + timedelta(days=1))}",
                            f"DESCRIPTION:{_escape_ics_text(EVENT_DESCRIPTION)}",
                        ]
                    )

                    for hours in REMINDERS:
                        lines.extend(
                            [
                                "BEGIN:VALARM",
                                f"TRIGGER:-PT{hours}H",
                                "ACTION:DISPLAY",
                                f"DESCRIPTION:{_escape_ics_text(ALARM_DESCRIPTION)}",
                                "END:VALARM",
                            ]
                        )

                    lines.append("END:VEVENT")

    lines.append("END:VCALENDAR")
    return "\n".join(lines) + "\n"


def generate_ics(output_path: str | Path = "lunar_reminder.ics") -> int:
    calendar_text = build_calendar()
    output = Path(output_path)
    output.write_text(calendar_text, encoding="utf-8", newline="\n")
    return calendar_text.count("BEGIN:VEVENT")
