#!/bin/bash

# 1. Avvia il Backend (FastAPI) in background
# Usiamo la '&' alla fine per dirgli "non bloccare il terminale, vai in background"
# Lo facciamo girare sulla porta 8000 interna
echo "🚀 Starting FastAPI backend..."
uvicorn app.api.main:app --host 0.0.0.0 --port 8000 &

# 2. Aspettiamo qualche secondo che l'API si avvii
sleep 5

# 3. Avvia il Frontend (Streamlit) in primo piano
# Streamlit DEVE usare la porta 7860 perché è l'unica che Hugging Face espone al pubblico
echo "🎨 Starting Streamlit frontend..."
streamlit run streamlit_app/app.py --server.port 7860 --server.address 0.0.0.0