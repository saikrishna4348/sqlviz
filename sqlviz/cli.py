import argparse

from sqlviz.core import process_sql


def main():
    parser = argparse.ArgumentParser(
        description="SQLViz - Visualize SQL queries and results"
    )
    parser.add_argument("input_file", type=str, help="Path to the SQL file to process")
    parser.add_argument(
        "--output",
        type=str,
        default="output.html",
        help="Path for the generated visualization file (default: output.html)",
    )
    args = parser.parse_args()

    process_sql(args.input_file, args.output)


if __name__ == "__main__":
    main()
