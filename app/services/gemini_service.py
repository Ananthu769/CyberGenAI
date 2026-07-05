import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_security(summary, events):

    prompt = f"""
You are an experienced SOC (Security Operations Center) analyst.

Analyze the following cybersecurity incident.

Summary

Total Events: {summary["total_events"]}

Failed Logins: {summary["failed_login"]}

Successful Logins: {summary["successful_login"]}

SQL Injection: {summary["sql_injection"]}

Cross Site Scripting: {summary["xss"]}

Firewall Blocks: {summary["firewall"]}

Port Scan: {summary["port_scan"]}

Malware: {summary["malware"]}

Log Events

{events}

Generate a professional report using markdown.

Use this format exactly.

# Executive Summary

# Severity Assessment

# Attack Analysis

# MITRE ATT&CK Mapping

# Indicators of Compromise

# Recommendations

# Conclusion

Keep the report concise and professional.
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:

        return f"""
# AI Report

Gemini API could not generate the report.

Reason

{str(e)}

The local analysis completed successfully.
"""