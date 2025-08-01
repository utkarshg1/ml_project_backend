import joblib
import pandas as pd
from functools import lru_cache
from pathlib import Path
from sklearn.pipeline import Pipeline
from src.constants import MODEL_PATH
from src.logging_config import logger


@lru_cache(maxsize=1)
def load_model(model_path: Path) -> Pipeline:
    logger.info(f"Loading model from : {model_path}")
    return joblib.load(model_path)


class IrisPredictor:

    def __init__(self, model_path: Path = MODEL_PATH) -> None:
        self.model_path = model_path
        self.model = load_model(self.model_path)
        self.classes = self.model.classes_

    def to_dataframe(
        self, sep_len: float, sep_wid: float, pet_len: float, pet_wid: float
    ) -> pd.DataFrame:
        logger.info("Converting to dataframe")
        data = [
            {
                "sepal_length": sep_len,
                "sepal_width": sep_wid,
                "petal_length": pet_len,
                "petal_width": pet_wid,
            }
        ]
        df = pd.DataFrame(data)
        logger.info(f"Converted to dataframe :\n{df}")
        return df

    def predict(self, x: pd.DataFrame):
        preds = self.model.predict(x)[0]
        logger.info(f"Prediction : {preds}")
        return preds

    def predict_proba(self, x: pd.DataFrame):
        probs = self.model.predict_proba(x)
        probs_df = pd.DataFrame(probs, columns=self.classes)
        logger.info(f"Predicted probabilities :\n{probs_df}")
        return probs_df.round(4)

    def predict_batch(self, x: pd.DataFrame):
        preds = self.model.predict(x)
        probs = self.model.predict_proba(x)
        probs_df = pd.DataFrame(probs, columns=self.classes).round(4)
        probs_df.insert(0, "prediction", preds)
        logger.info(f"Batch prediction results :\n{probs_df}")
        return probs_df
