import openai
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Set API key the old way
openai.api_key = os.getenv('OPENAI_API_KEY')

# Debug: Print if API key is loaded
if not openai.api_key:
    print("WARNING: OPENAI_API_KEY not found!")
else:
    print(f"OpenAI API Key loaded: {openai.api_key[:20]}...")

SYSTEM_PROMPT = """You are a data visualization assistant. Given a user's natural language request and dataset information, generate a JSON configuration for creating visualizations.

Available columns in the dataset:
- Company Name (string)
- Founded Year (integer)
- HQ (string)
- Industry (string)
- Total Funding (string, parsed as Total Funding Numeric)
- ARR (string, parsed as ARR Numeric)
- Valuation (string, parsed as Valuation Numeric)
- Employees (string, parsed as Employees Numeric)
- Top Investors (string, comma-separated)
- Product (string, comma-separated)
- G2 Rating (float)

Supported visualization types:
- pie: For categorical distributions (uses 'column' field)
- scatter: For two numeric variables (uses 'x_column' and 'y_column')
- bar: For comparing values across categories
- line: For trends over time
- table: For raw data display (uses 'columns' list)

Return ONLY valid JSON in this exact format:
{
  "query_type": "pie|scatter|bar|line|table",
  "config": {
    "column": "column_name",
    "x_column": "column_name",
    "y_column": "column_name",
    "columns": ["col1", "col2"],
    "title": "Chart Title",
    "color": "#hexcode",
    "limit": 20
  }
}

For investor frequency analysis, use table type with columns focusing on Top Investors.
For correlation analysis (ARR vs Valuation), use scatter plot with ARR Numeric and Valuation Numeric.
"""

def parse_user_query(user_prompt):
    """Use OpenAI to parse user query into visualization config"""
    
    print(f"=== Parsing query: {user_prompt}")
    
    try:
        print(f"=== Calling OpenAI API...")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        result = response.choices[0].message.content.strip()
        print(f"=== GPT Response: {result}")
        
        # Clean up response if it has markdown code blocks
        if result.startswith('```'):
            result = result.split('```')[1]
            if result.startswith('json'):
                result = result[4:]
            result = result.strip()
        
        config = json.loads(result)
        print(f"=== Parsed config successfully: {config}")
        return config
        
    except json.JSONDecodeError as e:
        print(f"=== JSON Parse Error: {e}")
        print(f"=== Response was: {result}")
        return None
    except Exception as e:
        print(f"=== OpenAI API Error: {e}")
        import traceback
        traceback.print_exc()
        return None