import unittest
import pandas as pd
import altair as alt
from app.graph import chart


class TestGraph(unittest.TestCase):
    """Unit test for the chart function"""

    def setUp(self):
        """Create a small fake dataset instead of callling the actual datatset."""
        self.df = pd.DataFrame({
            "health": [50, 80, 30],
            "energy": [70, 60, 40],
            "rarity": ["Rank1", "Rank2", "Rank4"]
        })

    def test_chart_returns_altair_chart(self):
        """Test the chart and returns altair chart"""
        tc = chart(self.df, "health", "energy", "rarity")
        self.assertIsInstance(tc, alt.Chart)
        
    def test_chart_has_correct_encodings(self):
        """Check the encodings have the correct fields"""
        tc = chart(self.df, "health", "energy", "rarity")

        enc = tc.to_dict()["encoding"]
        self.assertEqual(enc["x"]["field"], "health")
        self.assertEqual(enc["y"]["field"], "energy")
        self.assertEqual(enc["color"]["field"], "rarity")

if __name__ == "__main__":
    unittest.main()