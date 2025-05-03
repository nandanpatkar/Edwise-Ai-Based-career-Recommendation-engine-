

import streamlit as st

# Likert scale mapping
OPTIONS = {
    "Strongly Disagree": 1,
    "Disagree": 2,
    "Neutral": 3,
    "Agree": 4,
    "Strongly Agree": 5
}

# Questions with reverse flag
QUESTIONS = {
    "Openness": [
        (11, "I enjoy exploring abstract philosophical questions.", False),
        (12, "I prefer sticking to tried-and-tested methods.", True),
        (13, "I often come up with creative solutions to problems.", False),
        (14, "I am fascinated by artistic expressions.", False),
        (15, "I enjoy learning about different cultures and traditions.", False),
        (16, "I find theoretical discussions boring.", True),
        (17, "I enjoy experimenting with new ways of doing things.", False),
        (18, "I prefer practical, concrete activities over abstract ones.", True),
        (19, "I seek out new experiences and sensations.", False),
        (20, "I enjoy contemplating art and natural beauty.", False),
    ],
    "Conscientiousness": [
        (21, "I follow a strict schedule in my daily life.", False),
        (22, "I tend to procrastinate on important tasks.", True),
        (23, "I pay attention to small details in my work.", False),
        (24, "I keep my belongings well organized.", False),
        (25, "I complete tasks thoroughly.", False),
        (26, "I often misplace things.", True),
        (27, "I make plans and stick to them.", False),
        (28, "I leave my work until the last minute.", True),
        (29, "I set high standards for myself and others.", False),
        (30, "I am methodical in my work.", False),
    ],
    "Extraversion": [
        (31, "Large social gatherings energize me.", False),
        (32, "I prefer working alone to working in teams.", True),
        (33, "I naturally take charge in group situations.", False),
        (34, "I enjoy being the center of attention.", False),
        (35, "I start conversations with others.", False),
        (36, "I need quiet time to recharge.", True),
        (37, "I make friends easily.", False),
        (38, "I prefer small, intimate gatherings to large parties.", True),
        (39, "I express my opinions assertively.", False),
        (40, "I enjoy meeting new people.", False),
    ],
    "Agreeableness": [
        (41, "I prioritize others' needs before my own.", False),
        (42, "In conflicts, I stand firm on my position.", True),
        (43, "I enjoy helping others even without recognition.", False),
        (44, "I sympathize with others' feelings.", False),
        (45, "I give people the benefit of the doubt.", False),
        (46, "I can be argumentative.", True),
        (47, "I cooperate well with others.", False),
        (48, "I tend to be skeptical of others' intentions.", True),
        (49, "I avoid confrontations.", False),
        (50, "I try to see the best in people.", False),
    ],
    "Neuroticism": [
        (51, "Small setbacks can seriously discourage me.", False),
        (52, "I remain calm under pressure.", True),
        (53, "I often worry about things that might go wrong.", False),
        (54, "I experience frequent mood swings.", False),
        (55, "I get stressed easily.", False),
        (56, "I handle uncertainty well.", True),
        (57, "I am easily frustrated.", False),
        (58, "I recover quickly from emotional setbacks.", True),
        (59, "I doubt my abilities.", False),
        (60, "I am sensitive to criticism.", False),
    ]
}

def calculate_big_five_scores(responses):
    # Calculate raw scores
    trait_scores = {}
    trait_levels = {}
    
    for trait, items in QUESTIONS.items():
        score = 0
        for idx, _, reverse in items:
            val = OPTIONS[responses[idx]]
            # Reverse scoring for reverse-coded items
            score += (6 - val) if reverse else val
        
        # Normalize to 0-100 scale
        normalized_score = int((score / (len(items) * 5)) * 100)
        trait_scores[trait.lower()] = normalized_score
        
        # Determine trait level
        if normalized_score >= 75:
            trait_levels[trait.lower()] = "high"
        elif normalized_score >= 50:
            trait_levels[trait.lower()] = "moderate"
        else:
            trait_levels[trait.lower()] = "low"
    
    # Determine top personality trait
    top_trait = max(trait_scores, key=trait_scores.get)
    
    return {
        "scores": trait_scores,
        "levels": trait_levels,
        "top_trait": top_trait
    }

def big_five_test():
    st.title("🌟 Big Five Personality Assessment")

    # Initialize responses dictionary
    responses = {}
    
    # Render questions for each trait
    for trait, items in QUESTIONS.items():
        st.subheader(f"{trait}")
        for idx, text, _ in items:
            responses[idx] = st.radio(
                label=text,
                options=list(OPTIONS.keys()),
                horizontal=True,
                key=f"q_{idx}"
            )

    if st.button("Submit Assessment", key="big_five_submit"):
        # Calculate scores
        result = calculate_big_five_scores(responses)
        
        # Store in session state
        st.session_state["big_five"] = result["scores"]
        st.session_state["big_five_levels"] = result["levels"]
        st.session_state["top_trait"] = result["top_trait"]
        
        # Display results
        st.success("Assessment completed successfully!")
        
        # Display scores
        st.subheader("🔢 Trait Scores")
        st.json(result["scores"])
        
        # Display trait levels
        st.subheader("📊 Trait Levels")
        st.json(result["levels"])
        
        # Display top trait
        st.subheader("🏆 Top Personality Trait")
        st.write(f"**{result['top_trait'].capitalize()}**: {result['scores'][result['top_trait']]} - {result['levels'][result['top_trait']]}")
        
        return result["scores"]
    
    # Return existing result if already submitted
    return st.session_state.get("big_five", None)


















































































































































































































































































































































































































































































































































































































































































































































































































































# import streamlit as st
# import plotly.graph_objects as go

# # st.set_page_config(page_title="🌟 Big 5 Personality Assessment", layout="wide")

# # Questions Data
# questions = {
#     "Openness": [
#         (11, "I enjoy exploring abstract philosophical questions.", False),
#         (12, "I prefer sticking to tried-and-tested methods.", True),
#         (13, "I often come up with creative solutions to problems.", False),
#         (14, "I am fascinated by artistic expressions.", False),
#         (15, "I enjoy learning about different cultures and traditions.", False),
#         (16, "I find theoretical discussions boring.", True),
#         (17, "I enjoy experimenting with new ways of doing things.", False),
#         (18, "I prefer practical, concrete activities over abstract ones.", True),
#         (19, "I seek out new experiences and sensations.", False),
#         (20, "I enjoy contemplating art and natural beauty.", False),
#     ],
#     "Conscientiousness": [
#         (21, "I follow a strict schedule in my daily life.", False),
#         (22, "I tend to procrastinate on important tasks.", True),
#         (23, "I pay attention to small details in my work.", False),
#         (24, "I keep my belongings well organized.", False),
#         (25, "I complete tasks thoroughly.", False),
#         (26, "I often misplace things.", True),
#         (27, "I make plans and stick to them.", False),
#         (28, "I leave my work until the last minute.", True),
#         (29, "I set high standards for myself and others.", False),
#         (30, "I am methodical in my work.", False),
#     ],
#     "Extraversion": [
#         (31, "Large social gatherings energize me.", False),
#         (32, "I prefer working alone to working in teams.", True),
#         (33, "I naturally take charge in group situations.", False),
#         (34, "I enjoy being the center of attention.", False),
#         (35, "I start conversations with others.", False),
#         (36, "I need quiet time to recharge.", True),
#         (37, "I make friends easily.", False),
#         (38, "I prefer small, intimate gatherings to large parties.", True),
#         (39, "I express my opinions assertively.", False),
#         (40, "I enjoy meeting new people.", False),
#     ],
#     "Agreeableness": [
#         (41, "I prioritize others' needs before my own.", False),
#         (42, "In conflicts, I stand firm on my position.", True),
#         (43, "I enjoy helping others even without recognition.", False),
#         (44, "I sympathize with others' feelings.", False),
#         (45, "I give people the benefit of the doubt.", False),
#         (46, "I can be argumentative.", True),
#         (47, "I cooperate well with others.", False),
#         (48, "I tend to be skeptical of others' intentions.", True),
#         (49, "I avoid confrontations.", False),
#         (50, "I try to see the best in people.", False),
#     ],
#     "Neuroticism": [
#         (51, "Small setbacks can seriously discourage me.", False),
#         (52, "I remain calm under pressure.", True),
#         (53, "I often worry about things that might go wrong.", False),
#         (54, "I experience frequent mood swings.", False),
#         (55, "I get stressed easily.", False),
#         (56, "I handle uncertainty well.", True),
#         (57, "I am easily frustrated.", False),
#         (58, "I recover quickly from emotional setbacks.", True),
#         (59, "I doubt my abilities.", False),
#         (60, "I am sensitive to criticism.", False),
#     ]
# }

# # Score calculation
# def calculate_scores(responses):
#     trait_scores = {}
#     for trait, items in questions.items():
#         score = 0
#         for idx, _, reverse in items:
#             val = responses[idx]
#             score += (6 - val) if reverse else val
#         trait_scores[trait.lower()] = int((score / (len(items)*5)) * 100)
#     return trait_scores






# # Main UI
# def big_five_test():
#     st.title("🌟 Big Five Personality Assessment")

#     responses = {}
#     for trait, items in questions.items():
#         st.subheader(f"**{trait}**")
#         for idx, text, reverse in items:
#             responses[idx] = st.radio(text, [1, 2, 3, 4, 5], horizontal=True, key=f"q{idx}")

#     if st.button("Submit", key="big_five_submit"):
#         scores = calculate_scores(responses)
#         st.session_state["big_five"] = scores
#         st.success("Assessment submitted successfully!")

#         st.subheader("🧠 Trait Scores")
#         st.write(scores)

#         st.subheader("📝 Personality Insights")
#         show_trait_insights(scores)

#         # radar_chart(scores)
#         return scores  # Send scores back to app.py
#     else:
#         return st.session_state.get("big_five", None)

# def show_trait_insights(scores):
#     descriptions = {
#         "openness": "creative, curious, and open to new experiences.",
#         "conscientiousness": "organized, responsible, and detail-oriented.",
#         "extraversion": "outgoing, energetic, and social.",
#         "agreeableness": "empathetic, cooperative, and caring.",
#         "neuroticism": "emotionally reactive and sensitive to stress (lower scores indicate emotional stability)."
#     }

#     for trait, score in scores.items():
#         level = "High" if score >= 75 else "Moderate" if score >= 50 else "Low"
#         desc = descriptions[trait]
#         st.markdown(f"- **{trait.capitalize()}**: {level} — {desc}")



  










        # radar_chart(scores)









# def radar_chart(scores):
#     categories = list(scores.keys())
#     values = list(scores.values())

#     fig = go.Figure(go.Scatterpolar(
#         r=values + [values[0]],
#         theta=categories + [categories[0]],
#         fill='toself'
#     ))

#     fig.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0,100])),
#         showlegend=False
#     )

#     st.plotly_chart(fig, use_container_width=True)


    







# # assessments/big_five.py
# import streamlit as st

# def big_five_test():
#     st.header("Big Five Personality Test")
#     traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
#     scores = {}

#     for trait in traits:
#         scores[trait] = st.slider(f"Rate your {trait}", 1, 10, 5)

#     return scores






# import streamlit as st

# def big_five_test():
#     st.subheader("🌟 Big Five Personality Assessment")
#     traits = ["Openness", "Conscientiousness", "Extraversion", "Agreeableness", "Neuroticism"]
#     big_five = {}

#     for trait in traits:
#         score = st.slider(f"{trait}", 1, 10, 5, key=f"bf_{trait}")
#         big_five[trait] = score

#     if st.button("Submit Big Five Assessment"):
#         st.session_state["big_five"] = big_five
#         st.success("Big Five assessment submitted.")

#     return st.session_state.get("big_five", None)










# import streamlit as st
# # import plotly.graph_objects as go

# # st.set_page_config(page_title="🌟 Big 5 Personality Assessment", layout="wide")

# # Likert scale mapping
# options = {
#     "Strongly Disagree": 1,
#     "Disagree": 2,
#     "Neutral": 3,
#     "Agree": 4,
#     "Strongly Agree": 5
# }

# # Questions with reverse flag
# questions = {
#     "Openness": [
#         (11, "I enjoy exploring abstract philosophical questions.", False),
#         (12, "I prefer sticking to tried-and-tested methods.", True),
#         (13, "I often come up with creative solutions to problems.", False),
#         (14, "I am fascinated by artistic expressions.", False),
#         (15, "I enjoy learning about different cultures and traditions.", False),
#         (16, "I find theoretical discussions boring.", True),
#         (17, "I enjoy experimenting with new ways of doing things.", False),
#         (18, "I prefer practical, concrete activities over abstract ones.", True),
#         (19, "I seek out new experiences and sensations.", False),
#         (20, "I enjoy contemplating art and natural beauty.", False),
#     ],
#     "Conscientiousness": [
#         (21, "I follow a strict schedule in my daily life.", False),
#         (22, "I tend to procrastinate on important tasks.", True),
#         (23, "I pay attention to small details in my work.", False),
#         (24, "I keep my belongings well organized.", False),
#         (25, "I complete tasks thoroughly.", False),
#         (26, "I often misplace things.", True),
#         (27, "I make plans and stick to them.", False),
#         (28, "I leave my work until the last minute.", True),
#         (29, "I set high standards for myself and others.", False),
#         (30, "I am methodical in my work.", False),
#     ],
#     "Extraversion": [
#         (31, "Large social gatherings energize me.", False),
#         (32, "I prefer working alone to working in teams.", True),
#         (33, "I naturally take charge in group situations.", False),
#         (34, "I enjoy being the center of attention.", False),
#         (35, "I start conversations with others.", False),
#         (36, "I need quiet time to recharge.", True),
#         (37, "I make friends easily.", False),
#         (38, "I prefer small, intimate gatherings to large parties.", True),
#         (39, "I express my opinions assertively.", False),
#         (40, "I enjoy meeting new people.", False),
#     ],
#     "Agreeableness": [
#         (41, "I prioritize others' needs before my own.", False),
#         (42, "In conflicts, I stand firm on my position.", True),
#         (43, "I enjoy helping others even without recognition.", False),
#         (44, "I sympathize with others' feelings.", False),
#         (45, "I give people the benefit of the doubt.", False),
#         (46, "I can be argumentative.", True),
#         (47, "I cooperate well with others.", False),
#         (48, "I tend to be skeptical of others' intentions.", True),
#         (49, "I avoid confrontations.", False),
#         (50, "I try to see the best in people.", False),
#     ],
#     "Neuroticism": [
#         (51, "Small setbacks can seriously discourage me.", False),
#         (52, "I remain calm under pressure.", True),
#         (53, "I often worry about things that might go wrong.", False),
#         (54, "I experience frequent mood swings.", False),
#         (55, "I get stressed easily.", False),
#         (56, "I handle uncertainty well.", True),
#         (57, "I am easily frustrated.", False),
#         (58, "I recover quickly from emotional setbacks.", True),
#         (59, "I doubt my abilities.", False),
#         (60, "I am sensitive to criticism.", False),
#     ]
# }

# def calculate_scores(responses):
#     trait_scores = {}
#     for trait, items in questions.items():
#         score = 0
#         for idx, _, reverse in items:
#             val = options[responses[idx]]
#             score += (6 - val) if reverse else val
#         trait_scores[trait.lower()] = int((score / (len(items)*5)) * 100)
#     return trait_scores


# def  big_five_test():
#     st.title("🌟 Big Five Personality Test")

#     responses = {}
#     for trait, items in questions.items():
#         st.subheader(f"{trait}")
#         for idx, text, _ in items:
#             responses[idx] = st.radio(
#                 label=text,
#                 options=list(options.keys()),
#                 horizontal=True,
#                 key=f"q_{idx}"
#             )

#     if st.button("Submit", key="big_five_submit"):

#         scores = calculate_scores(responses)
#         st.session_state["big_five"] = scores
#         st.success("Assessment submitted successfully!")

#         st.subheader("📊 Personality Trait Scores")
#         st.code(scores, language="python")
#         # radar_chart(scores)


 







# def radar_chart(scores):
#     categories = list(scores.keys())
#     values = list(scores.values())

#     fig = go.Figure(go.Scatterpolar(
#         r=values + [values[0]],
#         theta=categories + [categories[0]],
#         fill='toself'
#     ))

#     fig.update_layout(
#         polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
#         showlegend=False
#     )

#     st.plotly_chart(fig, use_container_width=True)

# Streamlit main app
