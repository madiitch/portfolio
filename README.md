# Data Science and AI Portfolio

Portfolio of pharma, biotech, and healthcare-focused analytics projects built to show freelance-ready delivery: reproducible code, clear business framing, and lightweight demos a client can review quickly.

**Owner:** Zina Tevzadze

## What I Can Build

- NLP pipelines for clinical, regulatory, and medical text
- Pharmacovigilance and safety analytics prototypes
- Forecasting, MMM, and commercial analytics for biotech teams
- LLM-powered research summarization and decision-support tools
- Dashboards, notebooks, and stakeholder-friendly reporting

## Featured Projects

### 1. Clinical Trials NLP

Pipeline for downloading ClinicalTrials.gov studies, training a phase classifier, and extracting candidate trial endpoints from free text.

- Business use: accelerate trial landscape review and study triage
- Data: public ClinicalTrials.gov records
- Current artifact: baseline classifier report and endpoint extraction preview
- Result snapshot: holdout accuracy of `0.650` on the saved sample, with strongest performance on Phase 1 and Phase 2 studies
- Folder: [`clinical-trials-nlp`](./clinical-trials-nlp)

### 2. Pharmacovigilance Signal Detection

Prototype workflow for pulling adverse event reports from OpenFDA and calculating simple disproportionality metrics.

- Business use: early signal screening and safety review workflows
- Data: public OpenFDA / FAERS endpoints
- Focus: PRR-style signal scoring, quick CSV outputs, reproducible scripts
- Folder: [`pv-signal-detection`](./pv-signal-detection)

### 3. Biotech Bayesian MMM

Bayesian marketing mix modeling on synthetic launch data to estimate channel contribution and support budget allocation discussions.

- Business use: commercial planning, budget prioritization, launch analytics
- Data: synthetic weekly spend and sales data
- Focus: PyMC model fitting, posterior summaries, ROI-oriented storytelling
- Folder: [`biotech-mmm`](./biotech-mmm)

### 4. Literature Summarizer App

Interactive Streamlit app that turns technical medical text into a structured brief with methods, findings, limitations, and executive takeaways.

- Business use: literature review acceleration for biotech and healthcare teams
- Demo style: works as a no-API rule-based summarizer and can be extended to external model providers
- Folder: [`llm-lit-summarizer`](./llm-lit-summarizer)


## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run llm-lit-summarizer/app/streamlit_app.py
```

## Recommended Review Path

If you are evaluating this portfolio as a client or recruiter, start here:

1. Open the project READMEs to see the problem, workflow, and outputs
2. Review [`clinical-trials-nlp/reports/metrics.txt`](./clinical-trials-nlp/reports/metrics.txt) for a concrete saved result
3. Run the Streamlit summarizer for the fastest hands-on demo

## Repository Structure

```text
.
├── biotech-mmm/
├── clinical-trials-nlp/
├── llm-lit-summarizer/
├── pv-signal-detection/
├── requirements.txt
└── LICENSE
```

## Notes

- Public-data download helpers are included for ClinicalTrials.gov and OpenFDA.
- Some projects use lightweight baselines or synthetic data intentionally to keep the portfolio portable.
- Where a workflow is a prototype rather than a production-grade implementation, the README calls that out directly.
