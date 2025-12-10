from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoConfig
import numpy as np
from scipy.special import softmax

# Questo è il modello specifico richiesto dall'esercizio
MODEL_NAME = "cardiffnlp/twitter-roberta-base-sentiment-latest"

class SentimentModel:
    def __init__(self):
        print(f"🔄 Loading model: {MODEL_NAME}...")
        # Scarichiamo Tokenizer (trasforma testo in numeri) e Modello (Rete Neurale)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
        self.config = AutoConfig.from_pretrained(MODEL_NAME)
        self.model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        print("✅ Model loaded successfully!")

    def predict(self, text: str):
        # 1. Preprocessing
        # Trasformiamo il testo in input per RoBERTa (truncation=True taglia i tweet troppo lunghi)
        encoded_input = self.tokenizer(text, return_tensors='pt', truncation=True, max_length=512)
        
        # 2. Inferenza (Il passaggio nella rete neurale)
        output = self.model(**encoded_input)
        
        # 3. Post-processing
        # L'output sono "logits" (punteggi grezzi), usiamo Softmax per avere probabilità (0-1)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        
        # 4. Mappatura Etichette
        # Questo modello specifico usa l'ordine: 0 -> Negative, 1 -> Neutral, 2 -> Positive
        labels = ["negative", "neutral", "positive"]
        
        # Troviamo l'indice con il punteggio più alto
        ranking = np.argsort(scores)
        ranking = ranking[::-1] # Ordiniamo decrescente
        
        top_label_id = ranking[0]
        top_label = labels[top_label_id]
        confidence = scores[top_label_id]
        
        return top_label, float(confidence)

# Istanziamo il modello UNA VOLTA sola qui. 
# Quando importiamo 'model_instance' negli altri file, sarà già caricato.
model_instance = SentimentModel()