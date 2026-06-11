from __future__ import annotations

import re
from typing import Any

import pandas as pd

EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

COLUMN_ALIASES = {
    "name": ["name", "full_name", "fullname", "creator_name"],
    "username": ["username", "handle", "user_name", "account"],
    "platform": ["platform", "social_network", "network", "channel"],
    "followers": ["followers", "followers_count", "follower_count", "fans"],
    "engagement_rate": ["engagement_rate", "engagement", "er", "engagement %"],
    "country": ["country", "location", "audience_country", "creator_country"],
    "bio": ["bio", "description", "about", "profile_bio"],
    "email": ["email", "contact_email", "business_email"],
    "profile_url": ["profile_url", "url", "link", "profile_link"],
}

STANDARD_COLUMNS = list(COLUMN_ALIASES.keys())


def normalize_col_name(value: str) -> str:
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def find_column(df: pd.DataFrame, aliases: list[str]) -> str | None:
    normalized = {normalize_col_name(col): col for col in df.columns}
    for alias in aliases:
        key = normalize_col_name(alias)
        if key in normalized:
            return normalized[key]
    return None


def normalize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    output = pd.DataFrame()
    for standard_col, aliases in COLUMN_ALIASES.items():
        matched = find_column(df, aliases)
        output[standard_col] = df[matched] if matched else ""

    output["followers"] = output["followers"].apply(parse_followers)
    output["engagement_rate"] = output["engagement_rate"].apply(parse_engagement_rate)
    output["email"] = output.apply(lambda row: extract_best_email(row.get("email", ""), row.get("bio", "")), axis=1)
    return output


def parse_followers(value: Any) -> int:
    if pd.isna(value):
        return 0
    text = str(value).strip().replace(",", "").lower()
    if not text:
        return 0

    multiplier = 1
    if text.endswith("k"):
        multiplier = 1_000
        text = text[:-1]
    elif text.endswith("m"):
        multiplier = 1_000_000
        text = text[:-1]

    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return 0
    return int(float(match.group()) * multiplier)


def parse_engagement_rate(value: Any) -> float:
    if pd.isna(value):
        return 0.0
    text = str(value).strip().replace(",", ".")
    if not text:
        return 0.0

    has_percent = "%" in text
    match = re.search(r"\d+(?:\.\d+)?", text)
    if not match:
        return 0.0

    number = float(match.group())
    if has_percent:
        return number
    if 0 < number < 1:
        return number * 100
    return number


def has_email(value: Any) -> bool:
    if pd.isna(value):
        return False
    return bool(EMAIL_RE.search(str(value)))


def extract_best_email(email_value: Any, bio_value: Any = "") -> str:
    for value in [email_value, bio_value]:
        if pd.isna(value):
            continue
        match = EMAIL_RE.search(str(value))
        if match:
            return match.group(0)
    return ""
