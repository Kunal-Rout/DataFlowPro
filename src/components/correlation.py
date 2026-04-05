"""
Correlation Analysis component.
"""

import streamlit as st
import numpy as np
import plotly.express as px
from src.config.constants import CORRELATION_COLOR_SCALES
from src.utils.data_helpers import get_numeric_columns, get_categorical_columns
from src.utils.chart_helpers import build_correlation_heatmap, build_scatter_with_trendline


def show_correlation():
    st.header("🔗 Correlation Analysis")

    if st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first!")
        return

    df = st.session_state.data
    numeric_df = df.select_dtypes(include=[np.number])

    if len(numeric_df.columns) < 2:
        st.error("❌ Need at least 2 numeric columns for correlation analysis")
        return

    st.markdown("Discover hidden relationships and patterns in your numerical data")

    corr_matrix = numeric_df.corr()

    _render_heatmap(corr_matrix)
    _render_strong_correlations(corr_matrix)
    _render_pairwise_analysis(df, numeric_df)


def _render_heatmap(corr_matrix):
    st.subheader("🔥 Correlation Heatmap")
    col1, col2 = st.columns([3, 1])
    with col2:
        st.markdown("**⚙️ Settings**")
        annotation = st.checkbox("Show values", value=True)
        color_scale = st.selectbox("Color scheme:", CORRELATION_COLOR_SCALES)
    with col1:
        fig = build_correlation_heatmap(corr_matrix, annotation, color_scale)
        st.plotly_chart(fig, use_container_width=True)


def _render_strong_correlations(corr_matrix):
    st.subheader("💪 Strong Correlations Discovery")
    threshold = st.slider("🎯 Correlation Strength Threshold:", 0.1, 1.0, 0.7, 0.05)
    strong_corr = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            corr_val = corr_matrix.iloc[i, j]
            if abs(corr_val) >= threshold:
                strength = "Very Strong" if abs(corr_val) >= 0.9 else "Strong" if abs(corr_val) >= 0.7 else "Moderate"
                direction = "Positive" if corr_val > 0 else "Negative"
                strong_corr.append({
                    'Variable 1': corr_matrix.columns[i],
                    'Variable 2': corr_matrix.columns[j],
                    'Correlation': round(corr_val, 3),
                    'Strength': strength,
                    'Direction': direction
                })
    if strong_corr:
        import pandas as pd
        strong_corr_df = pd.DataFrame(strong_corr).sort_values('Correlation', key=abs, ascending=False)
        st.success(f"🎉 Found {len(strong_corr)} strong correlations!")
        st.dataframe(strong_corr_df, use_container_width=True, height=300)
        strongest = strong_corr_df.iloc[0]
        st.info(
            f"🏆 **Strongest Relationship**: {strongest['Variable 1']} and {strongest['Variable 2']} "
            f"have a {strongest['Strength'].lower()} {strongest['Direction'].lower()} correlation "
            f"of {strongest['Correlation']}"
        )
    else:
        st.info(f"🔍 No correlations found above {threshold} threshold.")


def _render_pairwise_analysis(df, numeric_df):
    st.subheader("🎯 Pairwise Variable Analysis")
    col1, col2 = st.columns(2)
    with col1:
        var1 = st.selectbox("📊 Select First Variable:", numeric_df.columns)
    with col2:
        var2 = st.selectbox("📊 Select Second Variable:", [c for c in numeric_df.columns if c != var1])

    if var1 and var2:
        correlation = numeric_df[var1].corr(numeric_df[var2])
        strength_desc, strength_color = _interpret_correlation(abs(correlation))
        direction = "Positive" if correlation > 0 else "Negative"

        st.metric(
            f"🔗 Correlation between {var1} and {var2}",
            f"{correlation:.3f}",
            delta=f"{strength_color} {strength_desc} {direction}"
        )

        categorical_cols = get_categorical_columns(df)
        fig = build_scatter_with_trendline(df, var1, var2, correlation, categorical_cols)
        st.plotly_chart(fig, use_container_width=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"📊 {var1} Mean", f"{df[var1].mean():.2f}")
        with col2:
            st.metric(f"📊 {var2} Mean", f"{df[var2].mean():.2f}")
        with col3:
            st.metric("📊 R² Score", f"{correlation**2:.3f}")


def _interpret_correlation(abs_corr):
    if abs_corr >= 0.9:
        return "Very Strong", "🟢"
    elif abs_corr >= 0.7:
        return "Strong", "🟡"
    elif abs_corr >= 0.5:
        return "Moderate", "🟠"
    elif abs_corr >= 0.3:
        return "Weak", "🔴"
    return "Very Weak", "⚫"