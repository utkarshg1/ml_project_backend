# Iris Classification API

A FastAPI-based REST API for classifying Iris flower species using machine learning. This service provides endpoints for single predictions, batch processing, and file uploads.

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [API Endpoints](#-api-endpoints)
- [Installation](#-installation)
- [Usage](#-usage)
- [API Reference](#-api-reference)
- [Request/Response Models](#-requestresponse-models)
- [Error Handling](#-error-handling)
- [CORS Configuration](#-cors-configuration)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Performance](#-performance)
- [Contributing](#-contributing)
- [Author](#-author)

## 🌸 Overview

This FastAPI service provides a production-ready REST API for the Iris flower classification model. It offers multiple prediction endpoints to handle different use cases, from single sample predictions to batch processing and file uploads.

The API is built on top of the trained Logistic Regression model and provides:
- Real-time predictions with probability scores
- Batch processing capabilities
- File upload support for CSV datasets
- Comprehensive error handling
- CORS support for web applications
- Interactive API documentation

## ✨ Features

- **RESTful API**: Clean, intuitive REST endpoints
- **Multiple Input Methods**: Single samples, batch requests, and file uploads
- **Probability Scores**: Returns prediction probabilities for all classes
- **CORS Enabled**: Ready for web application integration
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc
- **Error Handling**: Comprehensive error responses
- **Type Safety**: Pydantic models for request/response validation
- **Health Check**: Service health monitoring endpoint

## 🚀 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Welcome message and endpoint overview |
| `GET` | `/health` | Health check endpoint |
| `POST` | `/predict` | Single sample prediction |
| `POST` | `/predict_batch` | Batch prediction for multiple samples |
| `POST` | `/predict_file` | File upload prediction (CSV) |
| `GET` | `/docs` | Interactive API documentation (Swagger UI) |
| `GET` | `/redoc` | Alternative API documentation (ReDoc) |

## 🔧 Installation

### Prerequisites

- Python 3.8+
- Trained Iris model (run `main.py` first to generate the model)
- [uv](https://docs.astral.sh/uv/) package manager (recommended)

### Setup

1. **Ensure the model is trained**
   ```bash
   # Train the model first if not already done
   uv run main.py
   ```

2. **Install FastAPI dependencies**
   ```bash
   # Add FastAPI dependencies to your project
   uv add fastapi uvicorn python-multipart
   ```

3. **Alternative: Install with pip**
   ```bash
   pip install fastapi uvicorn python-multipart
   ```

## 📖 Usage

### Starting the Server

**Development Server:**
```bash
# Using uv
uv run uvicorn service:app --reload --host 0.0.0.0 --port 8000

# Traditional method
uvicorn service:app --reload --host 0.0.0.0 --port 8000
```

**Production Server:**
```bash
# Using uv with Gunicorn
uv run gunicorn service:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000

# Traditional method
gunicorn service:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

The API will be available at:
- **API Base URL**: `http://localhost:8000`
- **Interactive Docs**: `http://localhost:8000/docs`
- **Alternative Docs**: `http://localhost:8000/redoc`

### API Usage Examples

#### 1. Health Check
```bash
curl -X GET "http://localhost:8000/health"
```

**Response:**
```json
{
  "status": "ok"
}
```

#### 2. Single Prediction
```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'
```

**Response:**
```json
{
  "prediction": "setosa",
  "probabilities": {
    "setosa": 0.9876,
    "versicolor": 0.0123,
    "virginica": 0.0001
  }
}
```

#### 3. Batch Prediction
```bash
curl -X POST "http://localhost:8000/predict_batch" \
  -H "Content-Type: application/json" \
  -d '{
    "samples": [
      {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
      },
      {
        "sepal_length": 6.7,
        "sepal_width": 3.1,
        "petal_length": 4.7,
        "petal_width": 1.5
      }
    ]
  }'
```

**Response:**
```json
[
  {
    "prediction": "setosa",
    "probabilities": {
      "setosa": 0.9876,
      "versicolor": 0.0123,
      "virginica": 0.0001
    }
  },
  {
    "prediction": "versicolor",
    "probabilities": {
      "setosa": 0.0023,
      "versicolor": 0.8456,
      "virginica": 0.1521
    }
  }
]
```

#### 4. File Upload Prediction
```bash
curl -X POST "http://localhost:8000/predict_file" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@iris_sample.csv"
```

**Sample CSV format:**
```csv
sepal_length,sepal_width,petal_length,petal_width
5.1,3.5,1.4,0.2
6.7,3.1,4.7,1.5
5.8,2.7,5.1,1.9
```

## 📚 API Reference

### Request Models

#### Features
```python
class Features(BaseModel):
    sepal_length: float  # Sepal length in cm
    sepal_width: float   # Sepal width in cm
    petal_length: float  # Petal length in cm
    petal_width: float   # Petal width in cm
```

#### BatchRequest
```python
class BatchRequest(BaseModel):
    samples: List[Features]  # List of feature samples
```

### Response Models

#### PredictionResult
```python
class PredictionResult(BaseModel):
    prediction: str                    # Predicted species name
    probabilities: Dict[str, float]    # Prediction probabilities by class
```

### Endpoints Detail

#### `GET /`
**Description**: Welcome endpoint with API overview
**Response**: JSON object with welcome message and available endpoints

#### `GET /health`
**Description**: Health check endpoint for monitoring
**Response**: `{"status": "ok"}`

#### `POST /predict`
**Description**: Predict species for a single sample
**Request Body**: `Features` model
**Response**: `PredictionResult` model

#### `POST /predict_batch`
**Description**: Predict species for multiple samples
**Request Body**: `BatchRequest` model
**Response**: `List[PredictionResult]`

#### `POST /predict_file`
**Description**: Predict species from uploaded CSV file
**Request**: Multipart form data with CSV file
**Response**: List of prediction results
**File Requirements**: 
- Content type: `text/csv`
- Required columns: `sepal_length`, `sepal_width`, `petal_length`, `petal_width`

## ⚠️ Error Handling

The API provides comprehensive error handling:

### HTTP Status Codes
- `200`: Success
- `400`: Bad Request (invalid input data)
- `422`: Validation Error (invalid request format)
- `500`: Internal Server Error

### Example Error Response
```json
{
  "detail": "Only CSV files are accepted."
}
```

### Common Errors
1. **Invalid file type**: Only CSV files are accepted for file upload
2. **Missing features**: All four features must be provided
3. **Invalid data types**: Features must be numeric values
4. **Model not found**: Ensure the model is trained and saved

## 🌐 CORS Configuration

The API is configured with CORS middleware to allow cross-origin requests:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Allow all origins
    allow_methods=["POST", "GET"], # Allowed HTTP methods
    allow_headers=["Content-Type"], # Allowed headers
)
```

**Production Note**: Replace `allow_origins=["*"]` with specific domains for security.

## 🧪 Testing

Test the API using the interactive documentation at `http://localhost:8000/docs` or use curl commands as shown in the usage examples above.

## 🚀 Deployment

### Docker Deployment

Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "service:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t iris-api .
docker run -p 8000:8000 iris-api
```

### Cloud Deployment Options

1. **Heroku**: Use `Procfile` with `web: uvicorn service:app --host=0.0.0.0 --port=${PORT:-5000}`
2. **AWS Lambda**: Use Mangum adapter for serverless deployment
3. **Google Cloud Run**: Deploy with cloud-native scaling
4. **Azure Container Instances**: Easy container deployment

### Environment Variables
Set these environment variables for production:
- `MODEL_PATH`: Path to the trained model file
- `HOST`: Server host (default: 0.0.0.0)  
- `PORT`: Server port (default: 8000)

## ⚡ Performance

- **Single Prediction**: ~10-50ms response time
- **Batch Processing**: Scales linearly with sample count  
- **Memory Usage**: ~50-100MB per worker process
- Model is cached using `@lru_cache` for efficient memory usage

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/api-enhancement`)  
3. Add your improvements and update documentation
4. Commit your changes (`git commit -m 'Add API enhancement'`)
5. Push to the branch (`git push origin feature/api-enhancement`)
6. Open a Pull Request

## 👨‍💻 Author

**Utkarsh Gaikwad**

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Quick Start**: 
1. Train the model: `uv run main.py`
2. Start the API: `uv run uvicorn service:app --reload`
3. Visit `http://localhost:8000/docs` for interactive documentation
4. Test with: `curl -X GET "http://localhost:8000/health"`