"""
Data Cleaning component — handles missing values, type conversion, deduplication.
"""

import streamlit as st
import pandas as pd
from src.config.constants import MISSING_VALUE_STRATEGIES, TEXT_STANDARDIZATION_OPTIONS


def show_cleaning():
    st.header("🧹 Data Cleaning & Preprocessing")

    if st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first in the Data Upload section!")
        return

    df = st.session_state.data.copy()
    st.markdown("Transform and clean your data with professional preprocessing tools")
    st.subheader("🛠️ Cleaning Operations")

    col1, col2 = st.columns(2)

    with col1:
        missing_action, fill_value = _missing_values_section(df)

    with col2:
        date_columns, numeric_columns = _type_conversion_section(df)

    remove_duplicates, standardize_text, text_operation, columns_to_drop = _additional_operations_section(df)

    if st.button("🚀 Apply All Cleaning Operations", type="primary", use_container_width=True):
        df = _apply_cleaning(
            df, missing_action, fill_value,
            date_columns, numeric_columns,
            remove_duplicates, standardize_text,
            text_operation, columns_to_drop
        )
        # ✅ FIX 1: Save cleaned df to session state BEFORE rendering summary
        st.session_state.data = df
        st.balloons()
        st.success("🎉 Data cleaning completed successfully!")

    # ✅ FIX 2: Always read from session_state so summary reflects latest cleaned data
    _render_cleaning_summary(st.session_state.data)


def _missing_values_section(df):
    st.markdown("**🔧 Missing Values Treatment**")
    missing_action = st.radio("How would you like to handle missing values?", MISSING_VALUE_STRATEGIES)
    fill_value = None
    if missing_action == "Fill with custom value":
        fill_value = st.text_input("Enter fill value:", "Unknown")
    if df.isnull().sum().sum() > 0:
        st.markdown("**Missing Values Summary:**")
        missing_summary = df.isnull().sum()
        missing_summary = missing_summary[missing_summary > 0]
        for col, count in missing_summary.items():
            st.write(f"• {col}: {count} missing ({count/len(df)*100:.1f}%)")
    else:
        st.success("✅ No missing values found!")
    return missing_action, fill_value


def _type_conversion_section(df):
    st.markdown("**🔄 Data Type Conversion**")
    date_columns = []
    numeric_columns = []
    if st.checkbox("🗓️ Convert date columns"):
        date_columns = st.multiselect(
            "Select columns to convert to datetime:",
            [col for col in df.columns if df[col].dtype == 'object']
        )
    if st.checkbox("🔢 Convert numeric columns"):
        numeric_columns = st.multiselect(
            "Select columns to convert to numeric:",
            [col for col in df.columns if df[col].dtype == 'object']
        )
    return date_columns, numeric_columns


def _additional_operations_section(df):
    st.markdown("**🔧 Additional Operations**")
    col3, col4 = st.columns(2)
    text_operation = None
    with col3:
        remove_duplicates = st.checkbox("🗑️ Remove duplicate rows")
        columns_to_drop = st.multiselect("Select columns to drop", options=list(df.columns))
        if columns_to_drop:
            st.info(f"Selected columns to drop: {', '.join(columns_to_drop)}")
        if remove_duplicates:
            dup_count = df.duplicated().sum()
            if dup_count > 0:
                st.info(f"Found {dup_count} duplicate rows")
            else:
                st.success("No duplicate rows found")
    with col4:
        standardize_text = st.checkbox("📝 Standardize text columns")
        if standardize_text:
            text_operation = st.selectbox("Text standardization:", TEXT_STANDARDIZATION_OPTIONS)
    return remove_duplicates, standardize_text, text_operation, columns_to_drop


def _apply_cleaning(df, missing_action, fill_value, date_columns, numeric_columns,
                    remove_duplicates, standardize_text, text_operation, columns_to_drop):
    original_shape = df.shape
    with st.spinner("🔄 Processing your data..."):

        if columns_to_drop:
            df = df.drop(columns=columns_to_drop)
            st.success(f"✅ Dropped {len(columns_to_drop)} columns: {', '.join(columns_to_drop)}")

        if missing_action == "Drop rows with missing values":
            df = df.dropna()
            st.success(f"✅ Removed {original_shape[0] - df.shape[0]} rows with missing values")

        elif missing_action == "Fill with mean":
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # ✅ FIX 3: Assign back instead of inplace=True (safer in pandas 2.x)
                    df[col] = df[col].fillna(df[col].mean())
            st.success("✅ Filled missing numeric values with mean")

        elif missing_action == "Fill with mode":
            for col in df.columns:
                mode_val = df[col].mode(dropna=True)
                if not mode_val.empty:
                    # ✅ FIX 3: Assign back instead of inplace=True
                    df[col] = df[col].fillna(mode_val[0])
            st.success("✅ Filled missing values with mode")

        elif missing_action == "Fill with median":
            for col in df.columns:
                if pd.api.types.is_numeric_dtype(df[col]):
                    # ✅ FIX 3: Assign back instead of inplace=True
                    df[col] = df[col].fillna(df[col].median())
            st.success("✅ Filled missing numeric values with median")

        elif missing_action == "Fill with custom value":
            df = df.fillna(fill_value)
            st.success(f"✅ Filled missing values with '{fill_value}'")

        elif missing_action == "Forward fill":
            df = df.ffill()
            st.success("✅ Applied forward fill to missing values")

        elif missing_action == "Backward fill":
            df = df.bfill()
            st.success("✅ Applied backward fill to missing values")

        for col in date_columns:
            try:
                df[col] = pd.to_datetime(df[col], errors='coerce')
                st.success(f"✅ Converted {col} to datetime format")
            except Exception as e:
                st.error(f"❌ Could not convert {col}: {str(e)}")

        for col in numeric_columns:
            try:
                df[col] = pd.to_numeric(df[col], errors='coerce')
                st.success(f"✅ Converted {col} to numeric format")
            except Exception as e:
                st.error(f"❌ Could not convert {col}: {str(e)}")

        if remove_duplicates:
            before = len(df)
            df = df.drop_duplicates()
            if before > len(df):
                st.success(f"✅ Removed {before - len(df)} duplicate rows")

        if standardize_text and text_operation:
            text_cols = df.select_dtypes(include=['object']).columns
            for col in text_cols:
                if text_operation == "lowercase":
                    df[col] = df[col].astype(str).str.lower()
                elif text_operation == "uppercase":
                    df[col] = df[col].astype(str).str.upper()
                elif text_operation == "title case":
                    df[col] = df[col].astype(str).str.title()
                elif text_operation == "trim whitespace":
                    df[col] = df[col].astype(str).str.strip()
            st.success(f"✅ Applied {text_operation} to text columns")

    return df


def _render_cleaning_summary(df):
    st.subheader("📊 Current Data Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("📋 Columns", df.shape[1])
    with col3:
        st.metric("❌ Missing Values", df.isnull().sum().sum())
    with col4:
        st.metric("🗑️ Duplicates", df.duplicated().sum())
    st.subheader("👁️ Data Preview")
    st.dataframe(df.head(10), use_container_width=True, height=300)