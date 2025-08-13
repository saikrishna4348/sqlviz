# SQLViz

SQLViz is a Python library that allows you to query SQL databases and visualize the results directly using Plotly charts.

---

## Installation

```bash
pip install sqlviz
```

---

## Features

* Query any SQL database supported by SQLAlchemy.
* Generate charts (bar, line, scatter, etc.) from SQL queries.
* CLI utility to quickly visualize SQL results.
* Auto-detect x/y columns when not provided.

---

## CLI Usage

You can use SQLViz from the command line to generate charts directly from your database.

### Syntax

```bash
sqlviz-cli --db-uri <DATABASE_URI> --sql "<SQL_QUERY>" --chart-type <CHART_TYPE> [--x <X_COLUMN>] [--y <Y_COLUMN>] [--show False]
```

### Parameters

* `--db-uri`: SQLAlchemy database URI (e.g., `sqlite:///mydata.db`).
* `--sql`: SQL query to fetch data.
* `--chart-type`: Type of chart (`bar`, `line`, `scatter`, etc.).
* `--x`: (Optional) Column name for X-axis.
* `--y`: (Optional) Column name for Y-axis.
* `--show`: Whether to display the chart immediately (default: True).

### Example

```bash
sqlviz-cli --db-uri sqlite:///test.db --sql "SELECT * FROM t" --chart-type bar --x x --y y --show False
```

This will generate a bar chart from the `t` table in `test.db`, mapping `x` to X-axis and `y` to Y-axis, without displaying it immediately.

---

## Python Usage

```python
from sqlviz.core import visualize_sql_cli

fig = visualize_sql_cli(
    db_uri="sqlite:///test.db",
    sql="SELECT * FROM t",
    chart_type="bar",
    show=True,
    kwargs_str='{"x": "x", "y": "y"}'
)
```

`fig` is a Plotly Figure object and can be further customized or saved.

---

## License

MIT License
