import streamlit as st
import os
from dotenv import load_dotenv
from resume_generator import generate_resume
from utils import apply_custom_css, create_download_link
from datetime import datetime
from streamlit_option_menu import option_menu

# Set page config as the first Streamlit command
st.set_page_config(page_title="Professional Resume Generator", page_icon="📄", layout="wide")

# Load environment variables
load_dotenv()

# Apply custom CSS
apply_custom_css()

# Sidebar
with st.sidebar:
    selected = option_menu(
        menu_title="Navigation",
        options=["Home", "Generate Resume", "About"],
        icons=["house", "file-earmark-text", "info-circle"],
        menu_icon="cast",
        default_index=0,
    )

if selected == "Home":
    st.title("🏠 Welcome to the Professional Resume Generator")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: #2c3e50;'>Create Your ATS-Friendly Resume in Minutes!</h3>
        <p style='color: #34495e;'>Our AI-powered resume generator helps you craft a professional, ATS-optimized resume tailored to your unique experiences and skills.</p>
        <ul style='color: #34495e;'>
            <li>Easy-to-use interface</li>
            <li>ATS-friendly formatting</li>
            <li>Professional content generation</li>
            <li>Downloadable in PDF and DOCX formats</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

elif selected == "Generate Resume":
    st.title("📄 Professional Resume Generator")

    # Personal Information
    st.header("📌 Personal Information")
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Full Name", key="name")
        email = st.text_input("Email", key="email")
    with col2:
        phone = st.text_input("Phone", key="phone")
        location = st.text_input("Location", key="location")

    # Professional Summary
    st.header("💼 Professional Summary")
    summary = st.text_area("Brief professional summary", key="summary", height=100)

    # Work Experience
    st.header("👔 Work Experience")
    num_experiences = st.number_input("Number of work experiences", min_value=1, max_value=5, value=1, step=1)

    experiences = []
    for i in range(num_experiences):
        st.subheader(f"Experience {i+1}")
        col1, col2 = st.columns(2)
        with col1:
            job_title = st.text_input("Job Title", key=f"job_title_{i}")
            company = st.text_input("Company", key=f"company_{i}")
        with col2:
            start_date = st.date_input("Start Date", key=f"start_date_{i}", min_value=datetime(1950, 1, 1), max_value=datetime.now())
            end_date = st.date_input("End Date", key=f"end_date_{i}", min_value=datetime(1950, 1, 1), max_value=datetime.now())
        responsibilities = st.text_area("Responsibilities", key=f"responsibilities_{i}", height=100)
        experiences.append({
            "job_title": job_title,
            "company": company,
            "start_date": start_date,
            "end_date": end_date,
            "responsibilities": responsibilities
        })

    # Education
    st.header("🎓 Education")
    col1, col2 = st.columns(2)
    with col1:
        degree = st.text_input("Degree", key="degree")
        institution = st.text_input("Institution", key="institution")
    with col2:
        graduation_date = st.date_input("Graduation Date", key="graduation_date", min_value=datetime(1950, 1, 1), max_value=datetime.now())

    # Skills
    st.header("🛠️ Skills")
    skills = st.text_area("List your skills (comma-separated)", key="skills", height=100)

    # Certifications
    st.header("🏆 Certifications")
    certifications = st.text_area("List your certifications (one per line)", key="certifications", height=100)

    if st.button("Generate Resume", key="generate"):
        if name and email and summary and experiences and degree and skills:
            resume_data = {
                "name": name,
                "email": email,
                "phone": phone,
                "location": location,
                "summary": summary,
                "experiences": experiences,
                "education": {
                    "degree": degree,
                    "institution": institution,
                    "graduation_date": graduation_date
                },
                "skills": skills,
                "certifications": certifications
            }
            
            generated_resume = generate_resume(resume_data)
            
            st.success("Resume generated successfully!")
            st.markdown("### Generated Resume")
            st.markdown(generated_resume, unsafe_allow_html=True)
            
            # Create download links
            pdf_link = create_download_link(generated_resume, "PDF")
            docx_link = create_download_link(generated_resume, "DOCX")
            
            st.markdown("### Download Options")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(pdf_link, unsafe_allow_html=True)
            with col2:
                st.markdown(docx_link, unsafe_allow_html=True)
        else:
            st.error("Please fill in all required fields.")

elif selected == "About":
    st.title("ℹ️ About the Professional Resume Generator")
    st.markdown("""
    <div style='background-color: #f0f2f6; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);'>
        <h3 style='color: #2c3e50;'>Our Mission</h3>
        <p style='color: #34495e;'>We aim to simplify the resume creation process by leveraging AI technology to generate professional, ATS-friendly resumes tailored to each individual's unique experiences and skills.</p>
        <h3 style='color: #2c3e50;'>How It Works</h3>
        <ol style='color: #34495e;'>
            <li>Input your personal information, work experience, education, skills, and certifications.</li>
            <li>Our AI-powered system processes your information to create a professional resume.</li>
            <li>Review and download your generated resume in PDF or DOCX format.</li>
            <li>Use your new resume to apply for jobs with confidence!</li>
        </ol>
        <h3 style='color: #2c3e50;'>Privacy & Security</h3>
        <p style='color: #34495e;'>We take your privacy seriously. All information you provide is used solely for generating your resume and is not stored or shared with any third parties.</p>
    </div>
    """, unsafe_allow_html=True)

# Add a footer
st.markdown("""
<div style='position: fixed; bottom: 0; width: 100%; text-align: center; padding: 10px; background-color: #f0f2f6;'>
    <p style='color: #34495e;'>Created with ❤️ by Shivaji P | © 2024 Professional Resume Generator</p>
</div>
""", unsafe_allow_html=True)