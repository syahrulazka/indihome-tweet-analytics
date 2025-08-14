from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import torch
from transformers import BertTokenizer, BertForSequenceClassification
import re
import time
import logging
import psutil
import uvicorn
from contextlib import asynccontextmanager

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variables for model and tokenizer
model = None
tokenizer = None
device = None

class TextPreprocessor:
    def clean_text(self, text):
        if not text:
            return ""
        text = text.lower()
        text = re.sub(r'http\S+|www\S+|https\S+', '', text)
        text = re.sub(r'@\w+|#\w+', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

class SentimentRequest(BaseModel):
    text: str

class BatchSentimentRequest(BaseModel):
    texts: List[str]

class SentimentResponse(BaseModel):
    text: str
    predicted_label: str
    confidence: float
    probabilities: Dict[str, float]

class BatchSentimentResponse(BaseModel):
    results: List[SentimentResponse]

preprocessor = TextPreprocessor()

def load_model(model_path: str = "best_model"):
    global model, tokenizer, device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    try:
        tokenizer = BertTokenizer.from_pretrained(model_path)
        model = BertForSequenceClassification.from_pretrained(model_path).to(device)
        model.eval()
        logger.info(f"Model loaded from {model_path} on {device}")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise e

def predict_sentiment(text: str, max_length: int = 128) -> Dict[str, Any]:
    global model, tokenizer, device
    if model is None or tokenizer is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    cleaned_text = preprocessor.clean_text(text)
    if not cleaned_text:
        return {
            'text': text,
            'predicted_label': 'neutral',
            'confidence': 0.33,
            'probabilities': {'negative': 0.33, 'neutral': 0.34, 'positive': 0.33}
        }
    encoding = tokenizer(cleaned_text, truncation=True, padding='max_length', max_length=max_length, return_tensors='pt')
    input_ids = encoding['input_ids'].to(device)
    attention_mask = encoding['attention_mask'].to(device)
    with torch.no_grad():
        outputs = model(input_ids=input_ids, attention_mask=attention_mask)
        predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
        predicted_class = torch.argmax(predictions, dim=-1).item()
        confidence = predictions[0][predicted_class].item()
    label_map = {0: 'negative', 1: 'neutral', 2: 'positive'}
    return {
        'text': text,
        'predicted_label': label_map[predicted_class],
        'confidence': confidence,
        'probabilities': {
            'negative': predictions[0][0].item(),
            'neutral': predictions[0][1].item(),
            'positive': predictions[0][2].item()
        }
    }

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up: loading model...")
    load_model()
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="BERT Sentiment Analysis API",
    description="Sentiment analysis using a fine-tuned BERT model",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"{request.method} {request.url.path} - Status: {response.status_code} - Time: {duration:.2f}s")
    return response

@app.get("/")
async def root():
    return {"message": "BERT Sentiment Analysis API", "docs": "/docs"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if model else "unhealthy",
        "device": str(device),
        "cuda_available": torch.cuda.is_available()
    }

@app.get("/metrics")
async def get_metrics():
    return {
        "cpu_percent": psutil.cpu_percent(),
        "memory_percent": psutil.virtual_memory().percent,
        "gpu_memory": torch.cuda.memory_allocated() if torch.cuda.is_available() else None,
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=SentimentResponse)
async def predict(request: SentimentRequest):
    result = predict_sentiment(request.text)
    return SentimentResponse(**result)

@app.post("/predict_batch", response_model=BatchSentimentResponse)
async def predict_batch(request: BatchSentimentRequest):
    if len(request.texts) > 100:
        raise HTTPException(status_code=400, detail="Max 100 texts allowed")
    results = [SentimentResponse(**predict_sentiment(text)) for text in request.texts]
    return BatchSentimentResponse(results=results)

@app.get("/model_info")
async def model_info():
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    return {
        "model_name": "bert-base-uncased",
        "num_classes": 3,
        "classes": ["negative", "neutral", "positive"],
        "device": str(device),
        "parameters": sum(p.numel() for p in model.parameters()),
        "trainable_parameters": sum(p.numel() for p in model.parameters() if p.requires_grad)
    }

@app.get("/examples")
async def get_examples():
    return {
        "positive": ["Thanks Indihome, sekarang kerja dari rumah jadi lebih nyaman."],
        "neutral": ["Teknisi Indihome datang jam 10 pagi sesuai jadwal."],
        "negative": ["Internet Indihome gangguan terus, kerja jadi kacau!"]
    }

if __name__ == "__main__":
    uvicorn.run("fastapi_app:app", host="0.0.0.0", port=8000, reload=True)