
# import streamlit as st
# import google.generativeai as genai
# import os
# import json
# import pandas as pd
# from dotenv import load_dotenv
# from datetime import datetime
# from auth import login

# # ---------------------------------------------------
# # CONFIG
# # ---------------------------------------------------
# st.set_page_config(
#     page_title="ResolveIQ",
#     layout="wide"
# )

# # ---------------------------------------------------
# # AUTHENTICATION
# # ---------------------------------------------------
# login()

# # ---------------------------------------------------
# # HEADER (Top Right User Info)

# col1, col2 = st.columns([6, 2])

# with col1:
#     st.image("logo.png", width=220)

# with col2:
#     st.markdown(f"<div style='text-align: right; margin-top: 20px;'>"
#                 f"👤 <b>{st.session_state.username}</b>"
#                 f"</div>", unsafe_allow_html=True)

#     if st.button("Logout"):
#         st.session_state.authenticated = False
#         st.session_state.username = None
#         st.rerun()

# st.markdown("---")

# # ---------------------------------------------------
# # GEMINI SETUP
# # ---------------------------------------------------
# load_dotenv()
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
# model = genai.GenerativeModel("gemini-1.5-flash")

# # ---------------------------------------------------
# # SESSION STATE
# # ---------------------------------------------------
# if "history" not in st.session_state:
#     st.session_state.history = []

# # ---------------------------------------------------
# # SIDEBAR NAVIGATION (Only after login)
# # ---------------------------------------------------
# st.sidebar.title("Navigation")

# page = st.sidebar.radio("Go to", [
#     "🏠 Dashboard",
#     "🎫 Analyze Ticket",
#     "📊 Analytics"
# ])

# # ---------------------------------------------------
# # DASHBOARD
# # ---------------------------------------------------
# if page == "🏠 Dashboard":

#     st.subheader("Welcome Back 👋")

#     if st.session_state.history:
#         total = len(st.session_state.history)
#         st.metric("Total Tickets Processed", total)

#         st.subheader("Recent Tickets")

#         for ticket in reversed(st.session_state.history[-5:]):
#             with st.expander(f"{ticket['category']} | {ticket['priority']}"):
#                 st.write(ticket["original_ticket"])
#                 st.write("Resolution:")
#                 st.write(ticket["resolution"])
#     else:
#         st.info("No tickets processed yet.")

# # ---------------------------------------------------
# # ANALYZE PAGE
# # ---------------------------------------------------
# elif page == "🎫 Analyze Ticket":

#     st.subheader("Analyze Support Ticket")

#     ticket_text = st.text_area("Enter Customer Ticket", height=200)

#     if st.button("Analyze"):

#         if ticket_text.strip() == "":
#             st.warning("Please enter ticket text.")
#         else:

#             prompt = f"""
#             Analyze this support ticket and return ONLY valid JSON.

#             Classify into:
#             Billing, Network, Login, Hardware, Software, Other

#             Assign priority:
#             Low, Medium, High, Critical

#             Detect sentiment:
#             Positive, Neutral, Negative

#             Provide confidence score (0-100).

#             Ticket:
#             {ticket_text}

#             Output format:
#             {{
#                 "category": "",
#                 "priority": "",
#                 "sentiment": "",
#                 "confidence_score": 0,
#                 "resolution": ""
#             }}
#             """

#             response = model.generate_content(prompt)

#             try:
#                 result = json.loads(response.text)

#                 result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                 result["original_ticket"] = ticket_text

#                 st.session_state.history.append(result)

#                 col1, col2, col3 = st.columns(3)
#                 col1.metric("Category", result["category"])
#                 col2.metric("Priority", result["priority"])
#                 col3.metric("Sentiment", result["sentiment"])

#                 st.progress(result["confidence_score"] / 100)

#                 st.subheader("Suggested Resolution")
#                 st.write(result["resolution"])

#             except:
#                 st.error("Invalid AI response.")

# # ---------------------------------------------------
# # ANALYTICS
# # ---------------------------------------------------
# elif page == "📊 Analytics":

#     if st.session_state.history:

#         df = pd.DataFrame(st.session_state.history)

#         st.subheader("Category Distribution")
#         st.bar_chart(df["category"].value_counts())

#         st.subheader("Priority Distribution")
#         st.bar_chart(df["priority"].value_counts())

#         csv = df.to_csv(index=False).encode("utf-8")
#         st.download_button(
#             "Download Report",
#             csv,
#             "resolveiq_report.csv",
#             "text/csv"
#         )

#     else:
#         st.info("No data available.")
import streamlit as st
from openai import OpenAI
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from auth import login
from database import save_ticket, get_tickets

from database import create_user_table

create_user_table()
from database import add_user, authenticate
# ---------------------------------------------------
# CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="ResolveIQ",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.metric-card {
    background-color: #1c1f26;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #2c2f36;
    text-align: center;
}

.metric-title {
    font-size: 16px;
    color: #9aa0a6;
}

.metric-value {
    font-size: 28px;
    font-weight: bold;
    color: #ffffff;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------
login()

# ---------------------------------------------------
# HEADER (Top Right User Info)
# ---------------------------------------------------
col1, col2 = st.columns([6, 2])

with col1:
    st.image("logo.png", width=220)

with col2:
    st.markdown(f"<div style='text-align: right; margin-top: 20px;'>"
                f"👤 <b>{st.session_state.username}</b>"
                f"</div>", unsafe_allow_html=True)

    if st.button("Logout"):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.rerun()

st.markdown("---")

# ---------------------------------------------------
# GROK API SETUP
# ---------------------------------------------------
load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

# completion = client.chat.completions.create(
#     model="meta-llama/llama-3-8b-instruct",
#     messages=[
#         {"role": "user", "content": "Explain agentic AI in simple terms"}
#     ]
# )

# print(completion.choices[0].message.content)

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = get_tickets()
# ---------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------
st.sidebar.title("Navigation")

page = st.sidebar.radio("Go to", [
    "🏠 Dashboard",
    "🎫 Analyze Ticket",
    "📊 Analytics"
])

# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------
if page == "🏠 Dashboard":

    st.subheader("Welcome Back 👋")

    if st.session_state.history:
        total = len(st.session_state.history)
        st.metric("Total Tickets Processed", total)

        st.subheader("Recent Tickets")

        for ticket in reversed(st.session_state.history[-5:]):
            with st.expander(f"{ticket['category']} | {ticket['priority']}"):
                st.write(ticket["original_ticket"])
                st.write("Resolution:")
                st.write(ticket["resolution"])
    else:
        st.info("No tickets processed yet.")

# ---------------------------------------------------
# ANALYZE PAGE
# ---------------------------------------------------
elif page == "🎫 Analyze Ticket":

    st.subheader("Analyze Support Ticket")

    ticket_text = st.text_area(
        "Enter Customer Ticket",
        placeholder="Paste or type the customer's support ticket here...",
        height=200
    )
    if st.button("Analyze"):

        if ticket_text.strip() == "":
            st.warning("Please enter ticket text.")
        else:

            prompt = f"""
            Analyze this support ticket and return ONLY valid JSON.

            Classify into:
            Billing, Network, Login, Hardware, Software, Other

            Assign priority:
            Low, Medium, High, Critical

            Detect sentiment:
            Positive, Neutral, Negative

            Provide:
            - category
            - priority
            - sentiment
            - confidence_score(0-100)
            - summary
            - resolution

            The customer_reply should be a professional support response email.

            Ticket:
            {ticket_text}

            Output format:
            {{
                "category": "",
                "priority": "",
                "sentiment": "",
                "confidence_score": 0,
                "summary":  "",
                "resolution": ""
                "customer_reply": ""
            }}
            """

            response = client.chat.completions.create(
                model="meta-llama/llama-3-8b-instruct",
                messages=[
                    {"role": "system", "content": "You are an expert IT support ticket classifier."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )

            ai_text = response.choices[0].message.content

            try:
                import re

                json_text = re.search(r"\{.*\}", ai_text, re.DOTALL).group()
                result = json.loads(json_text)

                result["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result["original_ticket"] = ticket_text
                team_map = {
                    "Billing": "Finance Team",
                    "Network": "Network Operations",
                    "Login": "Identity & Access Team",
                    "Hardware": "IT Infrastructure",
                    "Software": "Application Support",
                    "Other": "General Support"
                }

                result["assigned_team"] = team_map.get(result["category"], "Support Team")
                save_ticket(result)
                st.session_state.history = get_tickets()

                col1, col2, col3, col4 = st.columns(4)

                col1.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">Category</div>
                <div class="metric-value">{result["category"]}</div>
                </div>
                """, unsafe_allow_html=True)

                col2.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">Priority</div>
                <div class="metric-value">{result["priority"]}</div>
                </div>
                """, unsafe_allow_html=True)

                col3.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">Sentiment</div>
                <div class="metric-value">{result["sentiment"]}</div>
                </div>
                """, unsafe_allow_html=True)

                col4.markdown(f"""
                <div class="metric-card">
                <div class="metric-title">Assigned Team</div>
                <div class="metric-value">{result["assigned_team"]}</div>
                </div>
                """, unsafe_allow_html=True)

                st.progress(result["confidence_score"] / 100)

                st.subheader("Ticket Summary")
                st.write(result["summary"])

                st.subheader("Suggested Resolution")
                st.write(result["resolution"])
                st.subheader("AI Generated Customer Reply")
                st.info(result["customer_reply"])

            except Exception as e:
                st.error(f"AI response error: {e}")

# ---------------------------------------------------
# ANALYTICS
# ---------------------------------------------------
elif page == "📊 Analytics":

    if st.session_state.history:

        df = pd.DataFrame(st.session_state.history)
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Tickets", len(df))
        col2.metric("High Priority", len(df[df["priority"]=="High"]))
        col3.metric("Critical Tickets", len(df[df["priority"]=="Critical"]))
        st.subheader("Category Distribution")
        st.bar_chart(df["category"].value_counts())

        st.subheader("Priority Distribution")
        st.bar_chart(df["priority"].value_counts())
        st.subheader("Customer Sentiment")
        st.bar_chart(df["sentiment"].value_counts())
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        tickets_by_time = df.groupby(df["timestamp"].dt.date).size()

        st.subheader("Tickets Over Time")
        st.line_chart(tickets_by_time)
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Report",
            csv,
            "resolveiq_report.csv",
            "text/csv"
        )

    else:
        st.info("No data available.")