
import streamlit as st
# st.set_page_config(page_title="Personal Information and Interests Form", layout="wide")
def render_personal_info_form():

    

    # Set page title
    

    # Header Section
    # st.title("Personal Information and Interests Form")
    # st.write("Please fill out the following details to help us understand your profile better.")

    # 1. Personal Information Section
    # st.header("1. Personal Information")
    name = st.text_input("Full Name", placeholder="Enter your full name")
    age = st.number_input("Age", min_value=1, max_value=100, step=1)
    gender = st.radio("Gender", options=["Male", "Female", "Non-Binary", "Prefer not to say"])
    email = st.text_input("Email Address", placeholder="Enter your email address")
    phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    location = st.text_input("Location (City/State)", placeholder="Enter your location")
    education = st.selectbox("Education Level", options=["High School", "Undergraduate", "Postgraduate", "Doctorate", "Other"])
    language = st.selectbox("Preferred Language", options=["English", "Hindi", "Spanish", "French", "Other"])

    # 2. Career Interests Section
    st.header("2. Career Interests")
    primary_fields = st.multiselect(
        "Primary Career Fields",
        options=[
            "Technology", "Medicine and Healthcare", "Engineering", "Business and Management",
            "Arts and Humanities", "Science and Research", "Media and Communication",
            "Education and Teaching", "Law and Public Policy", "Other"
        ],
    )

    # Store subfields selections in session state
    if "Technology" in primary_fields:
        tech_subfields = st.multiselect(
            "Subfields in Technology",
            options=[
                "Artificial Intelligence", "Data Science", "Software Development", "Cybersecurity",
                "Web Development", "Mobile App Development", "Cloud Computing",
                "Blockchain", "Game Development", "Internet of Things (IoT)"
            ],
            key="tech_subfields"
        )

    if "Medicine and Healthcare" in primary_fields:
        med_subfields = st.multiselect(
            "Subfields in Medicine and Healthcare",
            options=[
                "Pediatrics", "Dentistry", "Nursing", "Psychiatry",
                "Pharmacology", "Physiotherapy", "Surgery", "Radiology",
                "Public Health", "Medical Research"
            ],
            key="med_subfields"
        )

    if "Engineering" in primary_fields:
        eng_subfields = st.multiselect(
            "Subfields in Engineering",
            options=[
                "Civil", "Mechanical", "Electrical", "Robotics",
                "Aerospace", "Biomedical", "Chemical", "Environmental",
                "Software Engineering", "Structural Engineering"
            ],
            key="eng_subfields"
        )

    if "Business and Management" in primary_fields:
        business_subfields = st.multiselect(
            "Subfields in Business and Management",
            options=[
                "Marketing", "Finance", "Entrepreneurship", "Human Resources",
                "Operations Management", "International Business", "Supply Chain Management",
                "Sales", "Business Analytics", "Consulting"
            ],
            key="business_subfields"
        )

    if "Arts and Humanities" in primary_fields:
        arts_subfields = st.multiselect(
            "Subfields in Arts and Humanities",
            options=[
                "Literature", "Visual Arts", "History", "Philosophy",
                "Performing Arts", "Archaeology", "Cultural Studies",
                "Linguistics", "Theology", "Creative Writing"
            ],
            key="arts_subfields"
        )

    if "Science and Research" in primary_fields:
        science_subfields = st.multiselect(
            "Subfields in Science and Research",
            options=[
                "Physics", "Chemistry", "Biology", "Environmental Science",
                "Astronomy", "Genetics", "Microbiology", "Material Science",
                "Earth Sciences", "Mathematics"
            ],
            key="science_subfields"
        )

    if "Media and Communication" in primary_fields:
        media_subfields = st.multiselect(
            "Subfields in Media and Communication",
            options=[
                "Journalism", "Public Relations", "Advertising", "Content Writing",
                "Digital Media", "Film and Television", "Graphic Design",
                "Social Media Management", "Broadcasting", "Photography"
            ],
            key="media_subfields"
        )

    if "Education and Teaching" in primary_fields:
        education_subfields = st.multiselect(
            "Subfields in Education and Teaching",
            options=[
                "Primary Education", "Secondary Education", "Special Education",
                "Higher Education", "Curriculum Design", "Educational Technology",
                "Counseling", "Adult Education", "Online Education", "Language Instruction"
            ],
            key="education_subfields"
        )

    if "Law and Public Policy" in primary_fields:
        law_subfields = st.multiselect(
            "Subfields in Law and Public Policy",
            options=[
                "Corporate Law", "Criminal Law", "International Law", "Human Rights",
                "Environmental Law", "Taxation Law", "Public Administration",
                "Policy Analysis", "Political Science", "Legislative Affairs"
            ],
            key="law_subfields"
        )

    priorities = st.selectbox(
        "Top Priority in a Career",
        options=["High Salary", "Work-Life Balance", "Opportunities for Growth", "Making an Impact", "Creativity", "Stability"],
    )

    # 3. Skills Assessment
    st.header("3. Skills Assessment")

    # Technical Skills
    tech_skills = st.multiselect(
        "Technical Skills",
        options=[
            "Python", "Java", "JavaScript", "C++", "SQL", "HTML/CSS",
            "React", "Node.js", "Docker", "AWS", "Azure", "Git",
            "Machine Learning", "Data Analysis", "Cloud Computing",
            "Network Security", "DevOps", "Mobile Development"
        ]
    )

    # Business Skills
    business_skills = st.multiselect(
        "Business Skills",
        options=[
            "Project Management", "Business Analysis", "Strategic Planning",
            "Financial Analysis", "Marketing Strategy", "Sales",
            "Customer Relationship Management", "Leadership", "Team Management",
            "Negotiations", "Business Development", "Risk Management"
        ]
    )

    # Creative Skills
    creative_skills = st.multiselect(
        "Creative Skills",
        options=[
            "Graphic Design", "UI/UX Design", "Video Editing",
            "Content Writing", "Digital Marketing", "Animation",
            "Photography", "Illustration", "3D Modeling",
            "Motion Graphics", "Brand Design", "Social Media Management"
        ]
    )

    # Soft Skills
    soft_skills = st.multiselect(
        "Soft Skills",
        options=[
            "Communication", "Problem Solving", "Critical Thinking",
            "Time Management", "Adaptability", "Teamwork",
            "Leadership", "Emotional Intelligence", "Conflict Resolution",
            "Decision Making", "Work Ethic", "Active Listening"
        ]
    )

    # Language Skills
    language_skills = st.multiselect(
        "Language Skills",
        options=[
            "English", "Spanish", "French", "German", "Chinese",
            "Japanese", "Arabic", "Russian", "Portuguese", "Hindi"
        ]
    )

    # Proficiency Levels
    if any([tech_skills, business_skills, creative_skills, soft_skills, language_skills]):
        st.subheader("Skill Proficiency Levels")
        st.write("For your selected skills, please indicate proficiency levels:")

        all_skills = {
           "tech": tech_skills,
           "business": business_skills,
           "creative": creative_skills,
           "soft": soft_skills,
           "language": language_skills
}

        for category, skills in all_skills.items():
          for skill in skills:
           st.select_slider(
            f"Proficiency in {skill}",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
            key=f"proficiency_{category}_{skill}"
            )

    # Certifications
    certifications = st.text_area("List any relevant certifications", placeholder="e.g., AWS Certified Solutions Architect, PMP, etc.")

    # 4. Hobbies and Personal Interests Section
    st.header("4. Hobbies and Personal Interests")
    hobbies = st.multiselect(
        "Select your Hobbies",
        options=["Reading", "Writing", "Sports", "Traveling", "Music", "Gaming", "Cooking",
                 "Gardening", "Photography", "Crafting/DIY", "Painting", "Meditation", "Dancing", "Other"]
    )
    team_preference = st.radio("Do you prefer working in teams or individually?", options=["Teams", "Individually", "Both"])
    public_speaking = st.radio("Are you comfortable with public speaking?", options=["Yes", "No", "Somewhat"])
    analytical_or_creative = st.radio("Do you consider yourself more analytical or creative?", options=["Analytical", "Creative", "Balanced"])

    # 5. Future Aspirations Section
    st.header("5. Future Aspirations")
    dream_job = st.text_input("What is your dream job or role?", placeholder="Enter your dream job")
    five_years = st.text_area("Where do you see yourself in the next 5 years?", placeholder="Describe your aspirations")
    career_change = st.radio("Are you open to pursuing a completely different career field if recommended?", options=["Yes", "No", "Maybe"])

    # 6. Additional Information
    st.header("6. Additional Information")
    special_considerations = st.text_area("Do you have any special considerations we should be aware of?", placeholder="Enter any special considerations")
    career_suggestions = st.radio("Would you like career suggestions based on your profile?", options=["Yes", "No"])

    # Submit Button with Comprehensive Summary
    if st.button("Submit"):
        st.success("Thank you for submitting the form! Your information has been recorded.")
#        
        # Return the collected data as a dictionary
        return {
            "personal_info": {
                "name": name,
                "age": age,
                "gender": gender,
                "email": email,
                "phone": phone,
                "location": location,
                "education": education,
                "language": language
            },
            "career_interests": {
                "primary_fields": primary_fields,
                "tech_subfields": st.session_state.get("tech_subfields", []),
                "med_subfields": st.session_state.get("med_subfields", []),
                "eng_subfields": st.session_state.get("eng_subfields", []),
                "business_subfields": st.session_state.get("business_subfields", []),
                "arts_subfields": st.session_state.get("arts_subfields", []),
                "science_subfields": st.session_state.get("science_subfields", []),
                "media_subfields": st.session_state.get("media_subfields", []),
                "education_subfields": st.session_state.get("education_subfields", []),
                "law_subfields": st.session_state.get("law_subfields", []),
                "priorities": priorities
            },
            "skills": {
                "tech_skills": tech_skills,
                "business_skills": business_skills,
                "creative_skills": creative_skills,
                "soft_skills": soft_skills,
                "language_skills": language_skills
            },
            "certifications": certifications,
            "hobbies_interests": {
                "hobbies": hobbies,
                "team_preference": team_preference,
                "public_speaking": public_speaking,
                "analytical_or_creative": analytical_or_creative
            },
            "future_aspirations": {
                "dream_job": dream_job,
                "five_years": five_years,
                "career_change": career_change
            },
            "additional_info": {
                "special_considerations": special_considerations,
                "career_suggestions": career_suggestions
            }
        }
