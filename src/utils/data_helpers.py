"""
Reusable data processing utilities used across components.
"""

import pandas as pd
import numpy as np


def get_numeric_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=[np.number]).columns.tolist()


def get_categorical_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=['object', 'category']).columns.tolist()


def get_datetime_columns(df: pd.DataFrame) -> list:
    return df.select_dtypes(include=['datetime64']).columns.tolist()


def compute_data_quality_score(df: pd.DataFrame) -> float:
    total_cells = df.shape[0] * df.shape[1]
    missing_cells = df.isnull().sum().sum()
    return ((total_cells - missing_cells) / total_cells * 100) if total_cells > 0 else 0.0


def get_column_summary(df: pd.DataFrame) -> pd.DataFrame:
    column_analysis = []
    for col in df.columns:
        col_info = {
            'Column': col,
            'Data Type': str(df[col].dtype),
            'Non-Null Count': df[col].count(),
            'Null Count': df[col].isnull().sum(),
            'Null %': round(df[col].isnull().sum() / len(df) * 100, 2),
            'Unique Values': df[col].nunique(),
            'Memory Usage (KB)': round(df[col].memory_usage(deep=True) / 1024, 2),
        }
        if df[col].dtype in ['int64', 'float64']:
            col_info.update({
                'Min': df[col].min(),
                'Max': df[col].max(),
                'Mean': round(df[col].mean(), 2),
                'Std': round(df[col].std(), 2),
            })
        else:
            col_info.update({
                'Most Frequent': df[col].mode().iloc[0] if not df[col].mode().empty else 'N/A',
                'Most Frequent Count': df[col].value_counts().iloc[0] if len(df[col].value_counts()) > 0 else 0,
            })
        column_analysis.append(col_info)
    return pd.DataFrame(column_analysis)