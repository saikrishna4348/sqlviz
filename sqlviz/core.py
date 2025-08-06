# sqlviz/core.py
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine


class SQLViz:
    def __init__(self, db_uri: str):
        self.engine = create_engine(db_uri, future=True)

    def query(self, sql: str) -> pd.DataFrame:
        return pd.read_sql(sql, self.engine)

    def visualize(
        self,
        sql: str,
        chart_type: str = "bar",
        show: bool = True,
        output: str = None,
        chart_backend: str = "plotly",
        **kwargs,
    ):
        df = self.query(sql)
        if df.empty:
            raise ValueError("The SQL query returned no data.")
        if chart_backend == "plotly":
            chart_fn = {"bar": px.bar, "line": px.line, "scatter": px.scatter}.get(
                chart_type
            )
            if chart_fn is None:
                raise ValueError(f"Unsupported chart type: {chart_type}")
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
