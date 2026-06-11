from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer

from cleaning import normalize_dataframe
from exporter import export_excel
from scoring import score_dataframe

app = typer.Typer(help="Filter influencer CSV exports for travel/eSIM partner outreach.")


@app.command()
def filter(
    input: str = typer.Option(..., "--input", "-i", help="Input CSV file path"),
    output: str = typer.Option("filtered_influencers.xlsx", "--output", "-o", help="Output Excel file path"),
) -> None:
    input_path = Path(input)
    output_path = Path(output)

    if not input_path.exists():
        typer.echo(f"Error: input file not found: {input_path}", err=True)
        raise typer.Exit(code=1)

    try:
        raw_df = pd.read_csv(input_path)
    except Exception as exc:
        typer.echo(f"Error: could not read CSV file: {exc}", err=True)
        raise typer.Exit(code=1)

    if raw_df.empty:
        typer.echo("Error: input CSV is empty", err=True)
        raise typer.Exit(code=1)

    normalized_df = normalize_dataframe(raw_df)
    scored_df = score_dataframe(normalized_df)

    columns = [
        "score",
        "grade",
        "name",
        "username",
        "platform",
        "country",
        "followers",
        "engagement_rate",
        "email",
        "profile_url",
        "bio",
        "reason",
    ]
    scored_df = scored_df[columns]

    export_excel(scored_df, str(output_path))
    typer.echo(f"Done: {output_path}")


if __name__ == "__main__":
    app()
