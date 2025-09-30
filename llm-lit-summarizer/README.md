# LLM Literature Summarizer

**Goal:** A Streamlit app that summarizes medical/biotech abstracts and outputs bullet insights with citations you provide.

**Why:** Clients often want quick, structured takeaways from papers without deep model-building.

## How to Run

```bash
pip install -r ../../requirements.txt
streamlit run app/streamlit_app.py
```

## Notes
- The app uses a simple adapter: you can plug in OpenAI, local models, or HuggingFace endpoints by implementing a single function.
