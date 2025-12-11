from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import csv
import os
from datetime import datetime

# Importiamo l'istanza del modello e l'istanza di GoogleNews per ricerca news
from app.model.loader import model_instance
from app.services.news_client import news_instance # Assicurati che il file si chiami news_client.py

# 1. Inizializziamo l'app
app = FastAPI(
    title="Reputation Monitor API",
    description="API per l'analisi del sentiment della reputazione aziendale sulla base di news estrapolate con Google di un azienda/soggetto dato in input",
    version="1.0.0"
)

# --- MONITORAGGIO (Logging su CSV) ---
LOG_FILE = "reputation_logs.csv"
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["timestamp", "query", "text", "sentiment", "confidence"])

def log_prediction(query, text, sentiment, confidence):
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), query, text, sentiment, confidence])

# --- MODELLI DATI (Pydantic) ---
class AnalysisRequest(BaseModel):
    query: str # Es. "Tesla"
    limit: int = 5

class SingleResult(BaseModel):
    text: str
    sentiment: str
    confidence: float

class AnalysisResponse(BaseModel):
    query: str
    results: List[SingleResult]
    summary: dict # Es. {"positive": 3, "negative": 1}

# --- ENDPOINTS ---

@app.get("/health")
def health_check():
    # VERIFICA: Controlliamo se il modello è stato caricato in memoria
    if model_instance.model is not None:
        return {"status": "ok", "model_loaded": True}
    raise HTTPException(status_code=503, detail="Model not loaded")

@app.post("/analyze", response_model=AnalysisResponse)
def analyze_company(request: AnalysisRequest):
    # --- DEBUG PRINT ---
    print(f"🔥 API RECEIVED REQUEST -> Query: {request.query}, Limit: {request.limit}") 
    # -------------------
    """
    1. Cerca news su Google
    2. Analizza il sentiment di ogni news
    3. Salva i log
    4. Restituisce il report completo
    """
    try:
        # 1. Scarica le News
        news_texts = news_instance.search_news(request.query, limit=request.limit)
        
        if not news_texts:
            return {"query": request.query, "results": [], "summary": {}}

        analyzed_results = []
        sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}

        # 2. Analizza ogni notizia col Modello
        for text in news_texts:
            sentiment, confidence = model_instance.predict(text)
            
            # Aggiorna conteggi
            sentiment_counts[sentiment] += 1
            
            # Aggiungi alla lista
            analyzed_results.append({
                "text": text,
                "sentiment": sentiment,
                "confidence": confidence
            })
            
            # 3. Logga per il monitoraggio (Punto 2 dell'esercizio)
            log_prediction(request.query, text, sentiment, confidence)

        return {
            "query": request.query,
            "results": analyzed_results,
            "summary": sentiment_counts
        }

    except Exception as e:
        # Se qualcosa va storto, restituiamo errore 500
        raise HTTPException(status_code=500, detail=str(e))