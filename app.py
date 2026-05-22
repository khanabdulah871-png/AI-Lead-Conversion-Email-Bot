# app.py
import streamlit as st
from email_utils import fetch_unread_emails, send_email
from agent import process_email
from database import create_tables, save_lead, save_message, update_lead_status, get_all_leads

# ─────────────────────────────────────────
# PAGE SETUP
# ─────────────────────────────────────────
st.set_page_config(
    page_title = "AI Email Sales Agent",
    page_icon  = "📧",
    layout     = "wide"
)

# Create tables if not exist
create_tables()

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
st.sidebar.title("📧 AI Email Sales Agent")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigation", ["Inbox", "All Leads"])

# ─────────────────────────────────────────
# PAGE 1 — INBOX
# ─────────────────────────────────────────
if page == "Inbox":
    st.title("📥 Inbox")
    st.markdown("Fetch and process unread emails from Gmail.")
    st.markdown("---")

    # Fetch emails button
    if st.button("🔄 Fetch Unread Emails", use_container_width=True):
        with st.spinner("Fetching emails from Gmail..."):
            emails = fetch_unread_emails()

        if not emails:
            st.info("No unread emails found.")
        else:
            st.success(f"{len(emails)} unread email(s) found!")
            st.session_state["emails"] = emails

    # Show fetched emails
    if "emails" in st.session_state and st.session_state["emails"]:
        emails = st.session_state["emails"]

        for i, email in enumerate(emails):
            with st.expander(f"📨 {email['subject']} — From: {email['sender']}"):

                # Email details
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**From:** {email['sender']}")
                with col2:
                    st.markdown(f"**Subject:** {email['subject']}")

                st.markdown("**Email Body:**")
                st.text_area(
                    label     = "Body",
                    value     = email["body"],
                    height    = 150,
                    disabled  = True,
                    key       = f"body_{i}"
                )

                # Process with AI button
                if st.button("🤖 Process with AI", key=f"process_{i}", use_container_width=True):
                    with st.spinner("AI is analyzing the email..."):
                        result = process_email(email)
                        st.session_state[f"result_{i}"] = result

                # Show AI result
                if f"result_{i}" in st.session_state:
                    result = st.session_state[f"result_{i}"]

                    st.markdown("---")

                    # Intent and Score
                    col1, col2 = st.columns(2)
                    with col1:
                        intent = result["intent"]
                        color  = {
                            "buying"   : "🟢",
                            "inquiry"  : "🔵",
                            "complaint": "🔴",
                            "followup" : "🟡",
                            "other"    : "⚪"
                        }.get(intent, "⚪")
                        st.markdown(f"**Intent:** {color} {intent.capitalize()}")

                    with col2:
                        score = result["lead_score"]
                        if score >= 8:
                            label = "🔥 Hot Lead"
                        elif score >= 5:
                            label = "warm Lead"
                        else:
                            label = "❄️ Cold Lead"
                        st.markdown(f"**Lead Score:** {score}/10 — {label}")

                    st.markdown("**AI Generated Reply:**")
                    reply = st.text_area(
                        label  = "AI Reply (you can edit before sending)",
                        value  = result["reply"],
                        height = 200,
                        key    = f"reply_{i}"
                    )

                    st.markdown("---")

                    # Approve / Reject buttons
                    col1, col2 = st.columns(2)

                    with col1:
                        if st.button("✅ Approve & Send", key=f"approve_{i}", use_container_width=True):
                            with st.spinner("Sending email..."):

                                # Send email
                                sent = send_email(
                                    to_email = result["sender"],
                                    subject  = result["subject"],
                                    body     = reply
                                )

                                if sent:
                                    # Save to database
                                    lead_id = save_lead(
                                        sender     = result["sender"],
                                        subject    = result["subject"],
                                        body       = result["body"],
                                        intent     = result["intent"],
                                        lead_score = result["lead_score"]
                                    )
                                    save_message(lead_id, "customer", result["body"])
                                    save_message(lead_id, "agent", reply)
                                    update_lead_status(lead_id, "approved")

                                    st.success("Email sent and saved successfully!")
                                else:
                                    st.error("Failed to send email. Please try again.")

                    with col2:
                        if st.button("❌ Reject", key=f"reject_{i}", use_container_width=True):
                            # Save as rejected
                            lead_id = save_lead(
                                sender     = result["sender"],
                                subject    = result["subject"],
                                body       = result["body"],
                                intent     = result["intent"],
                                lead_score = result["lead_score"]
                            )
                            update_lead_status(lead_id, "rejected")
                            st.warning("Email rejected and saved.")

# ─────────────────────────────────────────
# PAGE 2 — ALL LEADS
# ─────────────────────────────────────────
elif page == "All Leads":
    st.title("📊 All Leads")
    st.markdown("View all processed leads and their status.")
    st.markdown("---")

    leads = get_all_leads()

    if not leads:
        st.info("No leads found yet. Process some emails first.")
    else:
        st.success(f"Total Leads: {len(leads)}")

        for lead in leads:
            # Status color
            status = lead["status"]
            if status == "approved":
                status_icon = "✅"
            elif status == "rejected":
                status_icon = "❌"
            else:
                status_icon = "⏳"

            # Score label
            score = lead["lead_score"]
            if score >= 8:
                score_label = "🔥 Hot"
            elif score >= 5:
                score_label = "😐 Warm"
            else:
                score_label = "❄️ Cold"

            with st.expander(f"{status_icon} {lead['subject']} — {lead['sender']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**Sender:** {lead['sender']}")
                with col2:
                    st.markdown(f"**Score:** {score}/10 — {score_label}")
                with col3:
                    st.markdown(f"**Status:** {status_icon} {status.capitalize()}")

                st.markdown("**Email Body:**")
                st.text_area(
                    label    = "Body",
                    value    = lead["body"],
                    height   = 120,
                    disabled = True,
                    key      = f"lead_body_{lead['id']}"
                )
                st.markdown(f"**Date:** {lead['created_at']}")