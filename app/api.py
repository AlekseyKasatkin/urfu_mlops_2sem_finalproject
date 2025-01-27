from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
# from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import List, Dict
# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Настройка CORS
# origins = [
#     "http://localhost:3000",  # Добавьте адреса, которые должны иметь доступ к вашему API
#     "https://your-frontend-domain.com",
# ]
#
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Инициализация пайплайна анализа тональности
sentiment_pipeline = pipeline("sentiment-analysis")

class TextRequest(BaseModel):
    """
    Класс, определяющий формат входных данных для конечной точки analyze_sentiment.
    """
    print('hallo')
    texts: list[str]

@app.get("/")
async def read_root():
    return {"message": "Welcome to the sentiment analysis API!"}

@app.post("/analyze_sentiment/", response_model=list[dict])
async def analyze_sentiment(request: TextRequest):
    """
    принимает список текстовых строк в качестве входных данных и возвращает
    список результатов анализа тональности. Результаты анализа тональности
    представляют собой словари с ключами:
    - label (str): Метка тональности (положительная или отрицательная)
    - score (float): Оценка тональности
    """
    if not request.texts:
        logger.warning("Received an empty list of texts.")
        raise HTTPException(status_code=400, detail="The 'texts' list cannot be empty.")

    # Анализируем тональность входных текстов
    try:
        results = sentiment_pipeline(request.texts)
        logger.info(f"Sentiment analysis results: {results}")
        return results
    except Exception as e:
        logger.error(f"Error during sentiment analysis: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during sentiment analysis.")

# Запуск сервера
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
