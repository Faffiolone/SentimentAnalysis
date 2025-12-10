from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 1. Inizializziamo l'app
app = FastAPI(
    title="Reputation Monitor API",
    description="API per l'analisi del sentiment della reputazione aziendale",
    version="1.0.0"
)

# 2. Definiamo il "modello dei dati" in input (Data Validation)
# Questo serve a garantire che chi chiama l'API mandi i dati giusti
class SentimentRequest(BaseModel):
    text: str
    language: str = "it"  # default italiano

class SentimentResponse(BaseModel):
    sentiment: str
    confidence: float

# 3. Endpoint di Health Check (fondamentale per MLOps e Docker)
# Serve a capire se il container è vivo
@app.get("/health")
def health_check():
    return {"status": "ok", "message": "Service is running"}

# 4. Endpoint di Previsione (Dummy per ora)
@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    """
    Riceve un testo e restituisce il sentiment (Positive, Neutral, Negative).
    """
    # TODO: Qui caricheremo il modello ML vero!
    # Per ora simuliamo una risposta logica
    print(f"Analyzing text: {request.text}")
    
    # Logica finta (Mock) per testare l'API
    mock_sentiment = "neutral"
    if "ottimo" in request.text.lower():
        mock_sentiment = "positive"
    elif "pessimo" in request.text.lower():
        mock_sentiment = "negative"
        
    return {
        "sentiment": mock_sentiment,
        "confidence": 0.95
    }