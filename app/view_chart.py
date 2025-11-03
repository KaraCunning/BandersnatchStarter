import os
import webbrowser

import pandas as pd
import altair as alt

from app.data import Database
from app.graph import chart


alt.renderers.enable('default')

def render_chart(local_demo: bool = False):
    """ Load monster data and generate a chart
    
    Args:
        local_demo (bool):
            True -> open chart in local browser using .show()
            False -> return html safe for embedding  in Render/Flask
    """
    db = Database()
    df = db.dataframe()

    if df is None or df.empty:
        db.seed(1000)
        df = db.dataframe()

    tc = chart(df, x="health", y="energy", target="rarity")

    if local_demo:
        filename = "monster_chart.html"
        tc.save(filename)
        filepath = os.path.abspath(filename)
        webbrowser.open(f"file://{filepath}", new=2)
        return None

    return tc.to_html()

if __name__ == "__main__":
    render_chart(local_demo=True)