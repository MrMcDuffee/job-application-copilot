import streamlit as st
from openai import OpenAI
import json

# -----------------------------
# OpenAI Client (WORKS LOCAL + CLOUD)
# -----------------------------
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# Helper
# -----------------------------
def run_agent(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "system", "content": "You are an expert hiring manager and resume coach."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"ERROR: {str(e)}"


def safe_json_parse(text):
    try:
        return json.loads(text)
    except Exception:
        return {
            "error": "invalid_json",
            "raw_output": text
        }


# -----------------------------
# Match Analysis
# -----------------------------
def analyze_match(job_text, resume_text):
    prompt = f"""
Return ONLY valid JSON:

{{
  "match_score": number (0-100),
  "summary": "short explanation",
  "top_strengths": [],
  "gaps": [],
  "missing_keywords": []
}}

JOB DESCRIPTION:
{job_text}

RESUME:
{resume_text}
"""
    return safe_json_parse(run_agent(prompt))


# -----------------------------
# Bullet Optimization
# -----------------------------
def optimize_bullets(job_text, resume_text):
    prompt = f"""
Rewrite resume bullets to improve clarity and alignment.

Rules:
- Do NOT invent experience
- Improve wording only
- Add keywords only if clearly supported

Return bullet points only.

JOB:
{job_text}

RESUME:
{resume_text}
"""
    return run_agent(prompt)


# -----------------------------
# Strategic Positioning
# -----------------------------
def get_positioning(job_text, resume_text):
    prompt = f"""
Give 3–5 strategic bullets:

- Why candidate is strong (use evidence)
- How experience maps to AI/LLM/product roles
- Interview narrative

Avoid generic language.

JOB:
{job_text}

RESUME:
{resume_text}
"""
    return run_agent(prompt)


# -----------------------------
# Resume Fix Suggestions
# -----------------------------
def suggest_fixes(job_text, resume_text):
    prompt = f"""
Give specific resume improvements.

Return:
- Bullet fixes
- Wording improvements
- Missing metrics

Be concise and actionable.

JOB:
{job_text}

RESUME:
{resume_text}
"""
    return run_agent(prompt)


# -----------------------------
# UI
# -----------------------------
st.set_page_config(page_title="Job Copilot", layout="wide")

st.title("🧠 Job Application Copilot")

job_text = st.text_area("Paste Job Description", height=200)
resume_text = st.text_area("Paste Resume", height=200)

if st.button("Analyze"):
    if not job_text.strip() or not resume_text.strip():
        st.warning("Please paste both job description and resume.")
        st.stop()

    # Match Analysis
    with st.spinner("Analyzing match..."):
        match = analyze_match(job_text, resume_text)

    st.subheader("📊 Match Analysis")

    if "match_score" in match and isinstance(match["match_score"], (int, float)):
        score = max(0, min(100, match["match_score"]))
        st.progress(score / 100)
        st.write(f"### Match Score: {score}%")

    st.json(match)

    # Optimized Bullets
    with st.spinner("Optimizing bullets..."):
        bullets = optimize_bullets(job_text, resume_text)

    st.subheader("✍️ Optimized Resume Bullets")
    st.write(bullets)

    # Strategic Positioning
    with st.spinner("Generating positioning..."):
        positioning = get_positioning(job_text, resume_text)

    st.subheader("🧠 Strategic Positioning")
    st.write(positioning)

    # Resume Fixes
    with st.spinner("Finding improvements..."):
        fixes = suggest_fixes(job_text, resume_text)

    st.subheader("📌 Resume Fixes")
    st.write(fixes)