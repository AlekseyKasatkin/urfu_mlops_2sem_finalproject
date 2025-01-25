from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
import uvicorn
app = FastAPI()

# initialize the sentiment analysis pipeline
sentiment_pipeline = pipeline("sentiment-analysis")

class TextRequest(BaseModel):
    """
    This class defines the input format for the analyze_sentiment endpoint.
    """

    texts: list[str]

# Определение маршрута для анализа тональности
@app.post("/analyze_sentiment/")
async def analyze_sentiment(request: TextRequest):
    """
    This endpoint takes a list of text strings as input and returns
    a list of sentimen
    t analysis results. The sentiment analysis results
    are dictionaries with the following keys:
    - label (str): The sentiment label (positive or negative)
    - score (float): The sentiment score
    """
    # Analyze the sentiment of the input texts
    results = sentiment_pipeline(request.texts)
    return results

# lounch server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
