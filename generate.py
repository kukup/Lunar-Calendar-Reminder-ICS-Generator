from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from lunar_calendar.generator import generate_ics


if __name__ == "__main__":
    output_file = ROOT / "lunar_reminder.ics"
    count = generate_ics(output_file)
    print(f"Generated {count} events -> {output_file.name}")
