"""
Statistical Summary component.
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from src.utils.data_helpers import get_column_summary


def show_statistics():
    st.header("📊 Comprehensive Statistical Analysis")

    if st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first!")
        return

    df = st.session_state.data
    st.markdown("Deep dive into your data with professional statistical insights")

    _render_overview_metrics(df)
    full_stats = _render_descriptive_stats(df)
    _render_quality_charts(df)
    _render_column_analysis(df)
    _render_export_section(df, full_stats)


def _render_overview_metrics(df):
    st.subheader("📋 Dataset Overview")
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("📊 Total Rows", f"{len(df):,}")
    with col2:
        st.metric("📋 Total Columns", len(df.columns))
    with col3:
        st.metric("💾 Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
    with col4:
        st.metric("🎯 Data Completeness", f"{((df.size - df.isnull().sum().sum()) / df.size * 100):.1f}%")
    with col5:
        st.metric("🗑️ Duplicate Rows", f"{df.duplicated().sum():,}")


def _render_descriptive_stats(df):
    st.subheader("📈 Descriptive Statistics")
    numeric_df = df.select_dtypes(include=[np.number])
    categorical_df = df.select_dtypes(include=['object', 'category'])
    full_stats = None

    if not numeric_df.empty:
        st.markdown("**🔢 Numerical Columns:**")
        desc_stats = numeric_df.describe().round(2)
        additional_stats = pd.DataFrame({
            col: {
                'variance': numeric_df[col].var(),
                'skewness': numeric_df[col].skew(),
                'kurtosis': numeric_df[col].kurtosis()
            } for col in numeric_df.columns
        }).round(3)
        full_stats = pd.concat([desc_stats, additional_stats])
        st.dataframe(full_stats, use_container_width=True, height=400)

        st.markdown("**🎯 Key Insights:**")
        for col in numeric_df.columns:
            skew = numeric_df[col].skew()
            if abs(skew) > 1:
                skew_desc = "highly skewed"
            elif abs(skew) > 0.5:
                skew_desc = "moderately skewed"
            else:
                skew_desc = "approximately normal"
            st.write(f"• **{col}**: {skew_desc} (skewness: {skew:.2f})")

    if not categorical_df.empty:
        st.markdown("**📝 Categorical Columns:**")
        cat_stats = pd.DataFrame({
            'Column': categorical_df.columns,
            'Unique Values': [categorical_df[col].nunique() for col in categorical_df.columns],
            'Most Frequent': [categorical_df[col].mode().iloc[0] if not categorical_df[col].mode().empty else 'N/A'
                              for col in categorical_df.columns],
            'Frequency': [categorical_df[col].value_counts().iloc[0] if len(categorical_df[col].value_counts()) > 0 else 0
                          for col in categorical_df.columns]
        })
        st.dataframe(cat_stats, use_container_width=True)

    return full_stats


def _render_quality_charts(df):
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📊 Data Types Distribution")
        dtype_counts = df.dtypes.value_counts()
        fig = px.pie(values=dtype_counts.values,
                     names=[str(d) for d in dtype_counts.index],
                     title="Distribution of Data Types")
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("❌ Missing Values Analysis")
        missing_df = pd.DataFrame({
            'Column': df.columns,
            'Missing Count': df.isnull().sum(),
            'Missing Percentage': (df.isnull().sum() / len(df) * 100).round(2)
        })
        missing_df = missing_df[missing_df['Missing Count'] > 0].sort_values('Missing Count', ascending=False)
        if not missing_df.empty:
            fig = px.bar(missing_df, x='Column', y='Missing Percentage',
                         title="Missing Values by Column (%)")
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.success("🎉 No missing values found in your dataset!")


def _render_column_analysis(df):
    st.subheader("🔍 Detailed Column Analysis")
    analysis_df = get_column_summary(df)
    st.dataframe(analysis_df, use_container_width=True, height=400)
    return analysis_df


def _render_export_section(df, full_stats):
    st.subheader("💾 Export Your Analysis")
    col1, col2, col3 = st.columns(3)
    analysis_df = get_column_summary(df)

    with col1:
        if st.button("📊 Download Statistical Summary", use_container_width=True):
            if full_stats is not None:
                csv = full_stats.to_csv()
                st.download_button("📊 Download CSV", csv, "statistical_summary.csv", "text/csv")

    with col2:
        if st.button("📋 Download Column Analysis", use_container_width=True):
            csv = analysis_df.to_csv(index=False)
            st.download_button("📋 Download CSV", csv, "column_analysis.csv", "text/csv")

    with col3:
        if st.button("🔧 Download Cleaned Data", use_container_width=True):
            csv = df.to_csv(index=False)
            st.download_button("🔧 Download CSV", csv, "cleaned_data.csv", "text/csv")