import argparse
from pathlib import Path
from typing import Optional

from sqlviz.core import process_sql


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Visualize SQL queries as diagrams or execution plans."
    )
    parser.add_argument("sql_source", help="Path to the SQL file or direct SQL string.")
    parser.add_argument(
        "-o",
        "--output",
        help=(
            "Path to save visualization output (e.g., diagram.png). "
            "If not provided, shows inline."
        ),
        default=None,
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Output format (png, svg, pdf, html).",
        choices=["png", "svg", "pdf", "html"],
        default="png",
    )

    args = parser.parse_args()

    # Determine if the argument is a file path or raw SQL
    sql_path = Path(args.sql_source)
    if sql_path.exists() and sql_path.is_file():
        sql_text: str = sql_path.read_text(encoding="utf-8")
    else:
        sql_text = args.sql_source

    # Call process_sql with typed parameters
    process_sql(sql_query=sql_text, output=args.output, fmt=args.format)


if __name__ == "__main__":
    main()
