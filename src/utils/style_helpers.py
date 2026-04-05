"""
CSS injection and reusable metric display utilities.
"""

import streamlit as st


def inject_custom_css():
    st.markdown("""
    <style>
        .main > div {
            padding-top: 2rem;
        }
        .metric-card {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            border-left: 5px solid #1f77b4;
        }
        .stSelectbox > div > div {
            background-color: white;
        }
        .title-style {
            font-size: 3rem;
            font-weight: bold;
            background: linear-gradient(90deg, #1f77b4, #ff7f0e);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.5rem;
        }
    </style>
    """, unsafe_allow_html=True)


def render_page_title(title: str):
    st.markdown(f'<h1 class="title-style">{title}</h1>', unsafe_allow_html=True)