
import streamlit as st
from collections import defaultdict
from utils.gemini_api import query_gemini
from utils.session_helpers import get_safe_user_data  # or wherever you placed it

user_data = get_safe_user_data()

if st.button("Generate Recommendations", key="generate_recs"):
    recommendations = get_recommendations(user_data)
    st.subheader("🎯 Personalized Career Recommendations")
    st.write(recommendations)

def summarize_big_five(traits):
    summary = []
    for trait, score in traits.items():
        if score >= 75:
            level = "high"
        elif score >= 50:
            level = "moderate"
        else:
            level = "low"
        summary.append(f"{trait.capitalize()}: {level}")
    return ", ".join(summary)




def summarize_holland_code(code_list):
    code_names = {
        "R": "Realistic (doers)",
        "I": "Investigative (thinkers)",
        "A": "Artistic (creators)",
        "S": "Social (helpers)",
        "E": "Enterprising (persuaders)",
        "C": "Conventional (organizers)"
    }
    descriptions = [f"{code}: {code_names.get(code, 'Unknown')}" for code in code_list]
    return ", ".join(descriptions)


# st.write("🔍 Debug: Current Holland Code Result")
# st.write(st.session_state.get("holland_code_result"))
user_data = {
    "personal_info": st.session_state.get("personal_info", {}),
    "career_interests": st.session_state.get("career_interests", {}),
    "skills": st.session_state.get("skills", {}),
    "future_aspirations": st.session_state.get("future_aspirations", {}),
    "assessments": {
        "iq_score": st.session_state.get("iq_score", "N/A"),
        "big_five": st.session_state.get("big_five", {}),
        "holland_code": st.session_state.get("holland_code_result", [])
    }
}

def get_recommendations(user_data):
    # personal = user_data["personal_info"]
    personal = user_data.get("personal_info", {
    "name": "N/A",
    "age": "N/A",
    "gender": "N/A",
    "location": "N/A",
    "education": "N/A",
    "language": "N/A"
})

    interests = user_data["career_interests"]
    skills = user_data["skills"]
    aspirations = user_data["future_aspirations"]
    assessments = user_data.get("assessments", {})
    assessments = {
    "big_five": st.session_state.get("big_five", {}),
    "holland_code": st.session_state.get("holland_code_result", [])
}
    big_five_summary = summarize_big_five(assessments.get("big_five", {}))
    holland_summary = summarize_holland_code(assessments.get("holland_code", []))

    iq_score = assessments.get("iq_score", "N/A")

    prompt = f"""
You are an expert AI career counselor with deep knowledge of the Indian job market and education system. Analyze the detailed profile and assessment results below, and provide 3-5 highly personalized career path recommendations that align with the user's unique background. Your response must be structured, actionable, and culturally relevant for an Indian context.

===========================
USER PROFILE
===========================
Personal Information:
- Name: {personal['name']}
- Age: {personal['age']}
- Gender: {personal['gender']}
- Location (State/City): {personal['location']}
- Current Education: {personal['education']}
- Preferred Language: {personal['language']}
- Family Background: {personal.get('family_background', 'Not specified')}
- Financial Constraints: {personal.get('financial_constraints', 'Not specified')}

Career Interests:
- Primary Fields: {', '.join(interests['primary_fields'])}
- Career Priorities: {interests['priorities']}
- Tech Subfields: {', '.join(interests.get('tech_subfields', []))}
- Business Subfields: {', '.join(interests.get('business_subfields', []))}
- Engineering Subfields: {', '.join(interests.get('eng_subfields', []))}
- Healthcare Subfields: {', '.join(interests.get('healthcare_subfields', []))}
- Creative Subfields: {', '.join(interests.get('creative_subfields', []))}

Skills Assessment:
- Technical Skills: {', '.join(skills['tech_skills'])}
- Business Skills: {', '.join(skills['business_skills'])}
- Creative Skills: {', '.join(skills['creative_skills'])}
- Soft Skills: {', '.join(skills['soft_skills'])}
- Language Proficiency: {', '.join(skills['language_skills'])}
- Academic Strengths: {', '.join(skills.get('academic_strengths', []))}

Future Aspirations:
- Dream Job/Role: {aspirations['dream_job']}
- 5-Year Career Plan: {aspirations['five_years']}
- Openness to Career Change: {aspirations['career_change']}
- Work-Life Balance Preference: {aspirations.get('work_life_balance', 'Not specified')}
- Salary Expectations: {aspirations.get('salary_expectations', 'Not specified')}
- Geographic Mobility: {aspirations.get('geographic_mobility', 'Not specified')}

Assessment Results:
- IQ Score: {iq_score}
- Big Five Personality Summary: {big_five_summary}
- Holland Code Personality Types: {holland_summary}
# - Multiple Intelligence Profile: 
- Learning Style:

===========================
CAREER RECOMMENDATIONS
===========================
For each recommended career path, include the following sections:

Career Path [Number]: [Career Title]

1. Why This Is an Ideal Match:
   - Explain how the career aligns with the user's personality, strengths, interests, and values.
   - Reference relevant assessment results (e.g., Holland Code, Big Five) to justify the fit.
   - Discuss how the career aligns with Indian cultural and work environment norms.

2. Education Pathway in India:
   - Recommend the appropriate academic stream (Science/Commerce/Arts/Other) and degree programs.
   - List top Indian institutions and specify required entrance exams (e.g., JEE, NEET, CAT, CLAT, GATE).
   - Mention alternative qualification routes (diplomas, certifications) with estimated timelines and costs.

3. Skill Development Plan:
   - Identify essential skills to develop immediately.
   - Suggest relevant online learning platforms (both Indian and international), industry-recognized certifications, and local training programs.
   - Recommend books, podcasts, and other resources in the user's preferred language.

4. Indian Market Outlook:
   - Describe the current demand in various regions (metro cities vs. tier 2/3 cities).
   - Provide salary ranges for entry-level, mid-level, and senior positions (in ₹) and growth projections (5-10 years).
   - Highlight prominent employers, startups, and potential entrepreneurial opportunities.

5. Next Steps:
   - Offer actionable steps for immediate career development (networking, resume building, interview tips).
   - Recommend relevant professional associations and networking opportunities in India.

Conclude with a motivational and culturally sensitive message that acknowledges the user’s potential, addresses family expectations, and encourages practical steps toward achieving their career goals.
"""



    return query_gemini(prompt)





# prompt 
# 
# You are an AI career counselor. Based on the user's full profile and assessment results below, suggest 3–5 highly personalized career paths. For each, provide:
# - A short summary of why this career fits the user's profile.
# - What skills, education, or certifications are needed to succeed.
# - Any additional tips to get started in this field.


#  prompt = f"""

# You are an AI career counselor for the Indian market. Based on the user's complete profile and assessment results provided below, suggest 3–5 highly personalized career paths that are well-suited to the Indian context. For each career option, include:

# Why this career is a good fit for the user's personality, strengths, interests, and values.

# Required qualifications, skills, and certifications in India, including suggested academic streams, entrance exams, or online/offline learning platforms.

# Potential career growth, demand in the Indian job market, and scope for entrepreneurship or freelancing (if applicable).
# ### Personal Information:
# - Name: {personal['name']}
# - Age: {personal['age']}
# - Gender: {personal['gender']}
# - Location: {personal['location']}
# - Education: {personal['education']}
# - Preferred Language: {personal['language']}

# ### Career Interests:
# - Primary Fields: {', '.join(interests['primary_fields'])}
# - Career Priority: {interests['priorities']}
# - Tech Subfields: {', '.join(interests.get('tech_subfields', []))}
# - Business Subfields: {', '.join(interests.get('business_subfields', []))}
# - Engineering Subfields: {', '.join(interests.get('eng_subfields', []))}

# ### Skills:
# - Technical: {', '.join(skills['tech_skills'])}
# - Business: {', '.join(skills['business_skills'])}
# - Creative: {', '.join(skills['creative_skills'])}
# - Soft: {', '.join(skills['soft_skills'])}
# - Languages: {', '.join(skills['language_skills'])}

# ### Future Aspirations:
# - Dream Job: {aspirations['dream_job']}
# - 5-Year Plan: {aspirations['five_years']}
# - Open to career change: {aspirations['career_change']}

# ### Assessment Results:
# - IQ Score: {iq_score}
# - Big Five Personality Summary: {big_five_summary}
# - Holland Code Personality Types: {holland_summary}

# Consider all of the above and generate motivational, practical career suggestions that align with the user's skills, values, and personality.
# """









 

# def get_recommendations(user_data):
#     personal = user_data["personal_info"]
#     interests = user_data["career_interests"]
#     skills = user_data["skills"]
#     aspirations = user_data["future_aspirations"]

#     prompt = f"""
# You are an AI career counselor. Based on the user's profile below, suggest 3–5 personalized career paths, with explanations for each, and required skills/education.

# Personal Info:
# - Name: {personal['name']}
# - Age: {personal['age']}
# - Gender: {personal['gender']}
# - Location: {personal['location']}
# - Education: {personal['education']}
# - Preferred Language: {personal['language']}

# Career Interests:
# - Primary Fields: {', '.join(interests['primary_fields'])}
# - Career Priority: {interests['priorities']}
# - Tech Subfields: {', '.join(interests['tech_subfields'])}
# - Business Subfields: {', '.join(interests['business_subfields'])}
# - Engineering Subfields: {', '.join(interests['eng_subfields'])}

# Skills:
# - Technical: {', '.join(skills['tech_skills'])}
# - Business: {', '.join(skills['business_skills'])}
# - Creative: {', '.join(skills['creative_skills'])}
# - Soft: {', '.join(skills['soft_skills'])}
# - Languages: {', '.join(skills['language_skills'])}

# Future Aspirations:
# - Dream Job: {aspirations['dream_job']}
# - 5-Year Plan: {aspirations['five_years']}
# - Open to career change: {aspirations['career_change']}

# Provide helpful, practical, and motivating recommendations.
# """

#     return query_gemini(prompt)