import io
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from modules.data_profiler import profile_dataframe
from modules.data_cleaner import clean_dataframe
from modules.analysis_engine import generate_insights, numeric_summary
from modules.report_generator import make_pdf_report
from modules.ui_style import apply_style, brand_sidebar, hero, feature_cards, style_fig, show_df, PALETTE

st.set_page_config(page_title="SmartData Cleaner & Analyzer", page_icon="📊", layout="wide")
apply_style()
px.defaults.color_discrete_sequence = PALETTE


def show_chart(fig):
    st.plotly_chart(style_fig(fig))


with st.sidebar:
    brand_sidebar()
    st.divider()
    st.subheader("⚙️ Cleaning options")
    st.caption("Cleaning is previewed before you download the result.")
    remove_duplicates = st.checkbox("Remove exact duplicate rows", value=True)
    trim_text = st.checkbox("Trim extra spaces in text", value=True)
    normalize_missing = st.checkbox("Convert blank strings to missing values", value=True)

hero(
    "SmartData Cleaner &amp; Analyzer",
    "Upload a CSV or Excel file. Profile, clean, analyze and export your data in seconds.",
    ["CSV / Excel", "Data profiling", "Smart cleaning", "Interactive charts", "PDF &amp; Excel reports"],
)

uploaded = st.file_uploader("Upload a CSV or Excel file", type=["csv", "xlsx", "xls"])
if uploaded:
    try:
        if uploaded.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
    except Exception as exc:
        st.error(f"Could not read this file: {exc}")
        st.stop()

    if df.empty:
        st.warning("The uploaded file has no rows.")
        st.stop()

    st.success(f"Loaded {uploaded.name}")
    profile = profile_dataframe(df)
    cleaned, log = clean_dataframe(
        df, remove_duplicates=remove_duplicates,
        trim_text=trim_text, normalize_missing=normalize_missing
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Rows", f"{len(df):,}")
    c2.metric("Columns", f"{len(df.columns):,}")
    c3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    c4.metric("Exact duplicate rows", f"{int(df.duplicated().sum()):,}")
    st.write("")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["👀 Preview", "🩺 Data quality", "🧹 Clean data", "📈 Analysis & charts", "📥 Export"]
    )
    with tab1:
        st.subheader("Original data preview")
        show_df(df.head(100))
        st.subheader("Detected column types")
        show_df(profile[["column", "inferred_type", "missing_count", "missing_percent", "unique_count"]])
    with tab2:
        st.subheader("Data quality profile")
        show_df(profile)
        missing = df.isna().sum().sort_values(ascending=False)
        missing = missing[missing > 0]
        if not missing.empty:
            fig = px.bar(x=missing.index, y=missing.values, labels={"x": "Column", "y": "Missing cells"},
                         title="Missing values by column")
            show_chart(fig)
        else:
            st.info("No missing values detected.")
        st.subheader("Numeric summary")
        if not df.select_dtypes(include=np.number).empty:
            show_df(df.describe().T)
        else:
            st.info("No numeric columns detected.")
    with tab3:
        st.subheader("Cleaning preview")
        show_df(pd.DataFrame(log))
        st.metric("Rows after selected cleaning", f"{len(cleaned):,}",
                  delta=f"{len(cleaned) - len(df):,} rows", delta_color="off")
        show_df(cleaned.head(100))
        st.caption("This starter version does not automatically fill missing values or delete statistical outliers. Review them first to avoid changing valid business data.")
    with tab4:
        st.subheader("Automatic insights")
        with st.container(border=True):
            st.markdown("\n".join(f"- {item}" for item in generate_insights(cleaned)))
        numeric = cleaned.select_dtypes(include=np.number)
        if not numeric.empty:
            st.subheader("Numeric distributions")
            col = st.selectbox("Choose a numeric column", list(numeric.columns))
            show_chart(px.histogram(numeric, x=col, title=f"Distribution of {col}"))
            if len(numeric.columns) >= 2:
                st.subheader("Relationship between numeric columns")
                xcol = st.selectbox("X axis", list(numeric.columns), key="x")
                ycol = st.selectbox("Y axis", list(numeric.columns), index=1, key="y")
                show_chart(px.scatter(numeric, x=xcol, y=ycol, title=f"{ycol} vs {xcol}"))
        categorical = cleaned.select_dtypes(include=["object", "category"])
        if not categorical.empty:
            st.subheader("Category frequency")
            cat = st.selectbox("Choose a category column", list(categorical.columns))
            counts = categorical[cat].fillna("(Missing)").astype(str).value_counts().head(15).reset_index()
            counts.columns = [cat, "Count"]
            show_chart(px.bar(counts, x=cat, y="Count", title=f"Top values in {cat}"))
        st.subheader("Numeric summary")
        show_df(numeric_summary(cleaned))
    with tab5:
        st.subheader("Download results")
        csv_bytes = cleaned.to_csv(index=False).encode("utf-8-sig")
        xlsx_buffer = io.BytesIO()
        with pd.ExcelWriter(xlsx_buffer, engine="openpyxl") as writer:
            cleaned.to_excel(writer, index=False, sheet_name="Cleaned_Data")
            profile.to_excel(writer, index=False, sheet_name="Data_Profile")
            pd.DataFrame(log).to_excel(writer, index=False, sheet_name="Cleaning_Log")
        pdf = make_pdf_report(uploaded.name, df, cleaned, log, profile)
        d1, d2, d3 = st.columns(3)
        d1.download_button("⬇️ Cleaned CSV", csv_bytes,
                           file_name="cleaned_" + uploaded.name.rsplit(".", 1)[0] + ".csv",
                           mime="text/csv")
        d2.download_button("⬇️ Excel report", xlsx_buffer.getvalue(),
                           file_name="smartdata_report.xlsx",
                           mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        d3.download_button("⬇️ PDF summary", pdf, file_name="smartdata_summary.pdf",
                           mime="application/pdf")
else:
    feature_cards([
        ("🩺", "Profile", "Column types, missing values, unique counts and duplicates at a glance."),
        ("🧹", "Clean", "Trim spaces, fix blanks and remove duplicates, with a full cleaning log."),
        ("📈", "Analyze", "Automatic insights plus interactive histograms, scatter plots and category charts."),
        ("📥", "Export", "Download a cleaned CSV, a multi-sheet Excel report and a PDF summary."),
    ])
    st.info("Start by uploading a CSV or Excel file above. Try Netflix titles, retail sales, employee records or student performance data.")
    st.caption("Insights are generic and descriptive. Domain-specific business KPIs need appropriate columns and should be validated before making decisions.")
