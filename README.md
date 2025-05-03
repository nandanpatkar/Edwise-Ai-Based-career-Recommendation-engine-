# Edvise: AI-Based Career Assessment Engine

Empower your future with Edvise – AI-driven career guidance you can trust.

---

## 🚀 Features

- 🎯 Personalized Career Recommendations  
  AI-driven suggestions based on personality, cognitive abilities, skills, and interests.

- 🧪 Comprehensive Assessments  
  Includes Big Five and Holland Code personality tests, adaptive aptitude and cognitive evaluations.

- 💬 Explainable AI  
  Each recommendation includes a natural language explanation for transparency.

- 📊 Interactive Dashboard  
  View assessment results, track progress, and download reports.

- 🛠 Admin Panel  
  Manage users, update assessments, and monitor system performance.

- 🔒 Secure & Scalable  
  Built with JWT-based auth, SQLite DB, and modular Python backend.

---

## 🧰 Tech Stack

- Frontend: Streamlit
- Backend: Python
- Database: SQLite
- Machine Learning: Decision Trees, SVM, Neural Networks, LLMs
- Authentication: JWT

---

## ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/edvise-career-assessment.git
cd edvise-career-assessment

# 2. Set up a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py

🧪 Usage
Register or log in to your account.

Complete the Big Five, Holland Code, and Aptitude tests.

Receive career suggestions backed by explainable AI.

Explore your dashboard and download personalized reports.

Admins can manage users, assessments, and system logs via the Admin Panel.

edvise-career-assessment/
│
├── app.py
├── requirements.txt
├── /modules
│   ├── authentication.py
│   ├── assessment.py
│   ├── recommendation.py
│   └── admin.py
├── /data
│   ├── career_dataset.csv
│   └── user_data.db
└── /static


🤝 Contributing
We welcome contributions!

Fork the repo and create your branch (git checkout -b feature/feature-name)

Commit your changes (git commit -am 'Add some feature')

Push to the branch (git push origin feature/feature-name)

Open a Pull Request
