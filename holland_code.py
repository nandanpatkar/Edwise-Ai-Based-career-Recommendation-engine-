
import streamlit as st
from collections import defaultdict

# --- Constants ---
SCORE_OPTIONS = {
    "Strongly Dislike": 1,
    "Dislike": 2,
    "Neutral": 3,
    "Like": 4,
    "Strongly Like": 5
}

CODE_TO_TYPE = {
    "R": "Realistic", "I": "Investigative", "A": "Artistic",
    "S": "Social", "E": "Enterprising", "C": "Conventional"
}

# --- Questions ---
def get_holland_questions():
    return [
        (1, "Repair a dishwasher", "R"),
        (2, "Use precision machines to build custom metal parts", "R"),
        (3, "Analyze the structure of molecules", "I"),
        (4, "Do scientific experiments", "I"),
        (5, "Design a magazine cover", "A"),
        (6, "Paint a portrait", "A"),
        (7, "Teach social skills to disabled children", "S"),
        (8, "Teach adults to read", "S"),
        (9, "Coordinate a business conference", "E"),
        (10, "Plan a marketing strategy for a new company", "E"),
        (11, "Track monthly expenses for a company", "C"),
        (12, "Review financial records for accuracy", "C"),
        (59, "Collect tax payments", "C"),
        (60, "Develop a budget for a city government", "C")
    ]

# --- Scoring ---
def calculate_holland_scores(responses):
    questions = get_holland_questions()
    trait_totals = defaultdict(int)
    trait_counts = defaultdict(int)

    for q_id, _, code in questions:
        trait = CODE_TO_TYPE[code]
        trait_counts[trait] += 1
        score = SCORE_OPTIONS.get(responses.get(q_id), 3)  # default to Neutral
        trait_totals[trait] += score

    normalized_scores = {}
    for trait in trait_totals:
        max_score = trait_counts[trait] * 5
        normalized_scores[trait] = round((trait_totals[trait] / max_score) * 50)

    return normalized_scores

def holland_code_test():
    st.title("🧭 Holland Career Test")

    # Initialize responses dictionary
    if 'holland_responses' not in st.session_state:
        st.session_state.holland_responses = {}

    questions = get_holland_questions()
    
    # Render questions
    for q_id, text, code in questions:
        # Use unique key and store in session state
        st.session_state.holland_responses[q_id] = st.radio(
            f"{q_id}. {text}",
            list(SCORE_OPTIONS.keys()),
            horizontal=True,
            key=f"holland_q_{q_id}"
        )

    if st.button("Submit Holland Code Test", key="holland_submit"):
        # Calculate scores
        scores = calculate_holland_scores(st.session_state.holland_responses)
        st.session_state["holland_scores"] = scores

        # Determine top 3 Holland Code types
        top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
        top_3_codes = [code[0][0] for code in top_3]

        # Store the Holland Code result in session state
        st.session_state["holland_code_result"] = top_3_codes

        # Display results
        st.success("Holland Code Test Completed!")
        st.subheader("Your Holland Code Types:")
        
        # Format and display detailed type descriptions
        code_names = {
            "R": "Realistic (Doers)",
            "I": "Investigative (Thinkers)",
            "A": "Artistic (Creators)",
            "S": "Social (Helpers)",
            "E": "Enterprising (Persuaders)",
            "C": "Conventional (Organizers)"
        }
        
        for code in top_3_codes:
            st.write(f"- {code}: {code_names.get(code, 'Unknown')}")

        return top_3_codes

    # Return existing result if already submitted
    return st.session_state.get("holland_code_result", None)

























































































 # assessments/holland_code.py
# import streamlit as st

# def holland_code_test():
#     st.header("Holland Code (RIASEC) Test")
#     categories = ["Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"]
#     scores = {}

#     for category in categories:
#         scores[category] = st.slider(f"Interest in {category} activities", 1, 10, 5)

#     sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#     holland_code = "".join([score[0][0] for score in sorted_scores[:3]])

#     return holland_code







# import streamlit as st

# def holland_code_test():
#     st.subheader("🧭 Holland Code (RIASEC) Test")
#     categories = ["Realistic", "Investigative", "Artistic", "Social", "Enterprising", "Conventional"]
#     scores = {}

#     for category in categories:
#         scores[category] = st.slider(f"{category}", 1, 10, 5, key=f"hc_{category}")

#     if st.button("Submit Holland Code"):
#         sorted_categories = sorted(scores.items(), key=lambda x: x[1], reverse=True)
#         holland_code = ''.join([cat[0][0] for cat in sorted_categories[:3]])
#         st.session_state["holland_code"] = holland_code
#         st.success(f"Your Holland Code is: {holland_code}")

#     return st.session_state.get("holland_code", None)



















# import streamlit as st
# from collections import defaultdict
# import plotly.graph_objects as go

# # --- Setup ---
# # st.set_page_config(page_title="🧭 Holland Career Test", layout="wide")

# # --- Constants ---
# SCORE_OPTIONS = {
#     "Strongly Dislike": 1,
#     "Dislike": 2,
#     "Neutral": 3,
#     "Like": 4,
#     "Strongly Like": 5
# }

# CODE_TO_TYPE = {
#     "R": "Realistic", "I": "Investigative", "A": "Artistic",
#     "S": "Social", "E": "Enterprising", "C": "Conventional"
# }

# # --- Questions ---
# def get_holland_questions():
#     return [
#         (1, "Repair a dishwasher", "R"),
#         (2, "Use precision machines to build custom metal parts", "R"),
#         (3, "Analyze the structure of molecules", "I"),
#         (4, "Do scientific experiments", "I"),
#         (5, "Design a magazine cover", "A"),
#         (6, "Paint a portrait", "A"),
#         (7, "Teach social skills to disabled children", "S"),
#         (8, "Teach adults to read", "S"),
#         (9, "Coordinate a business conference", "E"),
#         (10, "Plan a marketing strategy for a new company", "E"),
#          (11, "Track monthly expenses for a company", "C"),
#         (12, "Review financial records for accuracy", "C"),
#         (13, "Install a hardwood floor", "R"),
#         (14, "Repair an air conditioning system", "R"),
#         (15, "Research the properties of nuclear energy", "I"),
#         (16, "Research a new medicine", "I"),
#         (17, "Design a greeting card", "A"),
#         (18, "Illustrate a children’s book", "A"),
#         (19, "Help a disabled person with their daily routine", "S"),
#         (20, "Tutor a child with a learning disability", "S"),
#         (21, "Negotiate business partnerships", "E"),
#         (22, "Motivate employees to achieve success", "E"),
#         (23, "Keep payroll records", "C"),
#         (24, "Use spreadsheets to organize financial data", "C"),
#         (25, "Install an alarm system in a building", "R"),
#         (26, "Install kitchen cabinets", "R"),
#         (27, "Look at cells through a microscope", "I"),
#         (28, "Work in a chemistry lab", "I"),
#         (29, "Design magazine ads", "A"),
#         (30, "Write a script for a television show", "A"),
#         (31, "Counsel a person recovering from drug addiction", "S"),
#         (32, "Counsel a person with depression", "S"),
#         (33, "Hire and fire employees", "E"),
#         (34, "Close an important business deal", "E"),
#         (35, "Check tax returns for errors", "C"),
#         (36, "Calculate the cost of an insurance claim", "C"),
#         (37, "Build a stone wall", "R"),
#         (38, "Operate a bulldozer", "R"),
#         (39, "Analyze soil samples for pollution", "I"),
#         (40, "Study a fault line to predict earthquakes", "I"),
#         (41, "Design a billboard advertisement", "A"),
#         (42, "Edit a movie", "A"),
#         (43, "Plan educational games for preschool children", "S"),
#         (44, "Plan activities for elderly people", "S"),
#         (45, "Lead a team", "E"),
#         (46, "Start a new business", "E"),
#         (47, "Calculate the cost of a construction project", "C"),
#         (48, "Help customers fill out loan applications", "C"),
#         (49, "Take apart a car engine", "R"),
#         (50, "Inspect a roof for leaks", "R"),
#         (51, "Do laboratory tests to diagnose diseases", "I"),
#         (52, "Research heat-resistant materials for airplane engines", "I"),
#         (53, "Compose a song", "A"),
#         (54, "Write a poem", "A"),
#         (55, "Help diabetic patients plan a proper diet", "S"),
#         (56, "Help a needy family find appropriate housing", "S"),
#         (57, "Give a speech in front of many people", "E"),
#         (58, "Persuade others to my point of view", "E"),
#         (59, "Collect tax payments", "C"),
#         (60, "Develop a budget for a city government", "C")
#     ]

# # --- Scoring ---
# def calculate_holland_scores(responses):
#     questions = get_holland_questions()
#     trait_totals = defaultdict(int)
#     trait_counts = defaultdict(int)

#     for q_id, _, code in questions:
#         trait = CODE_TO_TYPE[code]
#         trait_counts[trait] += 1
#         score = SCORE_OPTIONS.get(responses.get(q_id), 3)  # default to Neutral
#         trait_totals[trait] += score

#     normalized_scores = {}
#     for trait in trait_totals:
#         max_score = trait_counts[trait] * 5
#         normalized_scores[trait] = round((trait_totals[trait] / max_score) * 50)

#     return normalized_scores


# def summarize_holland_code(code_list):
#     code_names = {
#         "R": "Realistic (doers)",
#         "I": "Investigative (thinkers)",
#         "A": "Artistic (creators)",
#         "S": "Social (helpers)",
#         "E": "Enterprising (persuaders)",
#         "C": "Conventional (organizers)"
#     }
#     descriptions = [f"{code}: {code_names.get(code, 'Unknown')}" for code in code_list]
#     return ", ".join(descriptions)

# def holland_code_test():
#     st.title("🧭 Holland Career Test")

#     responses = {}
#     questions = get_holland_questions()
#     for q_id, text, code in questions:
#         responses[q_id] = st.radio(
#             f"{q_id}. {text}",
#             list(SCORE_OPTIONS.keys()),
#             horizontal=True,
#             key=f"holland_q_{q_id}"
#         )
#     if st.button("Submit", key="holland_submit"):
#         st.write("✅ Submit clicked")

#         scores = calculate_holland_scores(responses)
#         st.session_state["holland_scores"] = scores

#         top_3 = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]
#         top_3_codes = [code[0][0] for code in top_3]  # R, I, A, S, E, C

#         st.session_state["holland_code_result"] = top_3_codes

#         st.write("✅ Stored holland_code_result:", top_3_codes)














    # if st.button("Submit", key="holland_submit"):
    #     scores = calculate_holland_scores(responses)
    #     st.session_state["holland_scores"] = scores

    #     # ✅ Get top 3 codes from scores and return them
    #     sorted_traits = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    #     top_3_codes = [trait[0][0] for trait in sorted_traits[:3]]  # first letter of trait name

    #     st.session_state["holland_code_result"] = top_3_codes  # 👈 store it in session
    #     st.success("Holland Code submitted!")

    #     st.subheader("Your Top Holland Types:")
    #     st.write(summarize_holland_code(top_3_codes))

    #     return top_3_codes  # ✅ return this

    # If not submitted yet
    # return None



# --- Radar Chart ---
# def show_holland_radar_chart(scores):
#     categories = list(scores.keys())
#     values = list(scores.values())

#     fig = go.Figure(go.Scatterpolar(
#         r=values + [values[0]],
#         theta=categories + [categories[0]],
#         fill='toself',
#         line_color="crimson"
#     ))

#     fig.update_layout(
#         title="Holland Career Code - Radar Chart",
#         polar=dict(radialaxis=dict(visible=True, range=[0, 50])),
#         showlegend=False,
#         margin=dict(t=50, b=50)
#     )

#     st.plotly_chart(fig, use_container_width=True)

# --- Main App ---
# def holland_code_test():
#     st.title("🧭 Holland Career Interest Test")
#     st.write("Rate how much you would enjoy each activity:")

#     responses = {}

#     questions = get_holland_questions()
#     for q_id, text, code in questions:
#      responses[q_id] = st.radio(
#         f"{q_id}. {text}",
#         list(SCORE_OPTIONS.keys()),
#         horizontal=True,
#         key=f"holland_q_{q_id}"  # unique key per question
#     )

#     if st.button("Submit", key="hollabd_code_submit"):

#         scores = calculate_holland_scores(responses)
#         st.session_state["holland_scores"] = scores
#         st.success("Test submitted successfully! ✅")
#         st.subheader("Your Holland Code Scores:")
#         st.code(scores, language="python")
        # show_holland_radar_chart(scores)

# i
    