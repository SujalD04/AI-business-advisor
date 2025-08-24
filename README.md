---

# AI-Powered Business Advisor

An interactive **Streamlit web application** that helps startup founders analyze their business metrics, predict growth, generate tailored strategies, and visualize performance — all powered by **machine learning, clustering, and LLMs (Gemini AI)**.

---

## Features

* **Form Input** – Enter your startup’s financials & metrics.
* **Growth Prediction** – Regression model estimates business growth.
* **Startup Clustering** – Groups startups into clusters (0,1,2) for benchmarking.
* **Interactive Dashboard** – Visualize KPIs, industry breakdowns, and clusters.
* **Reports** – Export structured reports for investors/advisors.
* **Ask Gemini** – Chat with an AI assistant for tailored insights & recommendations.
* **Postgres Integration** – Persist startup data for portfolio analysis.

---

## Tech Stack

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend / Database**: PostgreSQL + SQLAlchemy
* **Machine Learning**: scikit-learn (Regression + Clustering)
* **Chatbot (LLM)**: Google Gemini (via `utils/gemini_helper.py`)
* **Visualization**: Matplotlib, Streamlit charts

---

## Project Structure

```
business-advisor/
│── app.py                  # Main Streamlit app
│── config.py               # Database & API config
│── requirements.txt        # Dependencies
│── .env.example            # Example env vars
│── utils/                  # Helper functions
│   ├── preprocessing.py
│   ├── strategy_engine.py
│   ├── nlp_summarizer.py
│   ├── report_generator.py
│   └── gemini_helper.py
│── models/                 # ML models
│   ├── regression_model.py
│   ├── clustering_model.py
│   └── startups_data.csv   # Synthetic dataset
│── dashboard.py            # Dashboard visualization
└── README.md
```

---

## Setup & Installation

### 1. Clone the repo

```bash
git clone https://github.com/your-username/business-advisor.git
cd business-advisor
```

### 2. Create & activate virtual environment

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` → `.env` and fill in:

```ini
# Database
DATABASE_URL=postgresql+psycopg2://user:password@localhost:5432/businessdb

# Google Gemini API
GEMINI_API_KEY=your_api_key_here
```

### 5. Run the app

```bash
streamlit run app.py
```

---

## Usage Flow

1. Go to **Form Input** → enter startup details.
2. Get instant **growth prediction & clustering**.
3. Explore portfolio in the **Dashboard**.
4. Generate structured **Reports**.
5. Chat with **Ask Gemini** for strategy & advice.

---

## Roadmap

* Add authentication (multi-user support)
* Expand industry-specific strategies
* Deploy on cloud (Streamlit Cloud / AWS / GCP)
* Support PDF export of reports

---

## Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to add.

---

## License

MIT License © 2025 Sujal Dixit

---

