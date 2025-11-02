from dotenv import load_dotenv
load_dotenv
from app.data import Database
from app.graph import chart

db = Database()
df = db.dataframe()


if df is None or df.empty:
    db.seed(1000)
    df = db.dataframe()

tc = chart(df, x="Health", y="Energy", target="Rarity")

tc.show()