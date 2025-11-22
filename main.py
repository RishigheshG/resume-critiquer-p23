#add the OpenAI key in a separate .env file in the same folder
#to install streamlit, type "pip install streamlit"
#to run this file, type "uv run streamlit run main.py" on the terminal after going inside the folder where the main.py file is

import streamlit as st
import PyPDF2
import io
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="AI Resume Critiquer",
    page_icon="📝",
    layout="centered"
)

st.title("AI Resume Critiquer")
st.markdown("Uplaod your resume to get AI powered feedback tailored to your needs.")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("Upload your resume ⬇️", type=["pdf", "txt"])
job_role = st.text_input("Enter the job role you're targetting (optional)")

analyze = st.button("Analyze Resume") # analyze become true when the button is clicked

def extract_text_from_pdf(pdf_file):
  pdf_reader = PyPDF2.PdfReader(pdf_file)
  text = ""
  for page in pdf_reader.pages:
    text += page.extract_text() + "\n"
  return text

def extract_text_from_file(uploaded_file):
  if uploaded_file.type == "application/pdf":
    return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
  return uploaded_file.decode("utf-8")

if analyze and uploaded_file:
  try:
    file_content = extract_text_from_file(uploaded_file) 

    if not file_content.strip():
      st.error("File does not have any content.")
      st.stop()

    prompt = f"""Please analyze this resume and provide constructive feedback. 
    Focus on the following aspects:
    1. Content clarity and impact
    2. Skills presentation
    3. Experience descriptions
    4. Specific improvements for {job_role if job_role else 'general job applications'}
    
    Resume content:
    {file_content}
    
    Please provide your analysis in a clear, structured format with specific recommendations."""

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages=[
            {"role" : "system", "content": "You are an expert resume reviewer with years of experience in HR and recruitment."},
            {"role" : "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1000
    )
    st.markdown("### Analysis Results")
    st.markdown(response.choices[0].message.content) #choices[0] means its the first response that we get from gpt

  except Exception as e:
    st.error(f"An error occurred: {str(e)}")