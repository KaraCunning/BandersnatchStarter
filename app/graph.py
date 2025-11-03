import altair as alt
from altair import Chart
from pandas import DataFrame


def chart(df: DataFrame, x: str, y: str, target: str) -> Chart:
    """Create an interactive scatter plot visualization.
    
    Args:
        df: DataFrame containing monster data
        x: Column name for x-axis
        y: Column name for y-axis
        target: Column name for color encoding
        
    Returns:
        Altair Chart object
    """

    properties = {
        "width": 600,
        "height": 400,
        "background": "#2a303c",
        "padding": 20
    }

    graph = (
        alt.Chart(df, title=f"{y} by {x} for {target}")
        .mark_circle(size=100)
        .encode(
            x = alt.X(x, title=x),
            y = alt.Y(y, title=y),
            color = alt.Color(target, type = "nominal", legend=alt.Legend(title=target)),
            tooltip = list(df.columns)
        )
        .properties(
            width = properties["width"],
            height = properties["height"],
            background = properties["background"],
            padding = properties ["padding"]
        )
        .configure_axis(
            labelColor = "#ffffff",
            titleColor = "#ffffff",
        )

        .configure_title(color = "#ffffff")
        .configure_legend(
            labelColor = "#ffffff",
            titleColor = "#ffffff"
        )
        .configure_view(stroke = "transparent")
    
    )
    return graph