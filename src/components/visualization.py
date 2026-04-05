"""
Data Visualization component — renders all interactive Plotly charts.
"""

import streamlit as st
import numpy as np
from src.config.constants import CHART_TYPES, COLOR_SCHEMES
from src.utils.data_helpers import get_numeric_columns, get_categorical_columns, get_datetime_columns
from src.utils.chart_helpers import (
    build_bar_chart, build_line_chart, build_scatter_chart,
    build_pie_chart, build_histogram, build_box_plot
)


def show_visualization():
    st.header("📈 Interactive Data Visualization")

    if st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first!")
        return

    df = st.session_state.data
    st.markdown("Create stunning interactive visualizations from your data")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.subheader("🎨 Chart Configuration")
        chart_type = st.selectbox("Select Visualization Type:", CHART_TYPES)

        numeric_cols = get_numeric_columns(df)
        categorical_cols = get_categorical_columns(df)
        datetime_cols = get_datetime_columns(df)

        x_col, y_col, extra = _column_selectors(df, chart_type, numeric_cols, categorical_cols, datetime_cols)

        st.subheader("⚙️ Customization")
        chart_title = st.text_input("📝 Chart Title:", value=f"{chart_type} - {x_col}")
        chart_height = st.slider("📏 Chart Height:", 300, 800, 500)
        # ✅ FIX: capture the selected value so it's actually used below
        color_scheme = st.selectbox("🎨 Color Scheme:", COLOR_SCHEMES)

    with col2:
        st.subheader(f"📊 {chart_title}")
        try:
            # ✅ FIX: pass color_scheme into _build_chart
            fig = _build_chart(df, chart_type, x_col, y_col, extra,
                               categorical_cols, datetime_cols, chart_title,
                               chart_height, color_scheme)
            if fig:
                st.plotly_chart(fig, use_container_width=True)
                if chart_type in ["📊 Bar Chart", "📈 Line Chart", "🎯 Scatter Plot"] and y_col:
                    _render_chart_stats(df, y_col)
        except Exception as e:
            st.error(f"❌ Error creating visualization: {str(e)}")


def _column_selectors(df, chart_type, numeric_cols, categorical_cols, datetime_cols):
    extra = {}
    x_col, y_col = None, None

    if chart_type in ["📊 Bar Chart", "🥧 Pie Chart"]:
        if categorical_cols:
            x_col = st.selectbox("🎯 Category Column (X-axis):", categorical_cols)
            if chart_type == "📊 Bar Chart" and numeric_cols:
                y_col = st.selectbox("📊 Value Column (Y-axis):", numeric_cols + [None])
        else:
            st.error("❌ No categorical columns found for this chart type")

    elif chart_type in ["📈 Line Chart", "🎯 Scatter Plot"]:
        if len(numeric_cols) >= 2:
            x_col = st.selectbox("➡️ X-axis Column:", numeric_cols + datetime_cols)
            y_col = st.selectbox("⬆️ Y-axis Column:", [col for col in numeric_cols if col != x_col])
            if chart_type == "🎯 Scatter Plot":
                extra['color_col'] = st.selectbox("🎨 Color by (optional):", [None] + categorical_cols)
                extra['size_col'] = st.selectbox("📏 Size by (optional):", [None] + numeric_cols)
        else:
            st.error("❌ Need at least 2 numeric columns")

    elif chart_type in ["📊 Histogram", "📦 Box Plot"]:
        if numeric_cols:
            x_col = st.selectbox("📊 Column to Analyze:", numeric_cols)
            if chart_type == "📦 Box Plot":
                extra['group_col'] = st.selectbox("🎨 Group by (optional):", [None] + categorical_cols)
        else:
            st.error("❌ No numeric columns found")

    return x_col, y_col, extra


def _build_chart(df, chart_type, x_col, y_col, extra, categorical_cols,
                 datetime_cols, title, height, color_scheme):
    # ✅ FIX: color_scheme is now received and passed to every builder
    if chart_type == "📊 Bar Chart" and x_col:
        agg_type = "sum"
        if y_col:
            agg_type = st.selectbox("Aggregation:", ["sum", "mean", "count"])
        return build_bar_chart(df, x_col, y_col, agg_type, title, height, color_scheme)

    elif chart_type == "📈 Line Chart" and x_col and y_col:
        return build_line_chart(df, x_col, y_col, title, height, color_scheme)

    elif chart_type == "🎯 Scatter Plot" and x_col and y_col:
        return build_scatter_chart(df, x_col, y_col, extra.get('color_col'),
                                   extra.get('size_col'), categorical_cols,
                                   title, height, color_scheme)

    elif chart_type == "🥧 Pie Chart" and x_col:
        return build_pie_chart(df, x_col, title, height, color_scheme)

    elif chart_type == "📊 Histogram" and x_col:
        nbins = st.slider("Number of bins:", 10, 100, 30)
        return build_histogram(df, x_col, nbins, title, height, color_scheme)

    elif chart_type == "📦 Box Plot" and x_col:
        return build_box_plot(df, x_col, extra.get('group_col'), title, height, color_scheme)

    return None


def _render_chart_stats(df, y_col):
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Mean", f"{df[y_col].mean():.2f}")
    with col2:
        st.metric("📈 Max", f"{df[y_col].max():.2f}")
    with col3:
        st.metric("📉 Min", f"{df[y_col].min():.2f}")