from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd

TARGET_COUNTRIES = {
    "turkey",
    "brazil",
    "mexico",
    "argentina",
    "colombia",
    "south africa",
    "indonesia",
    "vietnam",
    "thailand",
}

GOOD_KEYWORDS = [
    "travel",
    "traveller",
    "traveler",
    "trip",
    "tourism",
    "vacation",
    "holiday",
    "digital nomad",
    "backpacking",
    "flight",
    "hotel",
    "abroad",
    "esim",
    "roaming",
    "internet abroad",
    "gezi",
    "seyahat",
    "gezgin",
    "viagem",
    "viajar",
    "viagens",
    "viaje",
    "viajes",
    "viajero",
    "viajera",
]

BAD_KEYWORDS = [
    "casino",
    "betting",
    "bet",
    "crypto",
    "forex",
    "adult",
    "onlyfans",
    "giveaway",
    "fake",
    "loan",
    "investment",
]


@dataclass
class ScoreResult:
    score: int
    grade: str
    reason: str


def contains_any(text: Any, words: list[str]) -> list[str]:
    value = "" if pd.isna(text) else str(text).lower()
    return [word for word in words if word in value]


def grade_score(score: int) -> str:
    if score >= 80:
        return "A - dərhal yaz"
    if score >= 60:
        return "B - yaxşı partner"
    if score >= 40:
        return "C - sonra bax"
    return "Reject"


def score_influencer(row: pd.Series) -> ScoreResult:
    score = 0
    reasons: list[str] = []

    country = str(row.get("country", "")).strip().lower()
    bio = str(row.get("bio", "")).strip().lower()
    followers = int(row.get("followers", 0) or 0)
    engagement = float(row.get("engagement_rate", 0) or 0)
    email = str(row.get("email", "")).strip()

    if country in TARGET_COUNTRIES or any(c in country for c in TARGET_COUNTRIES):
        score += 20
        reasons.append("target country")

    good_matches = contains_any(bio, GOOD_KEYWORDS)
    if good_matches:
        score += 25
        reasons.append("travel keyword found: " + ", ".join(good_matches[:3]))

    if email:
        score += 25
        reasons.append("email available")
    else:
        score -= 10
        reasons.append("missing email")

    if 5_000 <= followers <= 150_000:
        score += 20
        reasons.append("good follower range")
    elif 150_000 < followers <= 500_000:
        score += 10
        reasons.append("large but acceptable follower range")
    elif followers < 3_000:
        score -= 20
        reasons.append("followers under 3k")
    elif followers > 1_000_000:
        score -= 20
        reasons.append("followers over 1M")

    if engagement >= 4:
        score += 20
        reasons.append("excellent engagement")
    elif engagement >= 2:
        score += 10
        reasons.append("good engagement")

    bad_matches = contains_any(bio, BAD_KEYWORDS)
    if bad_matches:
        score -= 60
        reasons.append("bad keyword found: " + ", ".join(bad_matches[:3]))

    return ScoreResult(score=score, grade=grade_score(score), reason="; ".join(reasons))


def score_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    results = df.apply(score_influencer, axis=1)
    scored = df.copy()
    scored["score"] = [result.score for result in results]
    scored["grade"] = [result.grade for result in results]
    scored["reason"] = [result.reason for result in results]
    return scored.sort_values(by="score", ascending=False)
