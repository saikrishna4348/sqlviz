import json
from typing import Any, Dict, Optional

import pandas as pd
import plotly.express as px
from plotly.graph_objs import Figure
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


class SQLViz:
    """Core SQL to visualization engine."""

    def __init__(self, db_uri: str):
        self.engine: Engine = create_engine(db_uri, future=True)

    def query(self, sql: str) -> pd.DataFrame:
        """Run a SQL query and return the result as a DataFrame."""
        return pd.read_sql(sql, self.engine)

    def visualize(
        self,
        sql: str,
        chart_type: str = "bar",
        show: bool = True,
        output: Optional[str] = None,
        chart_backend: str = "plotly",
        **kwargs: Any,
    ) -> Figure:
        """Run a SQL query and visualize the results."""
        df = self.query(sql)
        if df.empty:
            raise ValueError("The SQL query returned no data.")

        if chart_backend == "plotly":
            chart_fn = {
                "bar": px.bar,
                "line": px.line,
                "scatter": px.scatter,
            }.get(chart_type)

            if chart_fn is None:
                raise ValueError(f"Unsupported chart type: {chart_type}")

            # Auto-detect x/y if not specified
            if "x" not in kwargs or "y" not in kwargs:
                if df.shape[1] >= 2:
                    kwargs.setdefault("x", df.columns[0])
                    kwargs.setdefault("y", df.columns[1])

            fig: Figure = chart_fn(df, **kwargs)

            if output:
                fig.write_image(output)
            if show:
                fig.show()

            return fig

        raise NotImplementedError(
            f"Chart backend '{chart_backend}' not implemented yet."
        )


def visualize_sql_cli(
    db_uri: str,
    sql: str,
    chart_type: str = "bar",
    show: bool = True,
    output: Optional[str] = None,
    chart_backend: str = "plotly",
    kwargs_str: Optional[str] = None,
) -> Figure:
    """CLI-friendly function to visualize SQL query results."""
    extra_kwargs: Dict[str, Any] = json.loads(kwargs_str) if kwargs_str else {}
    viz = SQLViz(db_uri)
    return viz.visualize(
        sql=sql,
        chart_type=chart_type,
        show=show,
        output=output,
        chart_backend=chart_backend,
        **extra_kwargs,
    )


def process_sql(
    sql_query: str,
    output: Optional[str] = None,
    fmt: str = "png",
) -> str:
    """Process the SQL query for CLI and optionally save visualization output.

    Args:
        sql_query: The SQL query string.
        output: Optional path to save visualization (default: None).
        fmt: Output format (png, svg, pdf, html), default is 'png'.

    Returns:
        The original SQL query (placeholder for extended processing).
    """
    # TODO: Implement actual processing and visualization logic
    # Example: save diagram or visualization if output is provided
    return sql_query


__all__ = ["SQLViz", "visualize_sql_cli", "process_sql"]
