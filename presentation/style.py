import streamlit as st

PRIMARY_COLOR = "#ffb347"
SECONDARY_COLOR = "#2c6bed"
BG_COLOR = "#f9fafc"

def inject_global_style():
    st.markdown(f"""
    <style>
        body {{ background-color: {BG_COLOR}; font-family: 'Inter', sans-serif; }}
        h1, h2, h3 {{ color: #222; }}
        .stButton button {{
            background-color: {PRIMARY_COLOR};
            color: white;
            border-radius: 8px;
            font-weight: 600;
        }}
        .stButton button:hover {{ background-color: #ffa500; }}
        .navbar {{
            display: flex; justify-content: space-between; align-items: center;
            background: white; padding: 1rem 2rem; border-radius: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
    </style>
    """, unsafe_allow_html=True)
