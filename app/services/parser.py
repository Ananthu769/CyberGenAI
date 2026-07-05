import re


def parse_log(file_path):

    events = []

    with open(file_path, "r", encoding="utf-8", errors="ignore") as file:

        for line in file:

            line = line.strip()

            ip_match = re.search(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", line)

            ip = ip_match.group(0) if ip_match else "Unknown"

            event_type = "Other"

            severity = "Low"

            if "Failed password" in line:
                event_type = "Failed Login"
                severity = "Medium"

            elif "Accepted password" in line:
                event_type = "Successful Login"
                severity = "Info"

            elif "SQL Injection" in line:
                event_type = "SQL Injection"
                severity = "Critical"

            elif "XSS" in line:
                event_type = "Cross Site Scripting"
                severity = "High"

            elif "denied" in line.lower():
                event_type = "Firewall Block"
                severity = "Medium"

            elif "port scan" in line.lower():
                event_type = "Port Scan"
                severity = "High"

            elif "malware" in line.lower():
                event_type = "Malware"
                severity = "Critical"

            events.append(
                {
                    "raw": line,
                    "ip": ip,
                    "type": event_type,
                    "severity": severity
                }
            )

    return events