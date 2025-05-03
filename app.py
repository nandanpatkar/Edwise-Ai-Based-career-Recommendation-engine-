
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import re
from fpdf import FPDF
import tempfile
import os
import io
from datetime import datetime


st.set_page_config(page_title="AI Career Counselor", layout="wide")

# ----------------- Custom CSS for Animations and Effects -----------------
st.markdown(
    """
    <style>
    .fade-in {
        animation: fadeInAnimation 1s ease-in;
        -webkit-animation: fadeInAnimation 1s ease-in;
    }
    @keyframes fadeInAnimation {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    @-webkit-keyframes fadeInAnimation {
        0% { opacity: 0; }
        100% { opacity: 1; }
    }
    /* Enhance button appearance */
    .stButton>button {
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        transition: transform 0.2s ease-in-out;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎓 AI Career Counselor")

# ----------------- Import Your Modules -----------------
from assessments.iq_test import iq_test
from assessments.big_five import big_five_test  # Assumes this returns a dict of scores
from assessments.holland_code import holland_code_test
from utils.scoring import get_recommendations
from personal_info_form import render_personal_info_form

# ----------------- Sidebar Navigation -----------------
with st.sidebar:
    st.title("🧭 Navigation")
    st.markdown("### Steps")
    st.markdown("1. Personal Info")
    st.markdown("2. Aptitude Test")
    st.markdown("3. Big Five Assessment")
    st.markdown("4. Holland Code Test")
    st.markdown("5. Recommendations, Analytics & Reports")
    st.markdown("6. 💬 Chatbot")

# ----------------- Progress Indicator -----------------
if "progress" not in st.session_state:
    st.session_state.progress = 0

def update_progress(step):
    steps = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
    st.session_state.progress = steps.get(step, st.session_state.progress)

st.progress(st.session_state.progress)

# ------------------ Helper Functions for PDF Report ------------------
def safe_text(text):
    """Ensure text is safe for PDF encoding."""
    return text.encode("latin-1", "replace").decode("latin-1")

def save_big_five_radar(scores, filename):
    labels = list(scores.keys())
    values = list(scores.values())
    angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
    values += values[:1]
    angles += angles[:1]
    fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
    ax.plot(angles, values, linewidth=2)
    ax.fill(angles, values, alpha=0.25)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)
    ax.set_title("Big Five Personality Radar")
    plt.savefig(filename, bbox_inches="tight")
    plt.close(fig)

def save_holland_bar_chart(codes, filename):
    holland_count = {}
    for code in codes:
        holland_count[code] = holland_count.get(code, 0) + 1
    df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
    df = df.sort_values("Count", ascending=False)
    fig, ax = plt.subplots(figsize=(6,4))
    ax.bar(df["Trait"], df["Count"], color="skyblue")
    ax.set_title("Holland Code Frequency")
    plt.savefig(filename, bbox_inches="tight")
    plt.close(fig)

def save_personal_info_3d(user_data, filename):
    career_interests = user_data.get("career_interests", {})
    primary_fields = career_interests.get("primary_fields", [])
    if not primary_fields:
        return False
    df = pd.DataFrame({
        "Field": primary_fields,
        "Count": [1] * len(primary_fields),
        "Index": list(range(len(primary_fields)))
    })
    fig = px.scatter_3d(df, x="Field", y="Index", z="Count", size="Count",
                          title="3D Analytics: Primary Career Fields",
                          hover_name="Field")
    fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
    fig.write_image(filename)
    return True

def save_market_trends_pie(trends_text, filename):
    pattern = r"(\w+):\s*(\d+)%"
    matches = re.findall(pattern, trends_text)
    if matches:
        labels = [match[0] for match in matches]
        values = [int(match[1]) for match in matches]
        fig = px.pie(names=labels, values=values, title="Market Trends by Sector")
        fig.write_image(filename)
        return True
    return False

def generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score, trends_text):
    pdf = FPDF()
    pdf.add_page()
    
    # Title Page
    pdf.set_font("Arial", "B", 24)
    pdf.cell(0, 20, safe_text("AI Career Counseling Report"), ln=True, align="C")
    pdf.set_font("Arial", "I", 12)
    pdf.cell(0, 10, safe_text("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ln=True, align="C")
    pdf.ln(20)
    
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(10)
    
    # User Profile Summary
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("User Profile Summary"), ln=True)
    pdf.set_font("Arial", "", 12)
    personal_info = user_data.get("personal_info", {})
    for key, value in personal_info.items():
        pdf.cell(0, 8, safe_text(f"{key.capitalize()}: {value}"), ln=True)
    pdf.ln(5)
    
    # Assessment Overview
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("Assessment Overview"), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.cell(0, 8, safe_text(f"IQ Score: {iq_score}"), ln=True)
    pdf.cell(0, 8, safe_text(f"Big Five Scores: {big_five_scores}"), ln=True)
    pdf.cell(0, 8, safe_text(f"Holland Code: {holland_code_result}"), ln=True)
    pdf.ln(5)
    
    # Career Recommendations
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("Career Recommendations"), ln=True)
    pdf.set_font("Arial", "", 12)
    pdf.multi_cell(0, 8, safe_text(recommendations))
    pdf.ln(5)
    
    tmp_files = []
    
    # Big Five Radar Chart
    bf_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    bf_file.close()
    save_big_five_radar(big_five_scores, bf_file.name)
    tmp_files.append(bf_file.name)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("Big Five Radar Chart"), ln=True)
    pdf.image(bf_file.name, w=100)
    pdf.ln(10)
    
    # Holland Code Bar Chart
    hc_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    hc_file.close()
    save_holland_bar_chart(holland_code_result, hc_file.name)
    tmp_files.append(hc_file.name)
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, safe_text("Holland Code Bar Chart"), ln=True)
    pdf.image(hc_file.name, w=100)
    pdf.ln(10)
    
    # Personal Info 3D Chart
    pi_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    pi_file.close()
    if save_personal_info_3d(user_data, pi_file.name):
        tmp_files.append(pi_file.name)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, safe_text("3D Analytics: Primary Career Fields"), ln=True)
        pdf.image(pi_file.name, w=100)
        pdf.ln(10)
    
    # Market Trends Pie Chart
    mt_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    mt_file.close()
    if save_market_trends_pie(trends_text, mt_file.name):
        tmp_files.append(mt_file.name)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, safe_text("Market Trends by Sector"), ln=True)
        pdf.image(mt_file.name, w=100)
        pdf.ln(10)
    
    pdf_str = pdf.output(dest="S")
    pdf_data = pdf_str.encode("latin-1")
    
    for file in tmp_files:
        os.remove(file)
    
    return pdf_data

# ------------------ End of Helper Functions for PDF ------------------

# ------------------ Main Application Tabs ------------------
tabs = st.tabs([
    "📄 Personal Info",
    "🧠 Aptitude Test",
    "🌟 Big Five Assessment",
    "🧭 Holland Code Test",
    "🎯 Recommendations, Analytics & Reports",
    "💬 Chatbot"
])

# ---------- TAB 1: Personal Info ----------
with tabs[0]:
    st.header("Step 1: Personal Information")
    user_data = render_personal_info_form()
    if user_data:
        st.session_state["user_data"] = user_data
        st.success("✅ Profile submitted successfully!")
        with st.expander("🔍 See Collected User Data"):
            st.json(user_data)
        update_progress(1)

# ---------- TAB 2: IQ Test ----------
with tabs[1]:
    st.header("Step 2: IQ Test")
    with st.expander("🧠 Start IQ Test"):
        iq_score = iq_test()
        if iq_score is not None:
            st.session_state["iq_score"] = iq_score
            # st.success(f"Your IQ Score: {iq_score}")
            update_progress(2)

# ---------- TAB 3: Big Five Assessment ----------
with tabs[2]:
    st.header("Step 3: Big Five Personality Assessment")
    with st.expander("📝 Begin Big Five Assessment"):
        big_five_scores = big_five_test()  # Assumes returns a dict of scores
    if big_five_scores is not None:
        st.session_state["big_five"] = big_five_scores
        st.success("Big Five Assessment Completed!")
        with st.expander("🔍 View Big Five Scores"):
            st.json(big_five_scores)
        update_progress(3)

# ---------- TAB 4: Holland Code Test ----------
with tabs[3]:
    st.header("Step 4: Holland Code Assessment")
    holland_code_result = holland_code_test()
    if holland_code_result is not None:
        st.session_state["holland_code_result"] = holland_code_result
        update_progress(4)

# ---------- TAB 5: Recommendations, Analytics & Reports ----------
with tabs[4]:
    st.header("Step 5: Get Career Recommendations and Analytics")
    user_data = st.session_state.get("user_data", {})
    iq_score = st.session_state.get("iq_score")
    big_five_scores = st.session_state.get("big_five")
    holland_code_result = st.session_state.get("holland_code_result")
    
    def all_steps_completed():
        return (
            user_data and isinstance(user_data, dict)
            and iq_score is not None and isinstance(iq_score, (int, float))
            and big_five_scores is not None and isinstance(big_five_scores, dict)
            and holland_code_result is not None and isinstance(holland_code_result, list)
        )
    
    with st.expander("🔍 Debug: Current State"):
        st.write("User Data:", "Present" if user_data else "Missing")
        st.write("IQ Score:", iq_score)
        st.write("Big Five Scores:", big_five_scores)
        st.write("Holland Code Result:", holland_code_result)
    
    if all_steps_completed():
        full_user_data = {
            "personal_info": user_data.get("personal_info", {}),
            "career_interests": user_data.get("career_interests", {}),
            "skills": user_data.get("skills", {}),
            "future_aspirations": user_data.get("future_aspirations", {}),
            "assessments": {
                "iq_score": iq_score,
                "big_five": big_five_scores,
                "holland_code": holland_code_result
            }
        }
        if st.button("✨ Generate Recommendations"):
            with st.spinner("Analyzing your profile..."):
                try:
                    recommendations = get_recommendations(full_user_data)
                    st.success("✅ Career Recommendations Generated!")
                    st.write(recommendations)
                    update_progress(5)
                    
                    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
                    st.markdown("## 📊 Visual Analytics")
                    
                    # Display Big Five Radar Chart
                    def plot_big_five_radar_display(scores):
                        labels = list(scores.keys())
                        values = list(scores.values())
                        angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
                        values += values[:1]
                        angles += angles[:1]
                        fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
                        ax.plot(angles, values, linewidth=2)
                        ax.fill(angles, values, alpha=0.25)
                        ax.set_xticks(angles[:-1])
                        ax.set_xticklabels(labels)
                        ax.set_title("🧠 Big Five Personality Radar")
                        st.pyplot(fig)
                    
                    if big_five_scores:
                        plot_big_five_radar_display(big_five_scores)
                    
                    # Display Holland Code Bar Chart
                    def plot_holland_bar_display(codes):
                        holland_count = {}
                        for code in codes:
                            holland_count[code] = holland_count.get(code, 0) + 1
                        df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
                        df = df.sort_values("Count", ascending=False)
                        st.bar_chart(df.set_index("Trait"))
                    
                    if holland_code_result:
                        plot_holland_bar_display(holland_code_result)
                    
                    st.metric(label="🧠 IQ Score", value=iq_score, delta="Out of 200")
                    
                    def plot_personal_info_3d_display(user_data):
                        career_interests = user_data.get("career_interests", {})
                        primary_fields = career_interests.get("primary_fields", [])
                        if not primary_fields:
                            st.info("No career interests available for 3D analytics.")
                            return
                        df = pd.DataFrame({
                            "Field": primary_fields,
                            "Count": [1] * len(primary_fields),
                            "Index": list(range(len(primary_fields)))
                        })
                        fig = px.scatter_3d(df, x="Field", y="Index", z="Count", size="Count",
                                              title="3D Analytics: Primary Career Fields",
                                              hover_name="Field")
                        fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    plot_personal_info_3d_display(user_data)
                    
                    from utils.market_analysis import market_trends
                    trends_text = ""
                    try:
                        trends_text = market_trends()  # Expected format: "Tech: 40%, Healthcare: 25%, Finance: 15%, ..."
                        st.write("Market Trends:", trends_text)
                    except Exception as e:
                        st.error(f"Error fetching market trends: {e}")
                    
                    def plot_market_trends_pie_display(trends_text):
                        pattern = r"(\w+):\s*(\d+)%"
                        matches = re.findall(pattern, trends_text)
                        if matches:
                            labels = [match[0] for match in matches]
                            values = [int(match[1]) for match in matches]
                            fig = px.pie(names=labels, values=values, title="Market Trends by Sector")
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("Market trends data could not be parsed for visual analytics.")
                    
                    if trends_text:
                        plot_market_trends_pie_display(trends_text)
                    
                    pdf_data = generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score, trends_text)
                    st.download_button("📥 Download Report as PDF", data=pdf_data, file_name="career_report.pdf", mime="application/pdf")
                    
                    st.markdown('</div>', unsafe_allow_html=True)
                            
                except Exception as e:
                    st.error(f"❌ Error generating recommendations: {e}")
    else:
        st.warning("Please complete all previous steps before generating recommendations.")
        st.info("Ensure you have:")
        st.info("1. Submitted Personal Information")
        st.info("2. Completed IQ Test")
        st.info("3. Completed Big Five Assessment")
        st.info("4. Completed Holland Code Test")

# ---------- TAB 6: Chatbot ----------
with tabs[5]:
    st.header("💬 Chatbot - CareerGuide AI")
    
    # Instead of an in-chatbot profile form, include a button to import personal info from Tab 1.
    if st.button("Import Personal Info for Chatbot Context"):
        if "user_data" in st.session_state and "personal_info" in st.session_state["user_data"]:
            st.session_state.user_info = st.session_state["user_data"]["personal_info"]
            st.success("Personal info imported successfully!")
        else:
            st.warning("No personal info found. Please fill out the Personal Info form in Tab 1.")
    
    # Ensure chatbot uses the imported info if available.
    if "user_info" not in st.session_state:
        st.session_state.user_info = {}
    
    # Import and configure the Gemini model for the chatbot
    import google.generativeai as genai
    API_KEY = "AIzaSyDw-USzBZis2PjPrdyLSbal6xPPRVQ01Co"
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash')
    
    # Chatbot Functions
    def generate_career_advice(query, use_cot=True):
        user_info_str = ""
        if st.session_state.user_info:
            ui = st.session_state.user_info
            user_info_str = (f"Name: {ui.get('name', 'N/A')}\n"
                             f"Age: {ui.get('age', 'N/A')}\n"
                             f"Education: {ui.get('education', 'N/A')}\n"
                             f"Test Score: {ui.get('test_score', 'N/A')}\n")
        base_prompt = f"""You are CareerGuide, an expert career counselor.
User Information:
{user_info_str}
Provide thoughtful, personalized career advice based on the query below."""
        if use_cot:
            prompt = f"""{base_prompt}
When answering, please follow this chain-of-thought process:
1. Identify the key career concern.
2. Consider the user's skills, interests, and education.
3. Suggest possible career paths.
4. Weigh pros and cons.
5. Provide actionable recommendations.

User query: {query}

Let's think step by step:"""
        else:
            prompt = f"{base_prompt}\n\nUser query: {query}"
        try:
            response_stream = model.generate_content(prompt, stream=True)
            full_response = ""
            for chunk in response_stream:
                if hasattr(chunk, 'text'):
                    full_response += chunk.text
                    yield chunk.text
            if not full_response:
                yield "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
        except Exception as e:
            yield f"An error occurred: {str(e)}. Please try again."
    
    def generate_follow_up_questions(previous_query, previous_response):
        prompt = f"""Based on the following career conversation, generate 5 follow-up questions.
User's question: {previous_query}
Your response: {previous_response}
List 5 concise follow-up questions (one per line)."""
        try:
            response = model.generate_content(prompt)
            if hasattr(response, 'text'):
                questions_text = response.text.strip()
                questions = [q.strip() for q in questions_text.split('\n') if q.strip()]
                questions = [q.lstrip('0123456789.- *') for q in questions]
                return questions[:5]
            else:
                return get_fallback_questions()
        except Exception as e:
            return get_fallback_questions()
    
    def get_fallback_questions():
        return [
            "What skills are most in-demand today?",
            "How can I improve my resume?",
            "Which career fields pay the most?",
            "How important is work-life balance?",
            "Should I consider freelancing?"
        ]
    
    def set_example_question(question):
        st.session_state.current_question = question
    
    # Initialize messages if not present
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
    
    # Display suggested follow-up questions (if available)
    if st.session_state.messages and len(st.session_state.messages) % 2 == 0:
        st.write("**Suggested follow-up questions:**")
        cols = st.columns(3)
        for i, question in enumerate(st.session_state.get("suggested_questions", [])):
            col_idx = i % 3
            with cols[col_idx]:
                if st.button(question, key=f"chat_sugg_{i}", use_container_width=True):
                    st.session_state.current_question = question
    
    # Get current query from chat input or example question
    if st.session_state.get("current_question"):
        user_query = st.session_state.current_question
        st.session_state.current_question = None
    else:
        user_query = st.chat_input("Ask me about your career...")
    
    if user_query:
        st.session_state.messages.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.write(user_query)
        with st.chat_message("assistant"):
            full_response = ""
            message_placeholder = st.empty()
            cot_enabled = st.toggle("Enable Chain-of-Thought", value=True)
            for chunk in generate_career_advice(user_query, use_cot=cot_enabled):
                full_response += chunk
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
        new_qs = generate_follow_up_questions(user_query, full_response)
        if new_qs:
            st.session_state.suggested_questions = new_qs
























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































# import streamlit as st
# # st.set_page_config(page_title="AI Career Counselor", layout="wide")
# from assessments.iq_test import iq_test
# from assessments.big_five import big_five_test
# from assessments.holland_code import holland_code_test
# from utils.scoring import get_recommendations
# from personal_info_form import render_personal_info_form
# # Removed redundant import as get_recommendations is already imported from utils.scoring
# # st.set_page_config(page_title="AI Career Counselor", layout="wide")
# # import scoring

# import sys
# import os
# from utils.session_helpers import get_safe_user_data  # or wherever you placed it

# st.title("🎓 AI Career Counselor")

# # Tabs for each section
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📄 Personal Info",
#     "🧠 Aptitude Test",
#     "🌟 Big Five Assessment",
#     "🧭 Holland Code Test",
#     "🎯 Recommendations"
# ])

# # ---------- TAB 1: Personal Info ----------
# with tab1:
#     st.header("Step 1: Personal Information")
# #     user_data = render_personal_info_form()

# #     if user_data:
# #         st.success("✅ Profile submitted successfully!")
# #         with st.expander("🔍 See Collected User Data"):
# #             st.json(user_data)
#     user_data = render_personal_info_form()
    
#     if user_data:
#         st.session_state["user_data"] = user_data  # <--- Store in session state
#         st.success("✅ Profile submitted successfully!")
#         with st.expander("🔍 See Collected User Data"):
#             st.json(user_data)




# # ---------- TAB 2: IQ Test ----------
# with tab2:
#     st.header("Step 2: IQ Test")
#     iq_score = iq_test()
#     # iq_score = st.session_state.get("iq_score", )

# # ---------- TAB 3: Big Five ----------
# with tab3:
#     st.header("Step 3: Big Five Personality Assessment")
#     big_five_scores = big_five_test()

# # ---------- TAB 4: Holland Code ----------
# with tab4:
#     st.header("Step 4: Holland Code Assessment")
#     holland_code_result = holland_code_test()

# # ---------- TAB 5: Recommendations ----------
# with tab5:
#     st.header("Step 5: Get Career Recommendations")
#     with st.expander("🔍 Debug: Current State"):
#         user_data = st.session_state.get("user_data", None)
#         st.write("user_data", user_data)
#         st.write("iq_score", st.session_state.get("iq_score"))
#         st.write("big_five_scores", st.session_state.get("big_five"))
#         st.write("holland_code_result", st.session_state.get("holland_code"))
#         # Safely get data from session state
#     iq_score = st.session_state.get("iq_score", None)
#     big_five_scores = st.session_state.get("big_five", None)
#     holland_code_result = st.session_state.get("holland_code_result", None)
#     # if all([
#     # user_data is not None,
#     # isinstance(iq_score, (int, float)),
#     # isinstance(big_five_scores, dict) and big_five_scores != {},
#     # isinstance(holland_code_result, str) and len(holland_code_result) == 3
#     # ]):
#     # Final check before generating
#     if user_data and iq_score is not None and big_five_scores and holland_code_result:
#         if st.button("✨ Generate Recommendations"):
        
#             with st.spinner("Analyzing your profile..."):

#                 # Inject assessment results into the user_data dict
#                 # user_data["assessments"] = {
#                 #     "iq_score": iq_score,
#                 #     "big_five": big_five_scores,
#                 #     "holland_code": holland_code_result
                   
#                 # }
# #                 user_data = {
    
# #      "assessments": {
# #         "iq_score": st.session_state.get("iq_score", "N/A"),
# #         "big_five": st.session_state.get("big_five", {}),
# #         "holland_code": st.session_state.get("holland_code_result", [])
# #     }
# # }              
#                 user_data = st.session_state.get("user_data", {})
#                 user_data["assessments"] = {
#                      "iq_score": iq_score,
#                      "big_five": big_five_scores,
#                      "holland_code": holland_code_result
# }
#                 try:
#                     recommendations = get_recommendations(user_data)
#                     st.success("✅ Career Recommendations Generated!")
#                     st.write(recommendations)
#                 except Exception as e:
#                     st.error(f"❌ Error: {e}")
#     else:
#         st.warning("Please complete all the previous steps before generating recommendations.")














### working code

# import streamlit as st
# st.set_page_config(page_title="AI Career Counselor", layout="wide")

# from assessments.iq_test import iq_test
# from assessments.big_five import big_five_test
# from assessments.holland_code import holland_code_test
# from utils.scoring import get_recommendations
# from personal_info_form import render_personal_info_form

# st.title("🎓 AI Career Counselor")

# # Tabs for each section
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📄 Personal Info",
#     "🧠 Aptitude Test",
#     "🌟 Big Five Assessment",
#     "🧭 Holland Code Test",
#     "🎯 Recommendations"
# ])

# # ---------- TAB 1: Personal Info ----------
# with tab1:
#     st.header("Step 1: Personal Information")
#     user_data = render_personal_info_form()
    
#     if user_data:
#         st.session_state["user_data"] = user_data
#         st.success("✅ Profile submitted successfully!")
#         with st.expander("🔍 See Collected User Data"):
#             st.json(user_data)

# # ---------- TAB 2: IQ Test ----------
# with tab2:
#     st.header("Step 2: IQ Test")
#     iq_score = iq_test()
#     if iq_score is not None:
#         st.session_state["iq_score"] = iq_score

# # ---------- TAB 3: Big Five ----------
# with tab3:
#     st.header("Step 3: Big Five Personality Assessment")
#     big_five_scores = big_five_test()
#     if big_five_scores is not None:
#         st.session_state["big_five"] = big_five_scores

# # ---------- TAB 4: Holland Code ----------
# with tab4:
#     st.header("Step 4: Holland Code Assessment")
#     holland_code_result = holland_code_test()
#     if holland_code_result is not None:
#         st.session_state["holland_code_result"] = holland_code_result

# # ---------- TAB 5: Recommendations ----------
# with tab5:
#     st.header("Step 5: Get Career Recommendations")
    
#     # Collect all required session state data
#     user_data = st.session_state.get("user_data", {})
#     iq_score = st.session_state.get("iq_score")
#     big_five_scores = st.session_state.get("big_five")
#     holland_code_result = st.session_state.get("holland_code_result")

#     # Comprehensive checks to ensure all data is present
#     def all_steps_completed():
#         checks = [
#             user_data and isinstance(user_data, dict),
#             iq_score is not None and isinstance(iq_score, (int, float)),
#             big_five_scores is not None and isinstance(big_five_scores, dict),
#             holland_code_result is not None and isinstance(holland_code_result, list)
#         ]
#         return all(checks)

#     # Debug information
#     with st.expander("🔍 Debug: Current State"):
#         st.write("User Data:", "Present" if user_data else "Missing")
#         st.write("IQ Score:", iq_score)
#         st.write("Big Five Scores:", big_five_scores)
#         st.write("Holland Code Result:", holland_code_result)

#     # Recommendation Generation
#     if all_steps_completed():
#         # Combine all data for recommendations
#         full_user_data = {
#             "personal_info": user_data.get("personal_info", {}),
#             "career_interests": user_data.get("career_interests", {}),
#             "skills": user_data.get("skills", {}),
#             "future_aspirations": user_data.get("future_aspirations", {}),
#             "assessments": {
#                 "iq_score": iq_score,
#                 "big_five": big_five_scores,
#                 "holland_code": holland_code_result
#             }
#         }

#         if st.button("✨ Generate Recommendations"):
#             with st.spinner("Analyzing your profile..."):
#                 try:
#                     recommendations = get_recommendations(full_user_data)
#                     st.success("✅ Career Recommendations Generated!")
#                     st.write(recommendations)
#                 except Exception as e:
#                     st.error(f"❌ Error generating recommendations: {e}")
#     else:
#         st.warning("Please complete all previous steps before generating recommendations.")
#         st.info("Ensure you have:")
#         st.info("1. Submitted Personal Information")
#         st.info("2. Completed IQ Test")
#         st.info("3. Completed Big Five Assessment")
#         st.info("4. Completed Holland Code Test")















### working 1
# import streamlit as st
# import matplotlib.pyplot as plt
# import pandas as pd

# # Configure the Streamlit page
# st.set_page_config(page_title="AI Career Counselor", layout="wide")
# st.title("🎓 AI Career Counselor")

# # Import assessment modules and utilities
# from assessments.iq_test import iq_test
# from assessments.big_five import big_five_test  # Assumes this returns a dict of scores
# from assessments.holland_code import holland_code_test
# from utils.scoring import get_recommendations
# from personal_info_form import render_personal_info_form

# # Sidebar for Navigation
# with st.sidebar:
#     st.title("🧭 Navigation")
#     st.markdown("### Steps")
#     st.markdown("1. Personal Info")
#     st.markdown("2. Aptitude Test")
#     st.markdown("3. Big Five Assessment")
#     st.markdown("4. Holland Code Test")
#     st.markdown("5. Recommendations & Analytics")

# # Progress Indicator (updates from 20% to 100% as steps complete)
# if "progress" not in st.session_state:
#     st.session_state.progress = 0

# def update_progress(step):
#     steps = {
#       1: 0.2,
#       2: 0.4,
#       3: 0.6,
#       4: 0.8,
#       5: 1.0
#     }
#     st.session_state.progress = steps.get(step, st.session_state.progress)
    
# st.progress(st.session_state.get("progress", 0))

# # Create tabs for each section of the application
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📄 Personal Info",
#     "🧠 Aptitude Test",
#     "🌟 Big Five Assessment",
#     "🧭 Holland Code Test",
#     "🎯 Recommendations & Analytics"
# ])

# # ---------- TAB 1: Personal Info ----------
# with tab1:
#     st.header("Step 1: Personal Information")
#     user_data = render_personal_info_form()
#     if user_data:
#         st.session_state["user_data"] = user_data
#         st.success("✅ Profile submitted successfully!")
#         with st.expander("🔍 See Collected User Data"):
#             st.json(user_data)
#         update_progress(1)

# # ---------- TAB 2: IQ Test ----------
# with tab2:
#     st.header("Step 2: IQ Test")
#     with st.expander("🧠 Start IQ Test"):
#         iq_score = iq_test()
#         if iq_score is not None:
#             st.session_state["iq_score"] = iq_score
#             st.success(f"Your IQ Score: {iq_score}")
#             update_progress(2)

# # ---------- TAB 3: Big Five Assessment ----------
# with tab3:
#     st.header("Step 3: Big Five Personality Assessment")
#     with st.expander("📝 Begin Big Five Assessment"):
#         big_five_scores = big_five_test()  # Assumes big_five_test returns a dict of scores
#     if big_five_scores is not None:
#         st.session_state["big_five"] = big_five_scores
#         st.success("Big Five Assessment Completed!")
#         with st.expander("🔍 View Big Five Scores"):
#             st.json(big_five_scores)
#         update_progress(3)

# # ---------- TAB 4: Holland Code Test ----------
# with tab4:
#     st.header("Step 4: Holland Code Assessment")
#     holland_code_result = holland_code_test()
#     if holland_code_result is not None:
#         st.session_state["holland_code_result"] = holland_code_result
#         update_progress(4)

# # ---------- TAB 5: Recommendations & Visual Analytics ----------
# with tab5:
#     st.header("Step 5: Get Career Recommendations and Analytics")
    
#     # Retrieve stored data from session state
#     user_data = st.session_state.get("user_data", {})
#     iq_score = st.session_state.get("iq_score")
#     big_five_scores = st.session_state.get("big_five")
#     holland_code_result = st.session_state.get("holland_code_result")
    
#     # Check if all steps are complete
#     def all_steps_completed():
#         checks = [
#             user_data and isinstance(user_data, dict),
#             iq_score is not None and isinstance(iq_score, (int, float)),
#             big_five_scores is not None and isinstance(big_five_scores, dict),
#             holland_code_result is not None and isinstance(holland_code_result, list)
#         ]
#         return all(checks)
    
#     with st.expander("🔍 Debug: Current State"):
#         st.write("User Data:", "Present" if user_data else "Missing")
#         st.write("IQ Score:", iq_score)
#         st.write("Big Five Scores:", big_five_scores)
#         st.write("Holland Code Result:", holland_code_result)
    
#     if all_steps_completed():
#         # Combine data for generating recommendations
#         full_user_data = {
#             "personal_info": user_data.get("personal_info", {}),
#             "career_interests": user_data.get("career_interests", {}),
#             "skills": user_data.get("skills", {}),
#             "future_aspirations": user_data.get("future_aspirations", {}),
#             "assessments": {
#                 "iq_score": iq_score,
#                 "big_five": big_five_scores,
#                 "holland_code": holland_code_result
#             }
#         }
    
#         if st.button("✨ Generate Recommendations"):
#             with st.spinner("Analyzing your profile..."):
#                 try:
#                     recommendations = get_recommendations(full_user_data)
#                     st.success("✅ Career Recommendations Generated!")
#                     st.write(recommendations)
#                     update_progress(5)
                    
#                     # ---------------- Visual Analytics ----------------
#                     st.markdown("## 📊 Visual Analytics")
                    
#                     # Big Five Radar Chart
#                     def plot_big_five_radar(scores):
#                         labels = list(scores.keys())
#                         values = list(scores.values())
#                         # Compute angles for radar chart
#                         angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
#                         values += values[:1]
#                         angles += angles[:1]
#                         fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
#                         ax.plot(angles, values, linewidth=2)
#                         ax.fill(angles, values, alpha=0.25)
#                         ax.set_xticks(angles[:-1])
#                         ax.set_xticklabels(labels)
#                         ax.set_title("🧠 Big Five Personality Radar")
#                         st.pyplot(fig)
                    
#                     if big_five_scores:
#                         plot_big_five_radar(big_five_scores)
                    
#                     # Holland Code Bar Chart
#                     def plot_holland_bar(codes):
#                         # Here we assume the holland_code_result is a list of codes; we count frequency.
#                         holland_count = {}
#                         for code in codes:
#                             holland_count[code] = holland_count.get(code, 0) + 1
#                         df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
#                         df = df.sort_values("Count", ascending=False)
#                         st.bar_chart(df.set_index("Trait"))
                    
#                     if holland_code_result:
#                         plot_holland_bar(holland_code_result)
                    
#                     # IQ Score as a Metric
#                     st.metric(label="🧠 IQ Score", value=iq_score, delta="Out of 200")
                    
#                     # Optional: Display Market Trends via Gemini API
#                     from utils.market_analysis import market_trends
#                     with st.expander("📈 View Market Trends for Careers"):
#                         try:
#                             trends = market_trends()
#                             st.write(trends)
#                         except Exception as e:
#                             st.error(f"Error fetching market trends: {e}")
                            
#                 except Exception as e:
#                     st.error(f"❌ Error generating recommendations: {e}")
#     else:
#         st.warning("Please complete all previous steps before generating recommendations.")
#         st.info("Ensure you have:")
#         st.info("1. Submitted Personal Information")
#         st.info("2. Completed IQ Test")
#         st.info("3. Completed Big Five Assessment")
#         st.info("4. Completed Holland Code Test")










# import streamlit as st
# import matplotlib.pyplot as plt
# import pandas as pd
# import plotly.express as px
# import re
# from fpdf import FPDF
# import io

# # MUST be the first command!
# st.set_page_config(page_title="AI Career Counselor", layout="wide")

# # ----------------- Custom CSS for Animations and Effects -----------------
# st.markdown(
#     """
#     <style>
#     .fade-in {
#         animation: fadeInAnimation 1s ease-in;
#         -webkit-animation: fadeInAnimation 1s ease-in;
#     }
#     @keyframes fadeInAnimation {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
#     @-webkit-keyframes fadeInAnimation {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
#     /* Enhance button appearance */
#     .stButton>button {
#         padding: 10px 20px;
#         font-size: 16px;
#         border-radius: 8px;
#         transition: transform 0.2s ease-in-out;
#     }
#     .stButton>button:hover {
#         transform: scale(1.05);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("🎓 AI Career Counselor")

# # Import assessment modules and utilities
# from assessments.iq_test import iq_test
# from assessments.big_five import big_five_test  # Assumes this returns a dict of scores
# from assessments.holland_code import holland_code_test
# from utils.scoring import get_recommendations
# from personal_info_form import render_personal_info_form

# # ----------------- Sidebar Navigation -----------------
# with st.sidebar:
#     st.title("🧭 Navigation")
#     st.markdown("### Steps")
#     st.markdown("1. Personal Info")
#     st.markdown("2. Aptitude Test")
#     st.markdown("3. Big Five Assessment")
#     st.markdown("4. Holland Code Test")
#     st.markdown("5. Recommendations, Analytics & Reports")

# # ----------------- Progress Indicator -----------------
# if "progress" not in st.session_state:
#     st.session_state.progress = 0

# def update_progress(step):
#     steps = {
#       1: 0.2,
#       2: 0.4,
#       3: 0.6,
#       4: 0.8,
#       5: 1.0
#     }
#     st.session_state.progress = steps.get(step, st.session_state.progress)
    
# st.progress(st.session_state.get("progress", 0))

# # ----------------- Helper: Safely encode text for PDF -----------------
# def safe_text(text):
#     """Convert text to a safe encoding for FPDF."""
#     return text.encode("latin-1", "replace").decode("latin-1")

# # ----------------- Helper: Generate PDF Report -----------------
# def generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(40, 10, safe_text("AI Career Counseling Report"), ln=True)
#     pdf.set_font("Arial", size=12)
#     pdf.cell(40, 10, safe_text(f"IQ Score: {iq_score}"), ln=True)
#     pdf.cell(40, 10, safe_text(f"Big Five Scores: {big_five_scores}"), ln=True)
#     pdf.cell(40, 10, safe_text(f"Holland Code: {holland_code_result}"), ln=True)
#     pdf.ln(10)
#     pdf.multi_cell(0, 10, safe_text(f"Recommendations: {recommendations}"))
    
#     # Instead of using a BytesIO, output the PDF as a string then encode it.
#     pdf_str = pdf.output(dest="S")
#     pdf_data = pdf_str.encode("latin-1")
#     return pdf_data


# # ----------------- Helper: Plot Market Trends Pie Chart -----------------
# def plot_market_trends_pie(trends_text):
#     """
#     Extract market trends percentages using regex and plot a pie chart.
#     Expected format in trends_text: "Technology: 40%, Healthcare: 25%, Finance: 15%, ..."
#     """
#     pattern = r"(\w+):\s*(\d+)%"
#     matches = re.findall(pattern, trends_text)
#     if matches:
#         labels = [match[0] for match in matches]
#         values = [int(match[1]) for match in matches]
#         fig = px.pie(names=labels, values=values, title="Market Trends by Sector")
#         st.plotly_chart(fig, use_container_width=True)
#     else:
#         st.info("Market trends data could not be parsed for visual analytics.")

# # ----------------- Tabs for Each Section -----------------
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📄 Personal Info",
#     "🧠 Aptitude Test",
#     "🌟 Big Five Assessment",
#     "🧭 Holland Code Test",
#     "🎯 Recommendations, Analytics & Reports"
# ])

# # ---------- TAB 1: Personal Info ----------
# with tab1:
#     st.header("Step 1: Personal Information")
#     user_data = render_personal_info_form()
#     if user_data:
#         st.session_state["user_data"] = user_data
#         st.success("✅ Profile submitted successfully!")
#         with st.expander("🔍 See Collected User Data"):
#             st.json(user_data)
#         update_progress(1)

# # ---------- TAB 2: IQ Test ----------
# with tab2:
#     st.header("Step 2: IQ Test")
#     with st.expander("🧠 Start IQ Test"):
#         iq_score = iq_test()
#         if iq_score is not None:
#             st.session_state["iq_score"] = iq_score
#             st.success(f"Your IQ Score: {iq_score}")
#             update_progress(2)

# # ---------- TAB 3: Big Five Assessment ----------
# with tab3:
#     st.header("Step 3: Big Five Personality Assessment")
#     with st.expander("📝 Begin Big Five Assessment"):
#         big_five_scores = big_five_test()  # Assumes this returns a dict of scores
#     if big_five_scores is not None:
#         st.session_state["big_five"] = big_five_scores
#         st.success("Big Five Assessment Completed!")
#         with st.expander("🔍 View Big Five Scores"):
#             st.json(big_five_scores)
#         update_progress(3)

# # ---------- TAB 4: Holland Code Test ----------
# with tab4:
#     st.header("Step 4: Holland Code Assessment")
#     holland_code_result = holland_code_test()
#     if holland_code_result is not None:
#         st.session_state["holland_code_result"] = holland_code_result
#         update_progress(4)

# # ---------- TAB 5: Recommendations, Analytics & Reports ----------
# with tab5:
#     st.header("Step 5: Get Career Recommendations and Analytics")
    
#     # Retrieve stored data from session state
#     user_data = st.session_state.get("user_data", {})
#     iq_score = st.session_state.get("iq_score")
#     big_five_scores = st.session_state.get("big_five")
#     holland_code_result = st.session_state.get("holland_code_result")
    
#     # Check if all steps are complete
#     def all_steps_completed():
#         checks = [
#             user_data and isinstance(user_data, dict),
#             iq_score is not None and isinstance(iq_score, (int, float)),
#             big_five_scores is not None and isinstance(big_five_scores, dict),
#             holland_code_result is not None and isinstance(holland_code_result, list)
#         ]
#         return all(checks)
    
#     with st.expander("🔍 Debug: Current State"):
#         st.write("User Data:", "Present" if user_data else "Missing")
#         st.write("IQ Score:", iq_score)
#         st.write("Big Five Scores:", big_five_scores)
#         st.write("Holland Code Result:", holland_code_result)
    
#     if all_steps_completed():
#         # Combine data for generating recommendations
#         full_user_data = {
#             "personal_info": user_data.get("personal_info", {}),
#             "career_interests": user_data.get("career_interests", {}),
#             "skills": user_data.get("skills", {}),
#             "future_aspirations": user_data.get("future_aspirations", {}),
#             "assessments": {
#                 "iq_score": iq_score,
#                 "big_five": big_five_scores,
#                 "holland_code": holland_code_result
#             }
#         }
    
#         if st.button("✨ Generate Recommendations"):
#             with st.spinner("Analyzing your profile..."):
#                 try:
#                     recommendations = get_recommendations(full_user_data)
#                     st.success("✅ Career Recommendations Generated!")
#                     st.write(recommendations)
#                     update_progress(5)
                    
#                     # ---------------- Visual Analytics Section (with fade-in) ----------------
#                     st.markdown('<div class="fade-in">', unsafe_allow_html=True)
#                     st.markdown("## 📊 Visual Analytics")
                    
#                     # Big Five Radar Chart
#                     def plot_big_five_radar(scores):
#                         labels = list(scores.keys())
#                         values = list(scores.values())
#                         angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
#                         values += values[:1]
#                         angles += angles[:1]
#                         fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
#                         ax.plot(angles, values, linewidth=2)
#                         ax.fill(angles, values, alpha=0.25)
#                         ax.set_xticks(angles[:-1])
#                         ax.set_xticklabels(labels)
#                         ax.set_title("🧠 Big Five Personality Radar")
#                         st.pyplot(fig)
                    
#                     if big_five_scores:
#                         plot_big_five_radar(big_five_scores)
                    
#                     # Holland Code Bar Chart
#                     def plot_holland_bar(codes):
#                         holland_count = {}
#                         for code in codes:
#                             holland_count[code] = holland_count.get(code, 0) + 1
#                         df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
#                         df = df.sort_values("Count", ascending=False)
#                         st.bar_chart(df.set_index("Trait"))
                    
#                     if holland_code_result:
#                         plot_holland_bar(holland_code_result)
                    
#                     # IQ Score Metric
#                     st.metric(label="🧠 IQ Score", value=iq_score, delta="Out of 200")
                    
#                     # Personal Info Analytics: 3D Chart for Career Interests
#                     def plot_personal_info_3d(user_data):
#                         career_interests = user_data.get("career_interests", {})
#                         primary_fields = career_interests.get("primary_fields", [])
#                         if not primary_fields:
#                             st.info("No career interests available for 3D analytics.")
#                             return
#                         df = pd.DataFrame({
#                             "Field": primary_fields,
#                             "Count": [1] * len(primary_fields),
#                             "Index": list(range(len(primary_fields)))
#                         })
#                         fig = px.scatter_3d(
#                             df, x="Field", y="Index", z="Count", size="Count",
#                             title="3D Analytics: Primary Career Fields",
#                             hover_name="Field"
#                         )
#                         fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
#                         st.plotly_chart(fig, use_container_width=True)
                    
#                     plot_personal_info_3d(user_data)
                    
#                     # ---------------- Market Trends Pie Chart ----------------
#                     from utils.market_analysis import market_trends
#                     with st.expander("📈 View Market Trends for Careers"):
#                         try:
#                             trends = market_trends()  # Expecting a string with sector percentages
#                             st.write(trends)
#                             plot_market_trends_pie(trends)
#                         except Exception as e:
#                             st.error(f"Error fetching market trends: {e}")
                    
#                     # ---------------- Exportable PDF Report ----------------
#                     pdf_data = generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score)
#                     st.download_button("📥 Download Report as PDF", data=pdf_data, file_name="career_report.pdf", mime="application/pdf")
                    
#                     st.markdown('</div>', unsafe_allow_html=True)
                            
#                 except Exception as e:
#                     st.error(f"❌ Error generating recommendations: {e}")
#     else:
#         st.warning("Please complete all previous steps before generating recommendations.")
#         st.info("Ensure you have:")
#         st.info("1. Submitted Personal Information")
#         st.info("2. Completed IQ Test")
#         st.info("3. Completed Big Five Assessment")
#         st.info("4. Completed Holland Code Test")



















# import streamlit as st
# import matplotlib.pyplot as plt
# import pandas as pd
# import plotly.express as px
# import re
# from fpdf import FPDF
# import tempfile
# import os
# import io
# from datetime import datetime

# # MUST be the first command!
# st.set_page_config(page_title="AI Career Counselor", layout="wide")

# # ----------------- Custom CSS for Animations and Effects -----------------
# st.markdown(
#     """
#     <style>
#     .fade-in {
#         animation: fadeInAnimation 1s ease-in;
#         -webkit-animation: fadeInAnimation 1s ease-in;
#     }
#     @keyframes fadeInAnimation {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
#     @-webkit-keyframes fadeInAnimation {
#         0% { opacity: 0; }
#         100% { opacity: 1; }
#     }
#     /* Enhance button appearance */
#     .stButton>button {
#         padding: 10px 20px;
#         font-size: 16px;
#         border-radius: 8px;
#         transition: transform 0.2s ease-in-out;
#     }
#     .stButton>button:hover {
#         transform: scale(1.05);
#     }
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# st.title("🎓 AI Career Counselor")

# # ----------------- Import Your Modules -----------------
# from assessments.iq_test import iq_test
# from assessments.big_five import big_five_test  # Assumes this returns a dict of scores
# from assessments.holland_code import holland_code_test
# from utils.scoring import get_recommendations
# from personal_info_form import render_personal_info_form

# # ----------------- Sidebar Navigation -----------------
# with st.sidebar:
#     st.title("🧭 Navigation")
#     st.markdown("### Steps")
#     st.markdown("1. Personal Info")
#     st.markdown("2. Aptitude Test")
#     st.markdown("3. Big Five Assessment")
#     st.markdown("4. Holland Code Test")
#     st.markdown("5. Recommendations, Analytics & Reports")

# # ----------------- Progress Indicator -----------------
# if "progress" not in st.session_state:
#     st.session_state.progress = 0

# def update_progress(step):
#     steps = {1: 0.2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1.0}
#     st.session_state.progress = steps.get(step, st.session_state.progress)

# st.progress(st.session_state.get("progress", 0))

# # ------------------ Helper Functions ------------------
# def safe_text(text):
#     """Ensure text is safe for PDF encoding."""
#     return text.encode("latin-1", "replace").decode("latin-1")

# def save_big_five_radar(scores, filename):
#     labels = list(scores.keys())
#     values = list(scores.values())
#     angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
#     values += values[:1]
#     angles += angles[:1]
#     fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
#     ax.plot(angles, values, linewidth=2)
#     ax.fill(angles, values, alpha=0.25)
#     ax.set_xticks(angles[:-1])
#     ax.set_xticklabels(labels)
#     ax.set_title("Big Five Personality Radar")
#     plt.savefig(filename, bbox_inches="tight")
#     plt.close(fig)

# def save_holland_bar_chart(codes, filename):
#     holland_count = {}
#     for code in codes:
#         holland_count[code] = holland_count.get(code, 0) + 1
#     df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
#     df = df.sort_values("Count", ascending=False)
#     fig, ax = plt.subplots(figsize=(6,4))
#     ax.bar(df["Trait"], df["Count"], color="skyblue")
#     ax.set_title("Holland Code Frequency")
#     plt.savefig(filename, bbox_inches="tight")
#     plt.close(fig)

# def save_personal_info_3d(user_data, filename):
#     career_interests = user_data.get("career_interests", {})
#     primary_fields = career_interests.get("primary_fields", [])
#     if not primary_fields:
#         return False
#     df = pd.DataFrame({
#         "Field": primary_fields,
#         "Count": [1] * len(primary_fields),
#         "Index": list(range(len(primary_fields)))
#     })
#     fig = px.scatter_3d(df, x="Field", y="Index", z="Count", size="Count",
#                           title="3D Analytics: Primary Career Fields",
#                           hover_name="Field")
#     fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
#     fig.write_image(filename)
#     return True

# def save_market_trends_pie(trends_text, filename):
#     pattern = r"(\w+):\s*(\d+)%"
#     matches = re.findall(pattern, trends_text)
#     if matches:
#         labels = [match[0] for match in matches]
#         values = [int(match[1]) for match in matches]
#         fig = px.pie(names=labels, values=values, title="Market Trends by Sector")
#         fig.write_image(filename)
#         return True
#     return False

# def generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score, trends_text):
#     pdf = FPDF()
#     pdf.add_page()
    
#     # Title Page
#     pdf.set_font("Arial", "B", 24)
#     pdf.cell(0, 20, safe_text("AI Career Counseling Report"), ln=True, align="C")
#     pdf.set_font("Arial", "I", 12)
#     pdf.cell(0, 10, safe_text("Generated on: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")), ln=True, align="C")
#     pdf.ln(20)
    
#     # Horizontal line separator
#     pdf.set_line_width(0.5)
#     pdf.line(10, pdf.get_y(), 200, pdf.get_y())
#     pdf.ln(10)
    
#     # Section: User Profile Summary
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, safe_text("User Profile Summary"), ln=True)
#     pdf.set_font("Arial", "", 12)
#     personal_info = user_data.get("personal_info", {})
#     for key, value in personal_info.items():
#         pdf.cell(0, 8, safe_text(f"{key.capitalize()}: {value}"), ln=True)
#     pdf.ln(5)
    
#     # Section: Assessment Overview
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, safe_text("Assessment Overview"), ln=True)
#     pdf.set_font("Arial", "", 12)
#     pdf.cell(0, 8, safe_text(f"IQ Score: {iq_score}"), ln=True)
#     pdf.cell(0, 8, safe_text(f"Big Five Scores: {big_five_scores}"), ln=True)
#     pdf.cell(0, 8, safe_text(f"Holland Code: {holland_code_result}"), ln=True)
#     pdf.ln(5)
    
#     # Section: Career Recommendations
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, safe_text("Career Recommendations"), ln=True)
#     pdf.set_font("Arial", "", 12)
#     pdf.multi_cell(0, 8, safe_text(recommendations))
#     pdf.ln(5)
    
#     # Prepare temporary files for charts
#     tmp_files = []
    
#     # Big Five Radar Chart
#     bf_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
#     bf_file.close()
#     save_big_five_radar(big_five_scores, bf_file.name)
#     tmp_files.append(bf_file.name)
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, safe_text("Big Five Radar Chart"), ln=True)
#     pdf.image(bf_file.name, w=100)
#     pdf.ln(10)
    
#     # Holland Code Bar Chart
#     hc_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
#     hc_file.close()
#     save_holland_bar_chart(holland_code_result, hc_file.name)
#     tmp_files.append(hc_file.name)
#     pdf.set_font("Arial", "B", 16)
#     pdf.cell(0, 10, safe_text("Holland Code Bar Chart"), ln=True)
#     pdf.image(hc_file.name, w=100)
#     pdf.ln(10)
    
#     # Personal Info 3D Chart
#     pi_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
#     pi_file.close()
#     if save_personal_info_3d(user_data, pi_file.name):
#         tmp_files.append(pi_file.name)
#         pdf.set_font("Arial", "B", 16)
#         pdf.cell(0, 10, safe_text("3D Analytics: Primary Career Fields"), ln=True)
#         pdf.image(pi_file.name, w=100)
#         pdf.ln(10)
    
#     # Market Trends Pie Chart
#     mt_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
#     mt_file.close()
#     if save_market_trends_pie(trends_text, mt_file.name):
#         tmp_files.append(mt_file.name)
#         pdf.set_font("Arial", "B", 16)
#         pdf.cell(0, 10, safe_text("Market Trends by Sector"), ln=True)
#         pdf.image(mt_file.name, w=100)
#         pdf.ln(10)
    
#     # Output PDF as bytes
#     pdf_str = pdf.output(dest="S")
#     pdf_data = pdf_str.encode("latin-1")
    
#     # Clean up temporary image files
#     for file in tmp_files:
#         os.remove(file)
    
#     return pdf_data

# # ------------------ End of Helper Functions ------------------

# # ------------------ Main Application ------------------
# # Create tabs for each section
# tab1, tab2, tab3, tab4, tab5 = st.tabs([
#     "📄 Personal Info",
#     "🧠 Aptitude Test",
#     "🌟 Big Five Assessment",
#     "🧭 Holland Code Test",
#     "🎯 Recommendations, Analytics & Reports"
# ])

# # ---------- TAB 1: Personal Info ----------
# with tab1:
#     st.header("Step 1: Personal Information")
#     user_data = render_personal_info_form()
#     if user_data:
#         st.session_state["user_data"] = user_data
#         st.success("✅ Profile submitted successfully!")
#         with st.expander("🔍 See Collected User Data"):
#             st.json(user_data)
#         update_progress(1)

# # ---------- TAB 2: IQ Test ----------
# with tab2:
#     st.header("Step 2: IQ Test")
#     with st.expander("🧠 Start IQ Test"):
#         iq_score = iq_test()
#         if iq_score is not None:
#             st.session_state["iq_score"] = iq_score
#             st.success(f"Your IQ Score: {iq_score}")
#             update_progress(2)

# # ---------- TAB 3: Big Five Assessment ----------
# with tab3:
#     st.header("Step 3: Big Five Personality Assessment")
#     with st.expander("📝 Begin Big Five Assessment"):
#         big_five_scores = big_five_test()  # Assumes returns a dict of scores
#     if big_five_scores is not None:
#         st.session_state["big_five"] = big_five_scores
#         st.success("Big Five Assessment Completed!")
#         with st.expander("🔍 View Big Five Scores"):
#             st.json(big_five_scores)
#         update_progress(3)

# # ---------- TAB 4: Holland Code Test ----------
# with tab4:
#     st.header("Step 4: Holland Code Assessment")
#     holland_code_result = holland_code_test()
#     if holland_code_result is not None:
#         st.session_state["holland_code_result"] = holland_code_result
#         update_progress(4)

# # ---------- TAB 5: Recommendations, Analytics & Reports ----------
# with tab5:
#     st.header("Step 5: Get Career Recommendations and Analytics")
#     # Retrieve stored data from session state
#     user_data = st.session_state.get("user_data", {})
#     iq_score = st.session_state.get("iq_score")
#     big_five_scores = st.session_state.get("big_five")
#     holland_code_result = st.session_state.get("holland_code_result")
    
#     def all_steps_completed():
#         return (
#             user_data and isinstance(user_data, dict)
#             and iq_score is not None and isinstance(iq_score, (int, float))
#             and big_five_scores is not None and isinstance(big_five_scores, dict)
#             and holland_code_result is not None and isinstance(holland_code_result, list)
#         )
    
#     with st.expander("🔍 Debug: Current State"):
#         st.write("User Data:", "Present" if user_data else "Missing")
#         st.write("IQ Score:", iq_score)
#         st.write("Big Five Scores:", big_five_scores)
#         st.write("Holland Code Result:", holland_code_result)
    
#     if all_steps_completed():
#         full_user_data = {
#             "personal_info": user_data.get("personal_info", {}),
#             "career_interests": user_data.get("career_interests", {}),
#             "skills": user_data.get("skills", {}),
#             "future_aspirations": user_data.get("future_aspirations", {}),
#             "assessments": {
#                 "iq_score": iq_score,
#                 "big_five": big_five_scores,
#                 "holland_code": holland_code_result
#             }
#         }
        
#         if st.button("✨ Generate Recommendations"):
#             with st.spinner("Analyzing your profile..."):
#                 try:
#                     recommendations = get_recommendations(full_user_data)
#                     st.success("✅ Career Recommendations Generated!")
#                     st.write(recommendations)
#                     update_progress(5)
                    
#                     # ---------------- Visual Analytics Section (with fade-in) ----------------
#                     st.markdown('<div class="fade-in">', unsafe_allow_html=True)
#                     st.markdown("## 📊 Visual Analytics")
                    
#                     # Big Five Radar Chart Display
#                     def plot_big_five_radar_display(scores):
#                         labels = list(scores.keys())
#                         values = list(scores.values())
#                         angles = [n / float(len(labels)) * 2 * 3.1416 for n in range(len(labels))]
#                         values += values[:1]
#                         angles += angles[:1]
#                         fig, ax = plt.subplots(figsize=(6,6), subplot_kw=dict(polar=True))
#                         ax.plot(angles, values, linewidth=2)
#                         ax.fill(angles, values, alpha=0.25)
#                         ax.set_xticks(angles[:-1])
#                         ax.set_xticklabels(labels)
#                         ax.set_title("🧠 Big Five Personality Radar")
#                         st.pyplot(fig)
                    
#                     if big_five_scores:
#                         plot_big_five_radar_display(big_five_scores)
                    
#                     # Holland Code Bar Chart Display
#                     def plot_holland_bar_display(codes):
#                         holland_count = {}
#                         for code in codes:
#                             holland_count[code] = holland_count.get(code, 0) + 1
#                         df = pd.DataFrame(list(holland_count.items()), columns=["Trait", "Count"])
#                         df = df.sort_values("Count", ascending=False)
#                         st.bar_chart(df.set_index("Trait"))
                    
#                     if holland_code_result:
#                         plot_holland_bar_display(holland_code_result)
                    
#                     # IQ Score Metric
#                     st.metric(label="🧠 IQ Score", value=iq_score, delta="Out of 200")
                    
#                     # Personal Info Analytics: 3D Chart Display
#                     # def plot_personal_info_3d_display(user_data):
#                     #     career_interests = user_data.get("career_interests", {})
#                     #     primary_fields = career_interests.get("primary_fields", [])
#                     #     if not primary_fields:
#                     #         st.info("No career interests available for 3D analytics.")
#                     #         return
#                     #     df = pd.DataFrame({
#                     #         "Field": primary_fields,
#                     #         "Count": [1] * len(primary_fields),
#                     #         "Index": list(range(len(primary_fields)))
#                     #     })
#                     #     fig = px.scatter_3d(df, x="Field", y="Index", z="Count", size="Count",
#                     #                           title="3D Analytics: Primary Career Fields",
#                     #                           hover_name="Field")
#                     #     fig.update_layout(scene_camera=dict(eye=dict(x=1.5, y=1.5, z=1.5)))
#                     #     st.plotly_chart(fig, use_container_width=True)
                    
#                     # plot_personal_info_3d_display(user_data)
                    
#                     # # Market Trends Pie Chart Display
#                     # from utils.market_analysis import market_trends
#                     # trends_text = ""
#                     # try:
#                     #     trends_text = market_trends()  # Expected to return a string like "Tech: 40%, Healthcare: 25%, Finance: 15%, ..."
#                     #     st.write("Market Trends:", trends_text)
#                     # except Exception as e:
#                     #     st.error(f"Error fetching market trends: {e}")
                    
#                     def plot_market_trends_pie_display(trends_text):
#                         pattern = r"(\w+):\s*(\d+)%"
#                         matches = re.findall(pattern, trends_text)
#                         if matches:
#                             labels = [match[0] for match in matches]
#                             values = [int(match[1]) for match in matches]
#                             fig = px.pie(names=labels, values=values, title="Market Trends by Sector")
#                             st.plotly_chart(fig, use_container_width=True)
#                         else:
#                             st.info("Market trends data could not be parsed for visual analytics.")
                    
#                     if trends_text:
#                         plot_market_trends_pie_display(trends_text)
                    
#                     # ---------------- Exportable PDF Report ----------------
#                     pdf_data = generate_pdf_report(user_data, recommendations, big_five_scores, holland_code_result, iq_score, trends_text)
#                     st.download_button("📥 Download Report as PDF", data=pdf_data, file_name="career_report.pdf", mime="application/pdf")
                    
#                     st.markdown('</div>', unsafe_allow_html=True)
                            
#                 except Exception as e:
#                     st.error(f"❌ Error generating recommendations: {e}")
#     else:
#         st.warning("Please complete all previous steps before generating recommendations.")
#         st.info("Ensure you have:")
#         st.info("1. Submitted Personal Information")
#         st.info("2. Completed IQ Test")
#         st.info("3. Completed Big Five Assessment")
#         st.info("4. Completed Holland Code Test")
















