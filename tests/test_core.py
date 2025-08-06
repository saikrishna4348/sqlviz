# tests/test_core.py
import pytest
from sqlviz.core import SQLViz

@pytest.fixture
def sv():
    obj = SQLViz("sqlite:///:memory:")
    with obj.engine.begin() as conn:
        conn.exec_driver_sql("CREATE TABLE t (x INT, y INT)")
        conn.exec_driver_sql("INSERT INTO t(x, y) VALUES (1, 2), (3, 4)")
    return obj

def test_query(sv):
    df = sv.query("SELECT * FROM t")
    assert len(df) == 2

def test_visualize_bar(sv):
    fig = sv.visualize("SELECT * FROM t", chart_type="bar", x="x", y="y", show=False)
    assert fig is not None

def test_empty_result(sv):
    import pandas as pd
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t WHERE x < 0", chart_type="bar", show=False)

def test_invalid_chart(sv):
    with pytest.raises(ValueError):
        sv.visualize("SELECT * FROM t", chart_type="unknown", show=False)
