import os
import datetime
import requests
import streamlit as st

BASE_URL = os.getenv("BACKEND_URL", "http://localhost:8000")  # Backend endpoint

st.set_page_config(
    page_title="🌍 Agentic Travel Planner",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Styling touch for a cleaner, modern look
st.markdown(
    """
    <style>
      .hero {
        padding: 1.2rem 1.6rem;
        border-radius: 16px;
        background: linear-gradient(135deg, #0f172a, #111827 55%, #0ea5e9);
        color: #e5e7eb;
      }
      .hero h1 { margin-bottom: 0.2rem; }
      .hero p { margin-top: 0.4rem; color: #cbd5f5; }
      .cta-card {
        border: 1px solid #e5e7eb;
        padding: 1rem;
        border-radius: 12px;
        background: #ffffff;
      }
      .stTextArea textarea {
        border-radius: 12px;
      }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = []  # list of dicts: {prompt, answer, timestamp}

quick_prompts = [
    "Plan a 4-day off-beat + tourist mix trip to Kyoto under $1200.",
    "Romantic 3-day Paris getaway with mid-range hotels and food recs.",
    "7-day family-friendly Bali plan with beaches + cultural stops, <$2000.",
    "Weekend in NYC focused on art, food, and hidden gems; keep it walkable.",
]

# Sidebar: helpful tips
with st.sidebar:
    st.subheader("How to get great plans")
    st.markdown(
        "- Include **dates** or season for better weather insights.\n"
        "- Share **budget** and **group type** (solo, couple, family).\n"
        "- Mention **interests** (nature, museums, food, nightlife).\n"
        "- Ask for **off-beat** spots to avoid tourist crowds."
    )
    st.divider()
    st.subheader("Backend")
    st.code(BASE_URL, language="bash")
    if st.session_state.history:
        latest = st.session_state.history[0]
        st.caption(f"Last response: {latest['timestamp'].strftime('%Y-%m-%d %H:%M')}")

# Hero section
st.markdown(
    """
    <div class="hero">
      <h1>🌍 Agentic Travel Planner</h1>
      <p>Design your next adventure with curated itineraries, live weather, and budget-aware plans — in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

# Prompt input + quick starts
col1, col2 = st.columns([2, 1], gap="large")
with col1:
    with st.form(key="query_form", clear_on_submit=False):
        user_input = st.text_area(
            "Describe your trip",
            placeholder="e.g. 5-day trip to Lisbon in April, focus on food and history, budget $1500, include local-only spots.",
            height=140,
        )
        submit_button = st.form_submit_button("Generate itinerary 🚀", use_container_width=True)

    if submit_button and user_input.strip():
        try:
            with st.spinner("AI is planning your trip..."):
                payload = {"question": user_input}
                response = requests.post(f"{BASE_URL}/query", json=payload, timeout=120)

            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned.")
                timestamp = datetime.datetime.now()
                st.session_state.history.insert(
                    0,
                    {
                        "prompt": user_input.strip(),
                        "answer": answer,
                        "timestamp": timestamp,
                    },
                )

                st.success("Your itinerary is ready.")
            else:
                st.error("Bot failed to respond: " + response.text)

        except Exception as e:
            st.error(f"The response failed: {e}")

    if st.session_state.history:
        latest = st.session_state.history[0]
        st.markdown("### Latest itinerary")
        st.caption(f"Generated: {latest['timestamp'].strftime('%Y-%m-%d %H:%M')}")
        st.markdown(latest["answer"])

        st.download_button(
            label="Download Markdown",
            data=latest["answer"],
            file_name=f"travel-plan-{latest['timestamp'].strftime('%Y%m%d-%H%M')}.md",
            mime="text/markdown",
            use_container_width=True,
        )

with col2:
    st.markdown("#### Quick start")
    for idx, sample in enumerate(quick_prompts, start=1):
        if st.button(f"Try idea {idx}", key=f"sample_{idx}", use_container_width=True):
            st.session_state["query_form-user_input"] = sample
            st.experimental_rerun()

    st.divider()
    if st.session_state.history:
        st.markdown("#### Recent plans")
        for item in st.session_state.history[:3]:
            with st.expander(item["prompt"][:60] + ("..." if len(item["prompt"]) > 60 else "")):
                st.caption(item["timestamp"].strftime("%Y-%m-%d %H:%M"))
                st.markdown(item["answer"])
