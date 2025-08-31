import csv
import openai
import os
from dotenv import load_dotenv
from prompts import FDI_RANKING_PROMPT


def read_csv(file_path):
    with open(file_path, newline='', encoding='utf-8-sig') as file:
        return list(csv.DictReader(file))


def get_company_analysis(row_data):
    # Try multiple ways to get the API key
    api_key = None
    
    # Method 1: Try to load from .env file in the same directory as this script
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        env_path = os.path.join(script_dir, '.env')
        if os.path.exists(env_path):
            load_dotenv(env_path)
            api_key = os.getenv('OPENAI_API_KEY')
    except Exception as e:
        print(f"⚠️ Warning: Could not load .env file: {e}")
    
    # Method 2: Try to get from system environment variables
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    # Method 3: Fallback to hardcoded key (not recommended for production)
    if not api_key:
        print("⚠️ Warning: No API key found. Please set OPENAI_API_KEY environment variable or check your .env file.")
        raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY environment variable or check your .env file.")
    
    if not api_key:
        raise ValueError("No OpenAI API key found. Please set OPENAI_API_KEY environment variable or check your .env file.")
    
    prompt = FDI_RANKING_PROMPT.format(
        firm_name=row_data.get('Firm name', ''),
        company_website=row_data.get('Company Website', ''),
        linkedin_url=row_data.get('LinkedIn URL', ''),
        boothnr=row_data.get('Booth nr', ''),
        country=row_data.get('Country', ''),
        hq_city=row_data.get('HQ City', ''),
        primary_sector=row_data.get('Primary Industry Sector', ''),
        vertical=row_data.get('Vertical', ''),
        all_industries=row_data.get('All Industries', ''),
        employee_count=row_data.get('Employees', ''),
        year_founded=row_data.get('Year Founded', ''),
        keywords=row_data.get('Keywords', ''),
        revenue=row_data.get('Revenue', ''),
        gross_profit=row_data.get('Gross Profit', ''),
        net_income=row_data.get('Net Income', ''),
        ownership_status=row_data.get('Ownership Status', ''),
        financing_status=row_data.get('Company Financing Status', ''),
        active_investors=row_data.get('Active Investors', ''),
        summary=row_data.get('Company Summary', '')
    )

    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")
    
    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful AI FDI analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ OpenAI API error for {row_data.get('Firm name', '')}: {e}")
        return "API_ERROR"
