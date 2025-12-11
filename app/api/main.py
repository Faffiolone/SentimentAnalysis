from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Importiamo l'istanza del modello che abbiamo appena creato
from app.model.loader import model_instance

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

# 3. Endpoint di default (la nostra Home che consiglia reindirizzamento a docs)
@app.get("/")
def home():
    return {"message": "Reputation Monitor API is running. Go to /docs for Swagger UI."}

# 4. Endpoint di Health Check (fondamentale per MLOps e Docker)
# Serve a capire se il container è vivo
@app.get("/health")
def health_check():
    # VERIFICA: Controlliamo se il modello è stato caricato in memoria
    if model_instance.model is not None:
        return {"status": "ok", "model_loaded": True}
    else:
        # Se il modello non c'è, restituiamo errore 503 (Service Unavailable)
        raise HTTPException(status_code=503, detail="Model not loaded yet")

# 5. Endpoint di Previsione (Dummy per ora)
@app.post("/predict", response_model=SentimentResponse)
def predict_sentiment(request: SentimentRequest):
    try:
        # Chiamiamo la funzione predict del nostro loader
        sentiment, confidence = model_instance.predict(request.text)
        
        return {
            "sentiment": sentiment,
            "confidence": confidence
        }
    except Exception as e:
        # Se qualcosa va storto, restituiamo errore 500
        raise HTTPException(status_code=500, detail=str(e))