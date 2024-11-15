import openai
import os
from openai.error import APIConnectionError

def generate_resume(resume_data):
    openai.api_key = os.getenv("OPENAI_API_KEY")

    prompt = f"""
    Generate a professional, ATS-friendly resume based on the following information:

    Name: {resume_data['name']}
    Email: {resume_data['email']}
    Phone: {resume_data['phone']}
    Location: {resume_data['location']}

    Professional Summary:
    {resume_data['summary']}

    Work Experience:
    {' '.join([f'''
    Job Title: {exp['job_title']}
    Company: {exp['company']}
    Duration: {exp['start_date']} to {exp['end_date']}
    Responsibilities:
    {exp['responsibilities']}
    ''' for exp in resume_data['experiences']])}

    Education:
    Degree: {resume_data['education']['degree']}
    Institution: {resume_data['education']['institution']}
    Graduation Date: {resume_data['education']['graduation_date']}

    Skills:
    {resume_data['skills']}

    Certifications:
    {resume_data['certifications']}

    Please format the resume using the following guidelines:
    1. Use clear, concise language and strong action verbs.
    2. Organize the content into clear sections: Contact Information, Professional Summary, Work Experience, Education, Skills, and Certifications.
    3. For the Work Experience section, use bullet points to highlight key achievements and responsibilities. Focus on quantifiable results and impactful contributions.
    4. Ensure the content is ATS-friendly by using standard section headings and relevant keywords from the job industry.
    5. Limit the resume to one page if possible, prioritizing the most relevant and recent information.
    6. Tailor the professional summary and skills sections to highlight the candidate's most relevant qualifications.
    7. Use a professional tone throughout the resume.
    8. Format the resume with appropriate spacing and indentation for easy readability.

    The resume should be well-structured, easy to scan, and effectively highlight the candidate's strengths and achievements.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert resume writer with extensive knowledge of ATS systems, modern hiring practices, and industry-specific requirements."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except APIConnectionError as e:
        return f"Error connecting to OpenAI API: {str(e)}. Please check your internet connection and try again."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}. Please try again later."