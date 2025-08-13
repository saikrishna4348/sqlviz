# tests/test_core.py
import os
import sys
import pytest

# Ensure package root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sqlviz.core import SQLViz, visualize_sql_cli


@pytest.fixture
def sv():
    """Fixture to create an in-memory SQLite DB with test data."""
    obj = SQLViz("sqlite:///:memory:")
    with obj.engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE t (x INT, y INT)")
        conn.exec_driver_sql("INSERT INTO t(x, y) VALUES (1, 2), (3, 4)")
    return obj


def test_query(sv):
    df = sv.query("SELECT * FROM t")
    assert len(df) == 2
    assert list(df.columns) == ["x", "y"]


def test_visualize_bar_with_xy(sv):
    fig = sv.visualize("SELECT * FROM t", chart_type="bar", x="x", y="y", show=False)
    assert fig is not None


def test_visualize_bar_auto_xy(sv):
    """Test auto x/y detection when not provided."""
    fig = sv.visualize("SELECT * FROM t", chart_type="bar", show=False)
    assert fig is not None


def test_empty_result(sv):
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t WHERE x < 0", chart_type="bar", show=False)


def test_invalid_chart(sv):
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t", chart_type="unknown", show=False)


def test_cli_function():
    """Test the CLI helper function."""
    db_uri = "sqlite:///:memory:"
    from sqlalchemy import create_engine

    engine = create_engine(db_uri, future=True)
    with engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE t (x INT, y INT)")
        conn.exec_driver_sql("INSERT INTO t(x, y) VALUES (1, 2), (3, 4)")

    fig = visualize_sql_cli(
        db_uri=db_uri,
        sql="SELECT * FROM t",
        chart_type="bar",
        show=False,
        kwargs_str='{"x": "x", "y": "y"}',
    )
    assert fig is not None
