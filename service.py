import pandas as pd
from pydantic import BaseModel
from typing import List, Dict
from src.predict import IrisPredictor
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Iris Classifier API")
predictor = IrisPredictor()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Input model for a single sample
class Features(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float


# Input model for batch
class BatchRequest(BaseModel):
    samples: List[Features]


# Output model for prediction result
class PredictionResult(BaseModel):
    prediction: str
    probabilities: Dict[str, float]


@app.get("/")
async def root():
    return {
        "message": "👋 Welcome to the Iris Classification API!",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict_batch",
            "file_predict": "/predict_file",
            "docs": "/docs",
        },
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/predict")
async def predict_species(features: Features):
    df = predictor.to_dataframe(
        features.sepal_length,
        features.sepal_width,
        features.petal_length,
        features.petal_width,
    )
    prediction = predictor.predict(df)
    proba = predictor.predict_proba(df).to_dict(orient="records")[0]
    return {"prediction": prediction, "probabilities": proba}


@app.post("/predict_batch", response_model=List[PredictionResult])
async def predict_batch(request: BatchRequest):
    # Convert input to DataFrame
    samples = request.model_dump()["samples"]
    df = pd.DataFrame(samples)

    preds = predictor.model.predict(df)
    probs = predictor.model.predict_proba(df)
    classes = predictor.model.classes_

    results = []
    for pred, prob in zip(preds, probs):
        results.append(
            {"prediction": pred, "probabilities": dict(zip(classes, prob.round(4)))}
        )

    return results


@app.post("/predict_file")
async def predict_file(file: UploadFile = File(...)):
    if file.content_type != "text/csv":
        raise HTTPException(status_code=400, detail="Only CSV files are accepted.")
    df = pd.read_csv(file.file)
    probs_df = predictor.predict_batch(df)
    return probs_df.to_dict(orient="records")
