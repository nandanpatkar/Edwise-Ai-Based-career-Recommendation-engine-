# utils/market_analysis.py
from .gemini_api import query_gemini

def market_trends():
    prompt = """
You are an expert career advisor AI assistant helping users make informed decisions based on real-time job market trends.

Provide a detailed analysis of the current job market trends and future outlook across top career fields. Highlight:
- Fast-growing industries in 2024–2025
- In-demand roles and skill sets in technology, healthcare, business, and other major sectors
- Emerging career paths powered by AI, automation, and sustainability
- Key global and regional trends (especially in India and Asia)
- Career fields that are declining or transforming

Summarize this in a clear, insightful way that helps users align their strengths and interests with future opportunities.
"""

    return query_gemini(prompt)
