---
title: Reputation Monitor
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
app_port: 7860
---

# 📊 End-to-End MLOps Pipeline for Real-Time Reputation Monitoring

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Model](https://img.shields.io/badge/model-RoBERTa-yellow)
![Deployment](https://img.shields.io/badge/deployed%20on-HuggingFace-orange)
![License](https://img.shields.io/badge/license-MIT-green)

## 🚀 Project Overview

**MachineInnovators Inc.** focuses on scalable, production-ready machine learning applications. This project is a comprehensive **MLOps solution** designed to monitor online company reputation through automated sentiment analysis of real-time news.

Unlike standard static notebooks, this repository demonstrates a **full-cycle ML workflow**. The system scrapes live data from **Google News**, analyzes sentiment using a **RoBERTa Transformer** model, and visualizes insights via an interactive dashboard, all orchestrated within a Dockerized environment.

### Key Features
* **Real-Time Data Ingestion:** Automated scraping of Google News for target brand keywords.
* **State-of-the-Art NLP:** Utilizes `twitter-roberta-base-sentiment` for high-accuracy classification.
* **Full-Stack Architecture:** Integrates a **FastAPI** backend for inference and a **Streamlit** frontend for visualization in a single container.
* **Automated Continuous Training (CT):** Implements a pipeline logic that checks for new data and simulates model fine-tuning during CI/CD execution.
* **CI/CD Automation:** Robust GitHub Actions pipeline for automated testing, building, and deployment to Hugging Face Spaces.
* **Embedded Monitoring:** Basic logging system to track model predictions and sentiment distribution over time.

---

## 🛠️ Tech Stack & Tools

* **Core:** Python 3.9+
* **Machine Learning:** Hugging Face Transformers, PyTorch, Scikit-learn.
* **Backend:** FastAPI, Uvicorn (REST API).
* **Frontend:** Streamlit (Interactive Dashboard).
* **Data Ingestion:** `GoogleNews` library (Real-time scraping).
* **DevOps:** Docker, GitHub Actions (CI/CD).
* **Deployment:** Hugging Face Spaces (Docker SDK).

---

## ⚙️ Architecture & MLOps Workflow

The project follows a rigorous MLOps pipeline to ensure reliability and speed of delivery:

1.  **Data & Modeling:**
    * **Input:** Real-time news titles and descriptions fetched dynamically.
    * **Model:** Pre-trained **RoBERTa** model optimized for social media and short-text sentiment.

2.  **Containerization (Docker):**
    * The application is containerized using a custom `Dockerfile`.
    * Implements a custom `entrypoint.sh` script to run both the **FastAPI backend** (port 8000) and **Streamlit frontend** (port 7860) simultaneously.

3.  **CI/CD Pipeline (GitHub Actions):**
    * **Trigger:** Pushes to the `main` branch.
    * **Continuous Training:** Checks the `data/` directory for new labeled datasets. If found, initiates a training simulation to demonstrate the retraining lifecycle.
    * **Test:** Executes `pytest` suite to verify API endpoints (`/health`, `/analyze`) and model loading.
    * **Build:** Verifies Docker image creation.
    * **Deploy:** Automatically pushes the validated code to Hugging Face Spaces.

4.  **Monitoring:**
    * The system logs every prediction to a local CSV file, which is visualized in the "Monitoring" tab of the dashboard.

---

## 📂 Repository Structure

```bash
├── .github/workflows/   # CI/CD configurations (GitHub Actions)
├── app/                 # Backend Application Code
│   ├── api/             # FastAPI endpoints (main.py)
│   ├── model/           # Model loader logic (RoBERTa)
│   └── services/        # Google News scraping logic
├── data/                # Dataset storage for retraining
├── streamlit_app/       # Frontend Application Code (app.py)
├── src/                 # Training scripts (Simulation)
├── tests/               # Unit and integration tests (Pytest)
├── Dockerfile           # Container configuration
├── entrypoint.sh        # Startup script for dual-process execution
├── requirements.txt     # Project dependencies
├── Appunti_Progetto.doc # Note and explanation of the project
└── README.md            # Project documentation


💻 Installation & Usage
To run this project locally using Docker (Recommended):

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/SentimentAnalysis.git](https://github.com/YOUR_USERNAME/SentimentAnalysis.git)
cd SentimentAnalysis

### 2. Build the Docker Image
```bash
docker build -t reputation-monitor .

### 3. Run the Container
```bash
docker run -p 7860:7860 reputation-monitor
Access the application at http://localhost:7860

Manual Installation (No Docker):
If you prefer running it directly with Python:

    1. Install dependencies:

    ```bash
    pip install -r requirements.txt

    2. Start the Backend (FastAPI):

    ```bash
    uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

    3. Start the Frontend (Streamlit) in a new terminal:

    ```bash
    streamlit run streamlit_app/app.py

⚠️ Limitations & Future Roadmap
Data Persistence: Currently, monitoring logs are stored in an ephemeral CSV file. In a production environment, this would be replaced by a persistent database (e.g., PostgreSQL) to ensure data retention across container restarts.

Scalability: The current Google News scraper is synchronous. Future versions will implement asynchronous scraping (aiohttp) or a message queue (RabbitMQ/Celery) for high-volume processing.

Model Retraining: A placeholder pipeline (src/train.py) is included. Full implementation would require GPU resources and a labeled dataset for fine-tuning.

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📝 License
Distributed under the MIT License. See LICENSE for more information.

---

### 👤 Author

**Fabio Celaschi**

<a href="https://www.linkedin.com/in/fabio-celaschi-4371bb92">
  <img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" />
</a>

<a href="https://www.instagram.com/fabiocelaschi/">
  <img src="https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram" />
</a>
