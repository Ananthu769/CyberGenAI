import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")


def analyze_security(summary, events):
    prompt = f"""
You are a cybersecurity expert.

Analyze the following security log summary.

Summary:
{summary}

Events:
{events}

Provide:
1. Executive Summary
2. Threat Level (Low/Medium/High/Critical)
3. Key Findings
4. Possible Attack Pattern
5. MITRE ATT&CK Techniques (if applicable)
6. Recommendations

Respond in clean markdown.
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Analysis Error: {str(e)}"