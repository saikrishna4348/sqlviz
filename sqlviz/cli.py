import click
from .core import visualize_sql_cli


@click.command()
@click.option('--db', 'db_uri', required=True, help='Database URI (e.g., sqlite:///mydb.db)')
@click.option('--query', required=True, help='SQL query to execute')
@click.option('--chart', 'chart_type', default='bar', help='Chart type: bar, line, scatter')
@click.option('--show/--no-show', default=True, help='Display the chart interactively')
@click.option('--output', default=None, help='Path to save chart image (optional)')
@click.option('--chart-backend', default='plotly', help='Chart backend (currently only "plotly")')
@click.option('--kwargs', 'kwargs_str', default=None,
              help='Extra chart kwargs as JSON string (e.g. \'{"x": "col1", "y": "col2"}\')')
def main(db_uri, query, chart_type, show, output, chart_backend, kwargs_str):
    """
    Run SQL query and visualize results from the command line.
    Example:
        sqlviz --db sqlite:///sales.db --query "SELECT * FROM sales" --chart bar
    """
    visualize_sql_cli(
        db_uri=db_uri,
        sql=query,
        chart_type=chart_type,
        show=show,
        output=output,
        chart_backend=chart_backend,
        kwargs_str=kwargs_str,
    )


if __name__ == "__main__":
    main()
