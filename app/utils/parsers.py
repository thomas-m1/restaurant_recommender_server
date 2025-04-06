from datetime import datetime
import re
from typing import List, Dict

DAY_MAP = {
    0: "Mon", 1: "Tue", 2: "Wed", 3: "Thu",
    4: "Fri", 5: "Sat", 6: "Sun"
}

def format_hours(hours_raw: List[Dict]) -> List[str]:
    if not hours_raw:
        return []
    results = []
    for block in hours_raw:
        for h in block.get("open", []):
            day = DAY_MAP.get(h["day"], f"Day {h['day']}")
            start = datetime.strptime(h["start"], "%H%M").strftime("%-I:%M %p")
            end = datetime.strptime(h["end"], "%H%M").strftime("%-I:%M %p")
            results.append(f"{day} {start} – {end}")
    return results

def extract_tags_from_specialties(specialties: str) -> List[str]:
    if not specialties:
        return []
    raw_tags = re.split(r"[\n\.\*:,]+", specialties)
    tags = [t.strip() for t in raw_tags if t.strip()]
    return tags[:5]  # return top 5 relevant tags

def combine_display_tags(
    liked_by: List[str],
    ambience_data: Dict,
    specialty_tags: List[str]
) -> List[str]:
    tags = []
    tags.extend(liked_by)
    tags.extend([
        k.replace("_", " ").title()
        for k, v in (ambience_data or {}).items() if v
    ])
    tags.extend(specialty_tags)
    return list(dict.fromkeys(tags))
