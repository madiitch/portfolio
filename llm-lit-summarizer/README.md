# Literature Summarizer App

Interactive Streamlit demo for turning medical or biotech text into a fast structured brief.

## Why It Is Useful

Clients often need a first-pass review of abstracts, trial descriptions, or technical notes without waiting for a custom NLP pipeline. This app shows that workflow in a lightweight format.

## Features

- rule-based summarization that works without an API key
- structured sections for methods, findings, limitations, and executive takeaways
- evidence extraction for numbers, dosing, percentages, and study-scale details
- downloadable markdown brief for client sharing

## How to Run

Run from inside `llm-lit-summarizer/`:

```bash
pip install -r ../requirements.txt
streamlit run app/streamlit_app.py
```

## Extension Path

The app is built so a real model provider can be swapped in later. For client demos, the current rule-based version keeps the portfolio runnable even without external API access.
