import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = OpenAI()

SYSTEM_PROMPT = """
You are an expert technical recruiter and career coach.

You analyze resumes and job descriptions with precision.
You avoid generic advice and focus on specific, actionable insights.

You always:
- Use concise, structured outputs
- Preserve factual accuracy (do not invent experience)
- Optimize for clarity, impact, and alignment with the job description
"""

def safe_json_parse(text):
    try:
        return json.loads(text)
    except:
        print("\n⚠️ JSON parsing failed. Raw output below:\n")
        print(text)
        return {}

def run_agent(prompt):
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    return response.choices[0].message.content


# 1. Job Analyzer
def analyze_job(job_text):
    prompt = f"""
Analyze the following job description.

Return JSON with:
role_summary, required_skills, preferred_skills,
responsibilities, keywords, seniority_level

Job Description:
{job_text}
"""
    return safe_json_parse(run_agent(prompt))


# 2. Resume Analyzer
def analyze_resume(resume_text):
    prompt = f"""
Analyze the following resume.

Return JSON with:
experience_summary, skills, strengths,
weaknesses, bullet_points

Resume:
{resume_text}
"""
    return safe_json_parse(run_agent(prompt))


# 3. Gap Analysis
def gap_analysis(job_json, resume_json):
    prompt = f"""
Compare the candidate resume to the job description.

Return JSON with:
match_score, strengths_match, gaps,
missing_keywords, improvement_priorities

Job:
{job_json}

Resume:
{resume_json}
"""
    return safe_json_parse(run_agent(prompt))


# 4. Resume Optimizer
def optimize_resume(job_json, bullets):
    prompt = f"""
Rewrite and improve the candidate's resume bullets.

Rules:
- Do NOT fabricate experience
- Improve clarity and impact

Return JSON with:
optimized_bullets, improvement_notes

Job:
{job_json}

Bullets:
{bullets}
"""
    return safe_json_parse(run_agent(prompt))


# 5. Recruiter Score
def recruiter_score(job_json, optimized_bullets):
    prompt = f"""
Act as a recruiter.

Return JSON with:
final_score, hire_decision,
reasoning, red_flags, standout_points

Job:
{job_json}

Resume:
{optimized_bullets}
"""
    return safe_json_parse(run_agent(prompt))


# 6. Interview Questions
def interview_questions(job_json, gap_json):
    prompt = f"""
Generate interview questions.

Return JSON with:
behavioral_questions, technical_questions, gap_targeted_questions

Job:
{job_json}

Gaps:
{gap_json}
"""
    return safe_json_parse(run_agent(prompt))


if __name__ == "__main__":
    print("\n=== Job Application Copilot ===\n")

    job_text = input("Paste Job Description:\n")
    resume_text = input("\nPaste Resume:\n")

    print("\nAnalyzing...\n")

    job_json = analyze_job(job_text)
    resume_json = analyze_resume(resume_text)
    gap_json = gap_analysis(job_json, resume_json)
    optimized = optimize_resume(job_json, resume_json.get("bullet_points", []))
    score = recruiter_score(job_json, optimized.get("optimized_bullets", []))
    questions = interview_questions(job_json, gap_json)

    print("\n=== MATCH SCORE ===")
    print(json.dumps(score, indent=2))

    print("\n=== OPTIMIZED BULLETS ===")
    for b in optimized.get("optimized_bullets", []):
        print("-", b)

    print("\n=== INTERVIEW QUESTIONS ===")
    print(json.dumps(questions, indent=2))