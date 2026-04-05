"""
Home page component.
"""

import streamlit as st


def show_home():
    st.markdown("""
    ## Welcome to DataFlow Pro! 🚀

    **Professional Data Analytics Made Simple** - Transform your raw CSV data into powerful insights without writing a single line of code.

    ### ✨ Key Features:
    - **📁 Smart CSV Upload** with instant data preview and validation
    - **🧹 Advanced Data Cleaning** with multiple preprocessing options
    - **📊 Rich Statistical Analysis** including descriptive statistics and data quality reports
    - **📈 Interactive Visualizations** - bar charts, line plots, scatter diagrams, pie charts, histograms, and box plots
    - **🔗 Correlation Intelligence** with heatmaps to discover hidden relationships
    - **📋 Multi-column Comparisons** for comprehensive data exploration
    - **🎨 Professional Themes** with dark/light mode support
    - **⚡ Lightning-fast Processing** with optimized performance

    ### 👥 Perfect For:
    - **📈 Data Analysts** - Advanced analytics and statistical insights
    - **🧑‍💼 Business Managers** - Executive dashboards and KPI tracking
    - **🚀 Product Teams** - User behavior analysis and metrics
    - **🎓 Researchers & Students** - Academic data analysis and learning
    - **💼 Consultants** - Client data exploration and reporting
    - **🏢 Small Business Owners** - Sales and operations analytics

    ### 🛠️ Powered By:
    - **Python 3.11+** - Latest language features
    - **Streamlit** - Modern web framework
    - **Pandas & NumPy** - Industry-standard data processing
    - **Matplotlib & Seaborn** - Statistical visualization
    - **Plotly** - Interactive charts and graphs

    ---

    ### 🎯 Quick Start Guide:

    1. **📁 Upload Your Data** → Go to 'Data Upload' and select your CSV file
    2. **🧹 Clean Your Data** → Handle missing values and format issues
    3. **📊 Explore Statistics** → View comprehensive data summaries
    4. **📈 Create Visualizations** → Generate interactive charts
    5. **🔗 Find Correlations** → Discover relationships in your data
    6. **💾 Export Results** → Download your cleaned and analyzed data

    **Ready to unlock your data's potential? Start by uploading your CSV file! →**
    """)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🚀 Features", "50+", delta="Advanced")
    with col2:
        st.metric("⚡ Processing", "Fast", delta="Optimized")
    with col3:
        st.metric("🎨 Charts", "6 Types", delta="Interactive")
    with col4:
        st.metric("💡 No Code", "100%", delta="User-Friendly")