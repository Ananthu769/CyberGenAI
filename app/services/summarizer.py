from collections import Counter


def summarize_events(events):

    summary = {
        "total_events": len(events),
        "failed_login": 0,
        "successful_login": 0,
        "sql_injection": 0,
        "xss": 0,
        "firewall": 0,
        "port_scan": 0,
        "malware": 0,
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }

    ips = Counter()

    for event in events:

        ips[event["ip"]] += 1

        if event["type"] == "Failed Login":
            summary["failed_login"] += 1

        elif event["type"] == "Successful Login":
            summary["successful_login"] += 1

        elif event["type"] == "SQL Injection":
            summary["sql_injection"] += 1

        elif event["type"] == "Cross Site Scripting":
            summary["xss"] += 1

        elif event["type"] == "Firewall Block":
            summary["firewall"] += 1

        elif event["type"] == "Port Scan":
            summary["port_scan"] += 1

        elif event["type"] == "Malware":
            summary["malware"] += 1

        if event["severity"] == "Critical":
            summary["critical"] += 1

        elif event["severity"] == "High":
            summary["high"] += 1

        elif event["severity"] == "Medium":
            summary["medium"] += 1

        else:
            summary["low"] += 1

    summary["top_ips"] = ips.most_common(5)

    return summary