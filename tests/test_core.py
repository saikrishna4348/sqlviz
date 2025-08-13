import os
import sys
from typing import TYPE_CHECKING

import pytest
from sqlalchemy import create_engine

# Ensure package root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlviz.core import SQLViz, visualize_sql_cli  # noqa: E402

if TYPE_CHECKING:
    from plotly.graph_objs import Figure


@pytest.fixture
def sv() -> SQLViz:
    """Fixture to create an in-memory SQLite DB with test data."""
    obj = SQLViz("sqlite:///:memory:")
    with obj.engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE t (x INT, y INT)")
        conn.exec_driver_sql("INSERT INTO t(x, y) VALUES (1, 2), (3, 4)")
    return obj


def test_query(sv: SQLViz) -> None:
    df = sv.query("SELECT * FROM t")
    assert len(df) == 2
    assert list(df.columns) == ["x", "y"]


def test_visualize_bar_with_xy(sv: SQLViz) -> None:
    fig: "Figure" = sv.visualize("SELECT * FROM t", chart_type="bar", x="x", y="y", show=False)
    assert fig is not None


def test_visualize_bar_auto_xy(sv: SQLViz) -> None:
    """Test auto x/y detection when not provided."""
    fig: "Figure" = sv.visualize("SELECT * FROM t", chart_type="bar", show=False)
    assert fig is not None


def test_empty_result(sv: SQLViz) -> None:
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t WHERE x < 0", chart_type="bar", show=False)


def test_invalid_chart(sv: SQLViz) -> None:
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t", chart_type="unknown", show=False)


def test_cli_function() -> None:
    """Test the CLI helper function."""
    db_uri = "sqlite:///:memory:"
    engine = create_engine(db_uri, future=True)
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE t (x INT, y INT)")
        conn.exec_driver_sql("INSERT INTO t(x, y) VALUES (1, 2), (3, 4)")

    fig: "Figure" = visualize_sql_cli(
        db_uri=db_uri,
        sql="SELECT * FROM t",
        chart_type="bar",
        show=False,
        kwargs_str='{"x": "x", "y": "y"}',
    )
    assert fig is not None
