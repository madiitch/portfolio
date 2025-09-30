import streamlit as st
import textwrap

st.set_page_config(page_title="Literature Summarizer", layout="wide")
st.title("LLM Literature Summarizer")

st.sidebar.header("Model Settings")
provider = st.sidebar.selectbox("Provider", ["echo-demo"])

st.markdown("""Paste one or more abstracts (or any long text). The app returns a structured summary with key findings and limitations.""")

text = st.text_area("Abstract(s)", height=250, placeholder="Paste abstract text here...")

def call_model(prompt: str, provider: str):
    # Placeholder for demo: echoes a compact version. Replace with your model call.
    return textwrap.shorten(prompt, width=500, placeholder="...")

if st.button("Summarize") and text.strip():
    with st.spinner("Summarizing..."):
        prompt = f"Summarize the following text into: 1) Key findings 2) Methods 3) Limitations 4) Takeaways for execs.\n\n{text}"
        out = call_model(prompt, provider)
        st.subheader("Summary")
        st.write(out)
        st.success("Swap `call_model` with your provider of choice.")
