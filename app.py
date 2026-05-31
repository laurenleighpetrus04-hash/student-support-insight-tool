from __future__ import annotations

from io import StringIO
from pathlib import Path

import pandas as pd ## For data manipulation and analysis
import plotly.express as px ## For interactive visualizations in the Streamlit dashboard
import streamlit as st ## For building the web app interface and handling user interactions

## Define required columns, confidence score columns, and allowed categorical values for validation
REQUIRED_COLUMNS = [
    "learner_id",
    "age_band",
    "province_area",
    "device_access",
    "internet_access",
    "digital_confidence",
    "programming_confidence",
    "ai_familiarity",
    "employment_status",
    "support_need",
    "attendance_risk",
    "notes",
]
## Mapping of support needs to descriptive notes for the synthetic dataset
CONFIDENCE_COLUMNS = [
    "digital_confidence",
    "programming_confidence",
    "ai_familiarity",
]
## --- IGNORE ---
ALLOWED_VALUES = {
    "age_band": {"18-24", "25-29", "30-35"},
    "device_access": {"Laptop", "Shared laptop", "Phone only"},
    "internet_access": {"Reliable", "Unstable", "Limited"},
    "employment_status": {"Unemployed", "Under-employed", "Employed part-time"},
    "support_need": {"Data", "Transport", "Academic support", "Mentoring"},
    "attendance_risk": {"Low", "Medium", "High"},
}

## loading function to read either the uploaded CSV file or the default synthetic dataset, with error handling for missing files
def load_data(uploaded_file) -> pd.DataFrame:
    if uploaded_file is not None:
        return pd.read_csv(uploaded_file)

    default_file = Path("data/synthetic_learners.csv")

    if not default_file.exists():
        st.error("Synthetic dataset missing. Run: python scripts/create_sample_data.py")
        st.stop()

    return pd.read_csv(default_file)

##  preprocessing and analysis functions, including validation, cleaning, risk scoring, insights generation, and report building
def validate_data(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]

    if missing_columns:
        errors.append(f"Missing required columns: {', '.join(missing_columns)}")
        return errors, warnings

    missing_values = df[REQUIRED_COLUMNS].isna().sum()
    missing_values = missing_values[missing_values > 0]

    if not missing_values.empty:
        warnings.append(f"Missing values found: {missing_values.to_dict()}")

    duplicate_ids = df[df["learner_id"].duplicated()]["learner_id"].tolist()

    if duplicate_ids:
        warnings.append(f"Duplicate learner IDs found: {duplicate_ids}")

    for column in CONFIDENCE_COLUMNS:
        numeric_values = pd.to_numeric(df[column], errors="coerce")

        invalid_rows = df[numeric_values.isna() | ~numeric_values.between(1, 5)]

        if not invalid_rows.empty:
            warnings.append(f"{column} has invalid values. Scores must be from 1 to 5.")

    for column, allowed_values in ALLOWED_VALUES.items():
        invalid_values = sorted(set(df[column].dropna().astype(str)) - allowed_values)

        if invalid_values:
            warnings.append(
                f"{column} has invalid values: {invalid_values}. "
                f"Allowed values: {sorted(allowed_values)}"
            )

    return errors, warnings

## normally this would be in a separate utils.py file, but included here for simplicity
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned = df.copy()

    for column in REQUIRED_COLUMNS:
        if cleaned[column].dtype == "object":
            cleaned[column] = cleaned[column].astype(str).str.strip()

    for column in CONFIDENCE_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned = cleaned.drop_duplicates(subset=["learner_id"], keep="first")

    return cleaned

## risk scoring function based on attendance risk, internet access, device access, and confidence scores
def calculate_risk_score(row: pd.Series) -> int:
    score = 0

    if row["attendance_risk"] == "High":
        score += 2
    elif row["attendance_risk"] == "Medium":
        score += 1

    if row["internet_access"] == "Limited":
        score += 2
    elif row["internet_access"] == "Unstable":
        score += 1

    if row["device_access"] == "Phone only":
        score += 2
    elif row["device_access"] == "Shared laptop":
        score += 1

    if row["digital_confidence"] <= 2:
        score += 1

    if row["programming_confidence"] <= 2:
        score += 1

    if row["ai_familiarity"] <= 2:
        score += 1

    return score

## Risk classification function to categorize learners into High, Medium, or Low support risk based on their risk score
def classify_support_risk(score: int) -> str:
    if score >= 6:
        return "High"

    if score >= 3:
        return "Medium"

    return "Low"

## Function to add risk score and support risk level columns to the dataset based on the defined scoring and classification logic
def add_risk_columns(df: pd.DataFrame) -> pd.DataFrame:
    analysed = df.copy()

    analysed["risk_score"] = analysed.apply(calculate_risk_score, axis=1)
    analysed["support_risk_level"] = analysed["risk_score"].apply(classify_support_risk)

    return analysed

## Functions to generate insights and recommendations based on the analysed dataset, which will be displayed in the Streamlit app
def generate_insights(df: pd.DataFrame) -> list[str]:
    total = len(df)
    high_risk = int((df["support_risk_level"] == "High").sum())
    medium_risk = int((df["support_risk_level"] == "Medium").sum())
    phone_only = int((df["device_access"] == "Phone only").sum())
    limited_internet = int((df["internet_access"] == "Limited").sum())
    top_support_need = df["support_need"].mode().iloc[0]
    avg_programming = round(float(df["programming_confidence"].mean()), 2)

    return [
        f"{high_risk} out of {total} learners are classified as high support risk.",
        f"{medium_risk} learners are classified as medium support risk.",
        f"The most common support need is {top_support_need}.",
        f"{phone_only} learners only have phone access, which may limit coding practice.",
        f"{limited_internet} learners have limited internet access.",
        f"The average programming confidence score is {avg_programming} out of 5.",
    ]

## Function to generate practical recommendations based on the insights derived from the dataset, which can be used by programme staff to plan support interventions
def generate_recommendations(df: pd.DataFrame) -> list[str]:
    recommendations: list[str] = []

    high_risk_count = int((df["support_risk_level"] == "High").sum())
    data_need_count = int((df["support_need"] == "Data").sum())
    academic_need_count = int((df["support_need"] == "Academic support").sum())
    transport_need_count = int((df["support_need"] == "Transport").sum())
    low_programming_count = int((df["programming_confidence"] <= 2).sum())

    if high_risk_count > 0:
        recommendations.append(
            "Prioritise high-risk learners for early staff check-ins during onboarding."
        )

    if data_need_count > 0:
        recommendations.append(
            "Provide data support, offline resources, or zero-rated learning materials."
        )

    if academic_need_count > 0 or low_programming_count > 0:
        recommendations.append(
            "Create a beginner programming support group for learners with low coding confidence."
        )

    if transport_need_count > 0:
        recommendations.append(
            "Review transport barriers and consider hybrid attendance options where possible."
        )

    recommendations.append(
        "Use mentors to support learners with confidence, motivation, and career planning."
    )

    return recommendations[:5]

## Function to build a comprehensive summary report combining key statistics, insights, and recommendations, which can be downloaded as a text file from the Streamlit app
def build_summary_report(
    df: pd.DataFrame,
    insights: list[str],
    recommendations: list[str],
) -> str:
    output = StringIO()

    output.write("Student Support Insights Tool Summary\n")
    output.write("====================================\n\n")

    output.write(f"Total learners analysed: {len(df)}\n")
    output.write(f"High-risk learners: {(df['support_risk_level'] == 'High').sum()}\n")
    output.write(f"Medium-risk learners: {(df['support_risk_level'] == 'Medium').sum()}\n")
    output.write(f"Low-risk learners: {(df['support_risk_level'] == 'Low').sum()}\n\n")

    output.write("Key Insights\n")
    output.write("------------\n")

    for index, insight in enumerate(insights, start=1):
        output.write(f"{index}. {insight}\n")

    output.write("\nRecommendations\n")
    output.write("---------------\n")

    for index, recommendation in enumerate(recommendations, start=1):
        output.write(f"{index}. {recommendation}\n")

    output.write("\nResponsible Use Notice\n")
    output.write("----------------------\n")
    output.write(
        "This tool supports decision-making but does not replace human judgement. "
        "Support-risk flags must be reviewed by programme staff before action is taken.\n"
    )

    return output.getvalue()

## Function to display validation results in the Streamlit app, showing errors and warnings in a user-friendly format
def show_validation(errors: list[str], warnings: list[str]) -> None:
    st.subheader("1. Data Validation")

    if not errors and not warnings:
        st.success("Validation passed. No major issues found.")
        return

    for error in errors:
        st.error(error)

    for warning in warnings:
        st.warning(warning)

## Function to display the main dashboard with key metrics, visualizations, and support need distributions based on the analysed dataset
def show_dashboard(df: pd.DataFrame) -> None:
    st.subheader("3. Dashboard")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Learners", len(df))
    col2.metric("High Risk", int((df["support_risk_level"] == "High").sum()))
    col3.metric("Medium Risk", int((df["support_risk_level"] == "Medium").sum()))
    col4.metric("Low Risk", int((df["support_risk_level"] == "Low").sum()))

    support_counts = df["support_need"].value_counts().reset_index()
    support_counts.columns = ["support_need", "count"]

    support_fig = px.bar(
        support_counts,
        x="support_need",
        y="count",
        title="Learners by Support Need",
        text_auto=True,
    )

    st.plotly_chart(support_fig, use_container_width=True)

    internet_counts = df["internet_access"].value_counts().reset_index()
    internet_counts.columns = ["internet_access", "count"]

    internet_fig = px.pie(
        internet_counts,
        names="internet_access",
        values="count",
        title="Internet Access Distribution",
    )

    st.plotly_chart(internet_fig, use_container_width=True)

    confidence_average = (
        df[CONFIDENCE_COLUMNS]
        .mean()
        .reset_index()
        .rename(columns={"index": "confidence_type", 0: "average_score"})
    )

    confidence_fig = px.bar(
        confidence_average,
        x="confidence_type",
        y="average_score",
        title="Average Confidence Scores",
        range_y=[0, 5],
        text_auto=True,
    )

    st.plotly_chart(confidence_fig, use_container_width=True)

    risk_counts = df["support_risk_level"].value_counts().reset_index()
    risk_counts.columns = ["support_risk_level", "count"]

    risk_fig = px.bar(
        risk_counts,
        x="support_risk_level",
        y="count",
        title="Support Risk Level Distribution",
        text_auto=True,
    )

    st.plotly_chart(risk_fig, use_container_width=True)

## Function to display a detailed table of learners who are classified as high or medium support risk, sorted by risk level and score, to help programme staff identify and prioritise support interventions
def show_support_table(df: pd.DataFrame) -> None:
    st.subheader("4. Learners Needing Support")

    risk_order = {"High": 0, "Medium": 1, "Low": 2}

    support_table = df.copy()
    support_table["risk_order"] = support_table["support_risk_level"].map(risk_order)

    support_table = support_table.sort_values(
        by=["risk_order", "risk_score"],
        ascending=[True, False],
    )

    support_table = support_table[
        support_table["support_risk_level"].isin(["High", "Medium"])
    ]

    st.dataframe(
        support_table[
            [
                "learner_id",
                "device_access",
                "internet_access",
                "programming_confidence",
                "support_need",
                "attendance_risk",
                "risk_score",
                "support_risk_level",
                "notes",
            ]
        ],
        use_container_width=True,
    )

## Main function to generate the synthetic learners data and save it as a CSV file
def main() -> None:
    st.set_page_config(
        page_title="Student Support Insights Tool",
        page_icon="📊",
        layout="wide",
    )

    st.title("Student Support Insights Tool")
    st.caption("MVP prototype for learner support analysis")

    st.info(
        "Privacy notice: This MVP uses synthetic or anonymised data only. "
        "Learner data should be collected with consent, used only for support planning, "
        "and reviewed by programme staff. Risk flags are not automatic decisions."
    )

    uploaded_file = st.sidebar.file_uploader("Upload learner CSV", type=["csv"])
    st.sidebar.write("No upload? The app uses the sample synthetic dataset.")

    raw_df = load_data(uploaded_file)

    errors, warnings = validate_data(raw_df)
    show_validation(errors, warnings)

    if errors:
        st.stop()

    cleaned_df = clean_data(raw_df)
    analysed_df = add_risk_columns(cleaned_df)

    st.subheader("2. Cleaned Dataset Preview")
    st.dataframe(analysed_df, use_container_width=True)

    show_dashboard(analysed_df)
    show_support_table(analysed_df)

    insights = generate_insights(analysed_df)
    recommendations = generate_recommendations(analysed_df)

    st.subheader("5. Data-Driven Insights")

    for insight in insights:
        st.write(f"- {insight}")

    st.subheader("6. Practical Recommendations")

    for recommendation in recommendations:
        st.write(f"- {recommendation}")

    summary_report = build_summary_report(
        analysed_df,
        insights,
        recommendations,
    )

    st.subheader("7. Export")

    st.download_button(
        label="Download Summary Report",
        data=summary_report,
        file_name="student_support_summary.txt",
        mime="text/plain",
    )

    st.download_button(
        label="Download Cleaned Dataset",
        data=analysed_df.to_csv(index=False),
        file_name="cleaned_student_support_data.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()