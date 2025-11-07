from app.data import Database
from app.machine import Machine
import pandas as pd


def load_monster_data(limit: int = 1000) -> pd.DataFrame:
    """Load Monster data from MongoDB and return as a DataFrame.
    
    Args:
        Limit (int) = number of monsters to include for testing
    
    Returns:
        pd.DataFrame =  DataFrame that contains the features and target
    """

    db = Database()
    monsters = list(db.collection.find())
    df = pd.DataFrame(monsters).drop(columns=["_id"]).head(limit)
    return df

def test_machine_class(df: pd.DataFrame, model_types=None, save_dir: str = "models"):
    """Train, test, save and load a Machine learning model.
        
    Args:
        df (pd.DataFream): Dataframe containing features and target
        model_type (srt): Type of model to be trained (rfc, lr, or xgb)
        model_path (str): Filepath to safe and load the trained model
    """

    if model_types is None:
        model_types = ["rfc", "lr", "xgb"]

    results = {}

    for model_type in model_types:
        model_path = f"{save_dir}/monster_{model_type}.joblib"

        model = Machine(df, model_type=model_type)

        sample = df.drop(columns=["rarity"]).iloc[[0]]
        pred_label, prob = model(sample)


        model.save(model_path)
        loaded_model = Machine.open(model_path)
        pred_label_loaded, prob_loaded = loaded_model(sample)

        results[model_type] = {
            "trained_model": model,
            "loaded_model": loaded_model,
            "sample_predicton": (pred_label, prob),
            "loaded_sample_prediction": (pred_label_loaded, prob_loaded)
        }
    
    return results

if __name__ == "__main__":
    data_frame = load_monster_data()
    model_results = test_machine_class(data_frame)

    sample_input = data_frame.drop(columns=["rarity"]).iloc[[0]]
    print("Sample input features:")
    print(sample_input)

    for model_type in ["rfc", "lr", "xgb"]:
        trained_model = model_results[model_type]["trained_model"]
        loaded_model = model_results[model_type]["loaded_model"]

        pred_label, prob = trained_model(sample_input)
        pred_label_loaded, prob_loaded = loaded_model(sample_input)

        print(f"\n=== {trained_model.name} ====")
        print(f"Predictions (trained model): {pred_label}, Probability: {prob:.2f}")
        print(f"Prediction (loaded model): {pred_label_loaded}, Probability: {prob_loaded:.2f}")
