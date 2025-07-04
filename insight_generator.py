import streamlit as st
import google.generativeai as genai
import io
from PIL import Image

# 🔧 Convert matplotlib figure to PIL Image
def fig_to_image(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    image = Image.open(buf)
    return image

# 🔑 Load Gemini model
def init_gemini():
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("models/gemini-1.5-flash-latest")

# 🤖 Generate AI insight
def generate_insight(model, df, chart_type, x_col="", y_col="", fig=None):
    prompt = f"""
You are a data analyst. A user has plotted a {chart_type}.
The selected columns were:
X-axis: {x_col or 'Not used'}
Y-axis: {y_col or 'Not used'}

Based on the image of the plot, provide 3–5 insights in bullet points.
Focus on trends, clusters, outliers, and correlations.
"""

    if fig:
        image = fig_to_image(fig)
        response = model.generate_content([image, prompt])
    else:
        response = model.generate_content(prompt)

    return response.text
