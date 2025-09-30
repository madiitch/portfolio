# Data Science & AI Portfolio

This repository showcases end-to-end projects in data science, analytics, and AI with a focus on pharmaceutical and biotech use cases. It contains reproducible code, documentation, and lightweight apps suitable for demonstrating capabilities on Upwork.

**Owner:** _Your Name_  
**Created:** 2025-09-30

## Projects

1. **clinical-trials-nlp/** – NLP pipeline that ingests ClinicalTrials.gov data, cleans text, and fine-tunes a classifier to predict study phase and extract endpoints (NER).  
2. **pv-signal-detection/** – Pharmacovigilance signal detection using FAERS/OpenFDA data with disproportionality analyses (PRR/ROR/Bayes).  
3. **biotech-mmm/** – Bayesian Marketing Mix Modeling on synthetic biotech launch data; elasticity, ROI, and budget reallocation.  
4. **llm-lit-summarizer/** – Streamlit app that summarizes medical abstracts and produces key insights; supports local/hosted LLMs via an adapter pattern.

## Getting Started

```bash
# (1) create environment
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate

# (2) install base requirements
pip install -r requirements.txt

# (3) run an example app
streamlit run llm-lit-summarizer/app/streamlit_app.py
```

## Repo Structure

```
.
├── clinical-trials-nlp/
├── pv-signal-detection/
├── biotech-mmm/
├── llm-lit-summarizer/
├── requirements.txt
├── .gitignore
└── LICENSE
```

## Notes

- Where public data is accessed (ClinicalTrials.gov, OpenFDA/FAERS), scripts include simple download helpers.  
- Each project folder has its own README with objectives, methods, and "How to run".  
- This repo favors clarity and business relevance: every model includes evaluation and a short report / slide-ready summary.

