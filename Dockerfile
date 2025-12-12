# 1. Usiamo un'immagine base ufficiale di Python (leggera e sicura)
FROM python:3.9-slim

# 2. Impostiamo la cartella di lavoro dentro il container
WORKDIR /code

# 3. Ottimizzazione della Cache:
# Copiamo PRIMA solo i requirements. Questo permette a Docker di non
# riscaricare tutte le librerie se cambi solo il codice ma non le dipendenze.
COPY ./requirements.txt /code/requirements.txt

# 4. Installiamo le dipendenze
# --no-cache-dir serve a mantenere l'immagine leggera
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# 5. Copiamo tutto il resto del codice dentro il container
COPY ./app /code/app

# 6. (Opzionale ma consigliato) Scarichiamo il modello durante la build
# In MLOps avanzato si fa per evitare che il container debba scaricare 
# 500MB ogni volta che si avvia.
# Creiamo un piccolo script inline per fare il "pre-load"
RUN python -c "from transformers import AutoTokenizer, AutoModelForSequenceClassification; \
    name='cardiffnlp/twitter-roberta-base-sentiment-latest'; \
    AutoTokenizer.from_pretrained(name); \
    AutoModelForSequenceClassification.from_pretrained(name)"

# 7) Hugging Face richiede la porta 7860
EXPOSE 7860

# Dobbiamo creare un utente non-root per sicurezza (Hugging Face lo gradisce molto)
RUN useradd -m -u 1000 user
USER user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

WORKDIR $HOME/app

COPY --chown=user . $HOME/app

# Copiamo lo script di avvio e lo rendiamo eseguibile
COPY --chown=user entrypoint.sh $HOME/app/entrypoint.sh
RUN chmod +x $HOME/app/entrypoint.sh

# Esponiamo la porta 7860 (quella di Streamlit/Hugging Face)
EXPOSE 7860

# Il nuovo comando di avvio è il nostro script
CMD ["./entrypoint.sh"]