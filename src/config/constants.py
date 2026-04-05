"""
App-wide constants: chart types, color schemes, aggregation options.
"""

CHART_TYPES = [
    "📊 Bar Chart",
    "📈 Line Chart",
    "🎯 Scatter Plot",
    "🥧 Pie Chart",
    "📊 Histogram",
    "📦 Box Plot",
]

COLOR_SCHEMES = [
    "plotly", "viridis", "plasma", "inferno", "cividis"
]

# ✅ Removed "coolwarm" and "seismic" — both break px.imshow in current Plotly versions
CORRELATION_COLOR_SCALES = [
    "RdBu_r", "viridis", "plasma", "inferno",
]

MISSING_VALUE_STRATEGIES = [
    "Keep as is",
    "Drop rows with missing values",
    "Fill with mean",
    "Fill with mode",
    "Fill with median",
    "Fill with custom value",
    "Forward fill",
    "Backward fill",
]

TEXT_STANDARDIZATION_OPTIONS = [
    "lowercase", "uppercase", "title case", "trim whitespace"
]