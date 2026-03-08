import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

from agents.summary_agent import SummaryAgent
from agents.blocker_agent import BlockerDetectorAgent
from agents.sprint_progress_agent import SprintProgressEstimatorAgent
from memory.standup_db import save_update, get_updates_by_day, get_updates_by_sprint

st.set_page_config(page_title="Agile Team Standup Tracker", layout="wide")

summary_agent = SummaryAgent()
blocker_agent = BlockerDetectorAgent()
progress_agent = SprintProgressEstimatorAgent()

EXPORT_DIR = Path("exports")
EXPORT_DIR.mkdir(exist_ok=True)

st.title("Agile Team Standup Tracker")
st.subheader("AI-Powered Asynchronous Standups")

menu = st.sidebar.selectbox(
    "Choose Option",
    ["Submit Update", "Daily Digest", "Sprint History", "About"]
)

if menu == "Submit Update":
    st.header("Submit Daily Standup")

    sprint = st.text_input("Sprint Name", "Sprint 12")
    standup_date = st.date_input("Standup Date")
    member_name = st.text_input("Team Member Name", "Ramya")
    yesterday = st.text_area("What did you complete yesterday?", "Finished API integration for sprint board updates.")
    today = st.text_area("What will you work on today?", "Work on export feature for weekly digest.")
    blocker = st.text_area("Any blockers?", "Waiting for frontend payload format confirmation.")

    if st.button("Save Update"):
        save_update(
            sprint=sprint,
            date=str(standup_date),
            member_name=member_name,
            yesterday=yesterday,
            today=today,
            blocker=blocker
        )
        st.success("Standup update saved.")

elif menu == "Daily Digest":
    st.header("Generate Daily Digest")

    sprint = st.text_input("Sprint Name", "Sprint 12", key="daily_sprint")
    standup_date = st.date_input("Digest Date", key="daily_date")

    if st.button("Generate Daily Digest"):
        updates = get_updates_by_day(sprint, str(standup_date))

        if not updates:
            st.info("No updates found for that sprint and date.")
        else:
            updates_text = "\n\n".join([
                f"""Member: {u['member_name']}
Yesterday: {u['yesterday']}
Today: {u['today']}
Blocker: {u['blocker']}"""
                for u in updates
            ])

            with st.spinner("Generating summary..."):
                summary = summary_agent.run(updates_text, sprint, str(standup_date))

            with st.spinner("Detecting blockers..."):
                blockers = blocker_agent.run(updates_text, sprint, str(standup_date))

            with st.spinner("Estimating sprint progress..."):
                progress = progress_agent.run(updates_text, sprint, str(standup_date))

            if summary.startswith("ERROR:"):
                st.error(f"Summary Agent failed: {summary}")
            else:
                st.subheader("Team Summary")
                st.write(summary)

                if blockers.startswith("ERROR:"):
                    st.warning("Blocker detection failed.")
                else:
                    st.subheader("Blocker Report")
                    st.write(blockers)

                if progress.startswith("ERROR:"):
                    st.warning("Sprint progress estimation failed.")
                else:
                    st.subheader("Sprint Progress Estimate")
                    st.write(progress)

                digest_text = f"""
Sprint: {sprint}
Date: {standup_date}

=== TEAM SUMMARY ===
{summary}

=== BLOCKER REPORT ===
{blockers}

=== SPRINT PROGRESS ===
{progress}
"""

                file_path = EXPORT_DIR / f"{sprint.replace(' ', '_')}_{standup_date}_daily_digest.txt"
                file_path.write_text(digest_text, encoding="utf-8")

                st.download_button(
                    label="Download Daily Digest",
                    data=digest_text,
                    file_name=file_path.name,
                    mime="text/plain"
                )

elif menu == "Sprint History":
    st.header("Sprint Logs and Weekly Digest")

    sprint = st.text_input("Sprint Name", "Sprint 12", key="history_sprint")

    updates = get_updates_by_sprint(sprint)

    if updates:
        df = pd.DataFrame(updates)
        st.dataframe(
            df[["date", "member_name", "yesterday", "today", "blocker"]],
            use_container_width=True
        )

        if st.button("Generate Weekly Digest"):
            weekly_text = "\n\n".join([
                f"""Date: {u['date']}
Member: {u['member_name']}
Yesterday: {u['yesterday']}
Today: {u['today']}
Blocker: {u['blocker']}"""
                for u in updates
            ])

            with st.spinner("Generating weekly team digest..."):
                weekly_summary = summary_agent.run(weekly_text, sprint, "Weekly Summary")

            if weekly_summary.startswith("ERROR:"):
                st.error(f"Weekly digest generation failed: {weekly_summary}")
            else:
                st.subheader("Weekly Digest")
                st.write(weekly_summary)

                file_path = EXPORT_DIR / f"{sprint.replace(' ', '_')}_weekly_digest.txt"
                file_path.write_text(weekly_summary, encoding="utf-8")

                st.download_button(
                    label="Download Weekly Digest",
                    data=weekly_summary,
                    file_name=file_path.name,
                    mime="text/plain"
                )
    else:
        st.info("No standup logs found for this sprint.")

else:
    st.header("About")
    st.markdown("""
This application supports asynchronous agile standups using three AI agents:
- Summary Agent
- Blocker Detector Agent
- Sprint Progress Estimator Agent

It stores sprint-based logs and can generate downloadable daily and weekly team digests.
""")