from fastapi.testclient import TestClient
from app.api.main import app

# Creiamo un client di test (simula il browser)
client = TestClient(app)

def test_health_check():
    """Verifica che l'endpoint /health risponda status 200"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "model_loaded": True}

def test_prediction_positive():
    """Verifica che il modello riconosca un sentimento positivo"""
    payload = {"text": "I love this service, it is amazing!"}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    json_data = response.json()
    assert "sentiment" in json_data
    assert "confidence" in json_data
    # Ci aspettiamo che sia positivo (o almeno non negativo)
    assert json_data["sentiment"] == "positive"

def test_prediction_negative():
    """Verifica che il modello riconosca un sentimento negativo"""
    payload = {"text": "This is terrible, I hate it."}
    response = client.post("/predict", json=payload)
    
    assert response.status_code == 200
    assert response.json()["sentiment"] == "negative"


"""
scrivi sul terminale:   pytest    Serve per lanciare il test
Oppure: pytest -v per vedere tutti i dettagli

P.S: pytest agisce come un detective, quando lancio il comando scanziona la cartella corrente
e cerca file che iniziano con "test_" o finiscono con "_test.py", una volta entrato nel file lancia solo le funzioni che iniziano con "test_"
"""