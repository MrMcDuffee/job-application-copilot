import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import json

load_dotenv()
client = OpenAI()

# -----------------------------
# Helper
# -----------------------------
def run_agent(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content


def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        return {"error": text}


# -----------------------------
# Match Analysis
# -----------------------------
def analyze_match(job_text, resume_text):
    prompt = f"""
You are a hiring manager evaluating a candidate.

Return ONLY valid JSON:

{{
  "match_score": number from 0 to 100,
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
You are a resume optimizer.

IMPORTANT RULES:
- Only use information explicitly in the resume
- Do NOT invent experience
- You may rephrase and strengthen wording
- You may add keywords ONLY if clearly implied

TASK:
Rewrite the resume bullets to better match the job.

Focus on:
- AI / LLM alignment (if present)
- Systems thinking
- APIs and architecture
- Automation and scale
- Metrics and impact

Return ONLY bullet points.

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
You are a hiring manager.

Explain in 3-5 bullets:

- Why this candidate is strong (use evidence, not generic claims)
- How their background translates into AI/LLM product work
- What story they should tell in interviews

Rules:
- Be specific and grounded in the resume
- Avoid generic phrases like "strong fit", "excited", "aligned"
- Use concrete examples and metrics where possible

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
You are a hiring manager reviewing a resume.

Give specific, actionable improvements.

Rules:
- Only suggest REAL improvements (no generic advice)
- Be concise and practical
- Focus on high-impact changes

Return:
- Bullet point fixes
- Suggested wording improvements
- Missing metrics or clarity issues

JOB:
{job_text}

RESUME:
{resume_text}
"""
    return run_agent(prompt)


# -----------------------------
# UI
# -----------------------------
st.title("🧠 Job Application Copilot")

job_text = st.text_area("Paste Job Description")
resume_text = st.text_area("Paste Resume")

if st.button("Analyze"):
    if not job_text or not resume_text:
        st.warning("Please paste both job description and resume.")
    else:
        # Match Analysis
        st.subheader("📊 Match Analysis")
        match = analyze_match(job_text, resume_text)

        if "match_score" in match:
            score = match["match_score"]
            st.progress(score / 100)
            st.write(f"### Match Score: {score}%")

        st.json(match)

        # Optimized Bullets
        st.subheader("✍️ Optimized Resume Bullets")
        bullets = optimize_bullets(job_text, resume_text)
        st.write(bullets)

        # Strategic Positioning
        st.subheader("🧠 Strategic Positioning")
        positioning = get_positioning(job_text, resume_text)
        st.write(positioning)

        # Resume Fixes
        st.subheader("📌 Resume Fixes")
        fixes = suggest_fixes(job_text, resume_text)
        st.write(fixes)