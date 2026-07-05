import sqlite3

DATABASE = "cybergenai.db"


def create_database():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            filename TEXT,

            total_events INTEGER,

            risk TEXT,

            risk_score INTEGER,

            report TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
    """)

    conn.commit()

    conn.close()


def save_report(filename, summary, risk, score, report):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO reports(

        filename,

        total_events,

        risk,

        risk_score,

        report

        )

        VALUES(?,?,?,?,?)

    """,

    (

        filename,

        summary["total_events"],

        risk,

        score,

        report

    )

    )

    conn.commit()

    conn.close()


def get_reports():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute("""

        SELECT

        id,

        filename,

        total_events,

        risk,

        risk_score,

        created_at

        FROM reports

        ORDER BY id DESC

    """)

    reports = cursor.fetchall()

    conn.close()

    return reports


def get_single_report(report_id):

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute(

        "SELECT * FROM reports WHERE id=?",

        (report_id,)

    )

    report = cursor.fetchone()

    conn.close()

    return report