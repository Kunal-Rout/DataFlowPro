"""
DataFlow Pro — Entry Point
All UI logic lives in src/components/. This file only handles routing.
"""

import warnings
warnings.filterwarnings('ignore')

import streamlit as st
from src.config.settings import APP_CONFIG, NAV_PAGES
from src.utils.style_helpers import inject_custom_css, render_page_title
from src.components.home import show_home
from src.components.upload import show_upload
from src.components.cleaning import show_cleaning
from src.components.visualization import show_visualization
from src.components.correlation import show_correlation
from src.components.statistics import show_statistics

# Page configuration
st.set_page_config(**APP_CONFIG)

# Initialize session state
if 'data' not in st.session_state:
    st.session_state.data = None
if 'original_data' not in st.session_state:
    st.session_state.original_data = None


def main():
    inject_custom_css()
    render_page_title("📊 DataFlow Pro")
    st.markdown("### Professional Data Analytics Without Coding")

    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio("Go to", NAV_PAGES)

    page_map = {
        "🏠 Home": show_home,
        "📁 Data Upload": show_upload,
        "🧹 Data Cleaning": show_cleaning,
        "📈 Data Visualization": show_visualization,
        "🔗 Correlation Analysis": show_correlation,
        "📊 Statistical Summary": show_statistics,
    }

    page_map[page]()


if __name__ == "__main__":
    main()