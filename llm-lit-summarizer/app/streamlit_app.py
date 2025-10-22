import re
from collections import Counter

import streamlit as st


SAMPLE_ABSTRACT = """
Background: Patients with metastatic non-small cell lung cancer often require treatment sequencing decisions under significant uncertainty.
Methods: In this multicenter retrospective cohort study, investigators reviewed 214 adults treated across 6 oncology centers between January 2021 and March 2024. The primary endpoint was progression-free survival at 12 months. Secondary endpoints included overall survival, grade 3 or higher adverse events, and treatment discontinuation. Patients receiving biomarker-guided therapy were compared with standard sequencing using adjusted Cox models.
Results: Median progression-free survival was 11.8 months in the biomarker-guided group versus 8.6 months in the standard group. The adjusted hazard ratio was 0.74 with a 95% confidence interval of 0.58 to 0.94. Grade 3 or higher adverse events occurred in 17% of patients versus 23%, respectively. Treatment discontinuation occurred in 12% and 19% of patients.
Limitations: The study was retrospective, non-randomized, and subject to residual confounding. Sample size was moderate, and subgroup analyses were underpowered.
Conclusion: Biomarker-guided sequencing was associated with longer progression-free survival and a lower severe adverse event burden, but prospective validation is still needed.
""".strip()

STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "was",
    "were",
    "with",
}

METHOD_KEYWORDS = {
    "study",
    "trial",
    "cohort",
    "randomized",
    "retrospective",
    "prospective",
    "multicenter",
    "phase",
    "patients",
    "participants",
    "model",
}
RESULT_KEYWORDS = {
    "result",
    "improved",
    "reduced",
    "increase",
    "decrease",
    "survival",
    "endpoint",
    "hazard",
    "response",
    "significant",
    "%",
    "months",
}
LIMITATION_KEYWORDS = {
    "limitation",
    "bias",
    "confounding",
    "retrospective",
    "underpowered",
    "single-center",
    "single center",
    "small",
    "short follow-up",
    "non-randomized",
    "generalizability",
}


def split_sentences(text: str) -> list[str]:
    clean = re.sub(r"\s+", " ", text).strip()
    if not clean:
        return []
    parts = re.split(r"(?<=[.!?])\s+", clean)
    return [part.strip() for part in parts if part.strip()]


def tokenize(text: str) -> list[str]:
    return re.findall(r"[A-Za-z][A-Za-z\-]+", text.lower())


def top_terms(text: str, limit: int = 8) -> list[str]:
    counts = Counter(
        token for token in tokenize(text) if token not in STOPWORDS and len(token) > 3
    )
    return [word for word, _ in counts.most_common(limit)]


def sentence_score(sentence: str, focus_terms: list[str]) -> int:
    lower = sentence.lower()
    score = 0
    score += sum(1 for term in focus_terms if term in lower)
    score += sum(1 for keyword in METHOD_KEYWORDS if keyword in lower)
    score += sum(1 for keyword in RESULT_KEYWORDS if keyword in lower)
    score += len(re.findall(r"\b\d+(?:\.\d+)?\b", sentence))
    return score


def pick_sentences(sentences: list[str], keywords: set[str], limit: int) -> list[str]:
    picked = [sentence for sentence in sentences if any(word in sentence.lower() for word in keywords)]
    return picked[:limit]


def extract_evidence(text: str, limit: int = 8) -> list[str]:
    patterns = [
        r"\b\d+(?:\.\d+)?%\b",
        r"\b\d+(?:\.\d+)?\s+(?:months?|weeks?|days?|patients?|participants?|subjects?|centers?)\b",
        r"\b(?:hazard ratio|odds ratio|risk ratio|confidence interval|p-value|p value)\b[^.]*",
        r"\b(?:phase\s+[ivx0-9/]+|grade\s+\d+)\b[^.]*",
        r"\bprimary endpoint\b[^.]*",
        r"\bsecondary endpoints?\b[^.]*",
    ]
    evidence = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            snippet = match.group(0).strip(" ;,")
            if snippet not in evidence:
                evidence.append(snippet)
            if len(evidence) >= limit:
                return evidence
    return evidence


def build_summary(text: str, audience: str, max_bullets: int) -> dict[str, list[str] | str]:
    sentences = split_sentences(text)
    if not sentences:
        return {
            "overview": "",
            "methods": [],
            "findings": [],
            "limitations": [],
            "takeaways": [],
            "evidence": [],
            "keywords": [],
        }

    keywords = top_terms(text)
    ranked = sorted(sentences, key=lambda sentence: sentence_score(sentence, keywords), reverse=True)
    overview = ranked[0] if ranked else sentences[0]

    methods = pick_sentences(sentences, METHOD_KEYWORDS, max_bullets)
    findings = pick_sentences(sentences, RESULT_KEYWORDS, max_bullets)
    limitations = pick_sentences(sentences, LIMITATION_KEYWORDS, max_bullets)

    if not methods:
        methods = ranked[: min(2, len(ranked))]
    if not findings:
        findings = ranked[: min(max_bullets, len(ranked))]
    if not limitations:
        limitations = ["No explicit limitation sentence was detected in the provided text."]

    if audience == "Executive":
        takeaways = [
            "The text suggests a practical business or clinical implication rather than only a statistical result.",
            "Key quantitative signals were extracted below so a client can scan impact quickly.",
            "Any recommendation should still be checked against study design quality and stated limitations.",
        ]
    elif audience == "Technical":
        takeaways = [
            "Focus on whether the study design supports the claimed effect size.",
            "Review extracted evidence terms for endpoints, sample size, and reported comparative metrics.",
            "Treat missing methodological details as a signal for follow-up review rather than a final conclusion.",
        ]
    else:
        takeaways = [
            "This brief condenses the main study design, result direction, and explicit caution points.",
            "Quantitative evidence is surfaced separately to speed manual review.",
            "The summary should be used as a first-pass screen before domain expert interpretation.",
        ]

    return {
        "overview": overview,
        "methods": methods[:max_bullets],
        "findings": findings[:max_bullets],
        "limitations": limitations[:max_bullets],
        "takeaways": takeaways[:max_bullets],
        "evidence": extract_evidence(text, limit=max_bullets + 3),
        "keywords": keywords,
    }


def to_markdown(summary: dict[str, list[str] | str]) -> str:
    sections = [
        "# Literature Brief",
        "",
        "## Overview",
        str(summary["overview"]),
        "",
        "## Methods",
    ]
    sections.extend(f"- {item}" for item in summary["methods"])
    sections.extend(["", "## Findings"])
    sections.extend(f"- {item}" for item in summary["findings"])
    sections.extend(["", "## Limitations"])
    sections.extend(f"- {item}" for item in summary["limitations"])
    sections.extend(["", "## Executive Takeaways"])
    sections.extend(f"- {item}" for item in summary["takeaways"])
    sections.extend(["", "## Evidence Extracts"])
    evidence = summary["evidence"] or ["No explicit evidence snippets detected."]
    sections.extend(f"- {item}" for item in evidence)
    return "\n".join(sections)


st.set_page_config(page_title="Literature Summarizer", page_icon=":microscope:", layout="wide")

st.title("Literature Summarizer")
st.caption("A client-friendly demo that turns dense medical text into a structured review brief.")

with st.sidebar:
    st.header("Review Settings")
    audience = st.selectbox("Audience", ["Executive", "Mixed", "Technical"])
    max_bullets = st.slider("Bullets per section", min_value=2, max_value=5, value=3)
    use_sample = st.button("Load Sample Abstract")
    st.markdown(
        """
        **How this demo works**

        - No API key required
        - Uses rule-based extraction for a reliable offline demo
        - Can later be swapped for an external LLM provider
        """
    )

if use_sample and "source_text" not in st.session_state:
    st.session_state["source_text"] = SAMPLE_ABSTRACT
elif use_sample:
    st.session_state["source_text"] = SAMPLE_ABSTRACT

default_text = st.session_state.get("source_text", "")

text = st.text_area(
    "Paste an abstract, trial summary, or technical note",
    value=default_text,
    height=320,
    placeholder="Paste medical or biotech text here...",
)
st.session_state["source_text"] = text

left, right = st.columns([3, 2])

with left:
    st.subheader("Source Text")
    st.write(
        "Use this to demonstrate how you can turn unstructured research text into a quick decision-support brief."
    )

with right:
    st.subheader("What the client gets")
    st.write(
        "A compact review with methods, key findings, limitations, evidence snippets, and a downloadable markdown summary."
    )

if st.button("Generate Brief", type="primary"):
    if not text.strip():
        st.warning("Add some source text first so the app has something to summarize.")
    else:
        summary = build_summary(text, audience=audience, max_bullets=max_bullets)
        markdown_brief = to_markdown(summary)

        overview_tab, evidence_tab, download_tab = st.tabs(
            ["Structured Brief", "Evidence", "Download"]
        )

        with overview_tab:
            st.subheader("Overview")
            st.write(summary["overview"])

            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### Methods")
                for item in summary["methods"]:
                    st.markdown(f"- {item}")

                st.markdown("### Limitations")
                for item in summary["limitations"]:
                    st.markdown(f"- {item}")

            with col2:
                st.markdown("### Findings")
                for item in summary["findings"]:
                    st.markdown(f"- {item}")

                st.markdown("### Executive Takeaways")
                for item in summary["takeaways"]:
                    st.markdown(f"- {item}")

        with evidence_tab:
            st.subheader("Extracted Evidence")
            evidence = summary["evidence"] or ["No explicit evidence snippets detected."]
            for item in evidence:
                st.markdown(f"- {item}")

            st.subheader("Top Keywords")
            st.write(", ".join(summary["keywords"]) if summary["keywords"] else "No keywords extracted.")

        with download_tab:
            st.subheader("Client-Ready Markdown")
            st.code(markdown_brief, language="markdown")
            st.download_button(
                label="Download Brief",
                data=markdown_brief,
                file_name="literature_brief.md",
                mime="text/markdown",
            )

        st.success("Structured brief generated.")
