"""
Data Upload component — handles file upload, preview, and quality assessment.
"""

import streamlit as st
import pandas as pd
import plotly.express as px


def show_upload():
    st.header("📁 Data Upload Center")
    st.markdown("Upload your CSV file to begin your data analysis journey")

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type="csv",
        help="Upload your CSV file to get started with professional data analysis",
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        try:
            st.success("✅ File uploaded successfully!")
            df = pd.read_csv(uploaded_file)
            st.session_state.data = df.copy()
            st.session_state.original_data = df.copy()

            _render_upload_metrics(df)
            _render_data_preview(df)
            _render_column_analysis(df)
            _render_quality_assessment(df)

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")
            st.info("Please ensure your file is a valid CSV format with proper encoding (UTF-8 recommended)")
    else:
        st.info("👆 Please upload a CSV file to get started with data analysis")
        _render_sample_format()


def _render_upload_metrics(df: pd.DataFrame):
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📋 Columns", df.shape[1])
    with col3:
        st.metric("❌ Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024:.1f} KB")
    with col5:
        st.metric("🔍 Duplicates", df.duplicated().sum())


def _render_data_preview(df: pd.DataFrame):
    st.subheader("📋 Data Preview")
    st.markdown("First 10 rows of your dataset:")
    st.dataframe(df.head(10), use_container_width=True, height=350)


def _render_column_analysis(df: pd.DataFrame):
    st.subheader("📊 Column Analysis")
    col_info = pd.DataFrame({
        'Column Name': df.columns,
        'Data Type': df.dtypes.astype(str),
        'Non-Null Count': df.count(),
        'Null Count': df.isnull().sum(),
        'Null %': (df.isnull().sum() / len(df) * 100).round(2),
        'Unique Values': [df[col].nunique() for col in df.columns]
    })
    st.dataframe(col_info, use_container_width=True, height=300)


def _render_quality_assessment(df: pd.DataFrame):
    st.subheader("🎯 Data Quality Assessment")
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    quality_score = ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📈 Data Completeness", f"{quality_score:.1f}%")
        if quality_score >= 90:
            st.success("🟢 Excellent data quality!")
        elif quality_score >= 70:
            st.warning("🟡 Good data quality with minor issues")
        else:
            st.error("🔴 Data quality needs improvement")
    with col2:
        dtype_counts = df.dtypes.value_counts()
        fig_pie = px.pie(values=dtype_counts.values, names=dtype_counts.index,
                         title="Data Types Distribution")
        fig_pie.update_layout(height=300)
        st.plotly_chart(fig_pie, use_container_width=True)


def _render_sample_format():
    st.subheader("📝 Expected CSV Format")
    st.markdown("Your CSV should look something like this:")
    sample_data = pd.DataFrame({
        'Employee_ID': [1001, 1002, 1003, 1004],
        'Name': ['John Smith', 'Jane Doe', 'Bob Johnson', 'Alice Brown'],
        'Department': ['IT', 'HR', 'Finance', 'Marketing'],
        'Age': [28, 34, 31, 29],
        'Salary': [55000, 75000, 68000, 62000],
        'Performance_Score': [85, 92, 78, 90]
    })
    st.dataframe(sample_data, use_container_width=True)