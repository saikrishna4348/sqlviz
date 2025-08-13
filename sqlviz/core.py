import json
from typing import Optional, Union

import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


class SQLViz:
    """Core SQL to visualization engine."""

    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri, future=True)

    def query(self, sql: str) -> pd.DataFrame:
        return pd.read_sql(sql, self.engine)

    def visualize(
        self,
        sql: str,
        chart_type: str = "bar",
        show: bool = True,
        output: Optional[str] = None,
        chart_backend: str = "plotly",
        **kwargs,
    ):
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

            fig = chart_fn(df, **kwargs)
            if output:
                fig.write_image(output)
            if show:
                fig.show()
            return fig
        else:
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
):
    """CLI-friendly function to visualize SQL query results."""
    extra_kwargs = json.loads(kwargs_str) if kwargs_str else {}
    viz = SQLViz(db_uri)
    return viz.visualize(
        sql=sql,
        chart_type=chart_type,
        show=show,
        output=output,
        chart_backend=chart_backend,
        **extra_kwargs,
    )
