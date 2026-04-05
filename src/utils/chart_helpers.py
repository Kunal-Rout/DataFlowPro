"""
Reusable Plotly chart builder utilities.
"""

import plotly.express as px
import pandas as pd


def _discrete_colors(color_scheme: str) -> list:
    """Map a color scheme name to a Plotly qualitative color sequence."""
    mapping = {
        "plotly":  px.colors.qualitative.Plotly,
        "viridis": px.colors.sequential.Viridis,
        "plasma":  px.colors.sequential.Plasma,
        "inferno": px.colors.sequential.Inferno,
        "cividis": px.colors.sequential.Cividis,
    }
    return mapping.get(color_scheme, px.colors.qualitative.Plotly)


def build_bar_chart(df, x_col, y_col=None, agg_type="sum",
                    title="Bar Chart", height=500, color_scheme="plotly"):
    if y_col:
        grouped_data = df.groupby(x_col)[y_col].agg(['sum', 'mean', 'count']).reset_index()
        # ✅ FIX: after groupby, the column is named "sum"/"mean"/"count" not y_col
        # so the y-axis label was showing "sum" / "mean" / "count" instead of e.g. "Salary (sum)"
        y_label = f"{y_col} ({agg_type})"
        fig = px.bar(
            grouped_data, x=x_col, y=agg_type, title=title,
            labels={agg_type: y_label, x_col: x_col},
            color_discrete_sequence=_discrete_colors(color_scheme)
        )
    else:
        value_counts = df[x_col].value_counts()
        fig = px.bar(
            x=value_counts.index, y=value_counts.values, title=title,
            labels={'x': x_col, 'y': 'Count'},
            color_discrete_sequence=_discrete_colors(color_scheme)
        )
    fig.update_layout(height=height, template='plotly_white')
    return fig


def build_line_chart(df, x_col, y_col, title="Line Chart",
                     height=500, color_scheme="plotly"):
    df_sorted = df.sort_values(x_col)
    fig = px.line(df_sorted, x=x_col, y=y_col, title=title, markers=True,
                  color_discrete_sequence=_discrete_colors(color_scheme))
    fig.update_layout(height=height, template='plotly_white')
    return fig


def build_scatter_chart(df, x_col, y_col, color_col=None, size_col=None,
                        categorical_cols=None, title="Scatter Plot",
                        height=500, color_scheme="plotly"):
    fig = px.scatter(
        df, x=x_col, y=y_col,
        color=color_col,
        size=size_col,
        title=title,
        hover_data=categorical_cols[:3] if categorical_cols else None,
        color_discrete_sequence=_discrete_colors(color_scheme)
    )
    fig.update_layout(height=height, template='plotly_white')
    return fig


def build_pie_chart(df, x_col, title="Pie Chart",
                    height=500, color_scheme="plotly"):
    value_counts = df[x_col].value_counts().head(10)
    fig = px.pie(values=value_counts.values, names=value_counts.index,
                 title=title,
                 color_discrete_sequence=_discrete_colors(color_scheme))
    fig.update_layout(height=height)
    return fig


def build_histogram(df, x_col, nbins=30, title="Histogram",
                    height=500, color_scheme="plotly"):
    single_color = _discrete_colors(color_scheme)[0]
    fig = px.histogram(df, x=x_col, title=title, nbins=nbins,
                       color_discrete_sequence=[single_color])
    fig.update_layout(height=height, template='plotly_white')
    return fig


def build_box_plot(df, x_col, group_col=None, title="Box Plot",
                   height=500, color_scheme="plotly"):
    fig = px.box(df, y=x_col, x=group_col, title=title, color=group_col,
                 color_discrete_sequence=_discrete_colors(color_scheme))
    fig.update_layout(height=height, template='plotly_white')
    return fig


def build_correlation_heatmap(corr_matrix, annotation=True,
                               color_scale="RdBu_r", height=500):
    fig = px.imshow(
        corr_matrix,
        text_auto=annotation,
        aspect="auto",
        title="Correlation Matrix - Discover Data Relationships",
        color_continuous_scale=color_scale,
        zmin=-1, zmax=1
    )
    fig.update_layout(height=height, title_font_size=16)
    return fig


def build_scatter_with_trendline(df, var1, var2, correlation, categorical_cols=None):
    fig = px.scatter(
        df, x=var1, y=var2,
        title=f"{var1} vs {var2} (Correlation: {correlation:.3f})",
        trendline="ols",
        hover_data=categorical_cols[:2] if categorical_cols else None
    )
    fig.update_layout(height=400, template='plotly_white')
    return fig