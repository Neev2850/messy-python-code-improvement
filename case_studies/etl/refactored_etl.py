"""
Refactored Data Cleaning & ETL Pipeline
Optimized with O(n) set lookups, dataclass validation, typing, and detailed error logging.
"""

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set, Tuple
import logging
import re

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


@dataclass(frozen=True)
class UserRecord:
    name: str
    email: str
    age: int

    @classmethod
    def from_raw(cls, raw: Dict[str, Any]) -> Optional["UserRecord"]:
        try:
            name = str(raw.get("name", "")).strip().title()
            email = str(raw.get("email", "")).strip().lower()
            age = int(raw.get("age", -1))

            if not name:
                logger.warning(f"Rejected record due to blank name: {raw}")
                return None
            if not EMAIL_REGEX.match(email):
                logger.warning(f"Rejected invalid email '{email}' for user '{name}'")
                return None
            if age < 18 or age > 100:
                logger.warning(f"Rejected out-of-range age {age} for user '{name}'")
                return None

            return cls(name=name, email=email, age=age)
        except (ValueError, TypeError) as exc:
            logger.error(f"Error parsing raw record {raw}: {exc}")
            return None


def clean_user_records(raw_data: List[Dict[str, Any]]) -> Tuple[List[UserRecord], int]:
    """
    Cleans raw user dictionaries, deduplicates via O(1) set membership,
    and returns verified UserRecord instances with count of dropped rows.
    """
    cleaned_records: List[UserRecord] = []
    seen_emails: Set[str] = set()
    dropped_count = 0

    for raw in raw_data:
        record = UserRecord.from_raw(raw)
        if record is None:
            dropped_count += 1
            continue

        if record.email in seen_emails:
            logger.info(f"Deduplicated duplicate email: {record.email}")
            dropped_count += 1
            continue

        seen_emails.add(record.email)
        cleaned_records.append(record)

    return cleaned_records, dropped_count
