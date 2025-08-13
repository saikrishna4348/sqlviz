"""
SQLViz - A Python library for visualizing SQL query results with interactive charts.

Usage (API):
------------
from sqlviz import SQLViz

viz = SQLViz("sqlite:///mydb.db")
viz.visualize("SELECT * FROM my_table", chart_type="bar", x="col1", y="col2")

Usage (CLI):
------------
sqlviz --db sqlite:///mydb.db --query "SELECT * FROM my_table" --chart bar
"""

from .core import SQLViz, visualize_sql_cli

__all__ = ["SQLViz", "visualize_sql_cli"]

__version__ = "0.0.1"
