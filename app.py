import streamlit as st
import pandas as pd
from data_cleaner import clean_data
from plot_generator import generate_plot
from insight_generator import init_gemini, generate_insight
import matplotlib.pyplot as plt

st.set_page_config(page_title="AutoVizAI", layout="wide")
st.title("📊 VizAI - Smart Analyzer with AI")

uploaded_file = st.file_uploader("📂 Upload your Excel/CSV file", type=["csv", "xlsx"])

if uploaded_file:
    file_ext = uploaded_file.name.split('.')[-1]

    try:
        # Load file
        if file_ext == 'csv':
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        # Raw Preview
        st.subheader("🔍 Raw Data Preview")
        st.write(df.head())

        # Cleaning
        st.subheader("🧼 Cleaning Data")
        cleaned_df = clean_data(df)
        st.success("✅ Data cleaned successfully!")

        # Plotting Section
        st.subheader("📊 Plot Your Data")

        chart_types = [
            "scatterplot", "lineplot", "barplot", "countplot", "boxplot", "violinplot",
            "stripplot", "swarmplot", "histplot", "kdeplot",
            "pairplot", "heatmap", "clustermap", "jointplot", "rugplot"
        ]

        chart_type = st.selectbox("Choose a chart type", chart_types)

        # Axis input logic
        x_axis = st.selectbox("X-axis", cleaned_df.columns) if chart_type not in ["pairplot", "clustermap", "heatmap"] else None
        y_axis = st.selectbox("Y-axis", cleaned_df.columns) if chart_type in [
            "scatterplot", "lineplot", "barplot", "boxplot", "violinplot",
            "stripplot", "swarmplot", "jointplot"
        ] else None

        if st.button("📈 Generate Plot"):
            # Generate plot
            plot = generate_plot(cleaned_df, chart_type, x_axis, y_axis)

            if plot:
                # Show plot
                if chart_type in ["pairplot", "clustermap", "jointplot"]:
                    fig = plot.figure if hasattr(plot, "figure") else plot
                    st.pyplot(fig)
                else:
                    fig = plot
                    st.pyplot(fig)

                # AI Insight Generation
                try:
                    model = init_gemini()
                    insight = generate_insight(model, cleaned_df, chart_type, x_axis, y_axis, fig=fig)

                    st.subheader("🧠 AI Insight")
                    st.success("✅ Insight Generated:")
                    st.markdown(insight)

                except Exception as e:
                    st.error(f"❌ Failed to generate insight: {e}")
            else:
                st.warning("⚠️ Could not generate the plot. Please check your column selection.")

    except Exception as e:
        st.error(f"❌ Failed to process the file: {e}")

else:
    st.info("📥 Upload an Excel or CSV file to get started.")
