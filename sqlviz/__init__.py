"""
SQLViz - A Python library for visualizing SQL query results with interactive charts.

Usage (API):
------------
from sqlviz import SQLViz

viz = SQLViz("sqlite:///mydb.db")
viz.visualize("SELECT * FROM my_table", chart_type="bar", x="col1", y="col2")

Usage (CLI):
------------
# Using the CLI helper
sqlviz --sql "SELECT * FROM my_table" --db sqlite:///mydb.db --chart bar --output result.png --format png
"""

from .core import SQLViz, visualize_sql_cli, process_sql

__all__ = ["SQLViz", "visualize_sql_cli", "process_sql"]

__version__ = "0.0.1"
