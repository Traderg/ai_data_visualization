import pandas as pd
import re

def parse_money(value):
    """Convert $1B, $65.4M, $3T to actual numbers"""
    if pd.isna(value) or value == '':
        return 0
    
    # Convert to string and clean up
    value = str(value).replace('$', '').replace(',', '').strip()
    
    # Remove anything in parentheses like (SALESFORCE)
    value = re.sub(r'\([^)]*\)', '', value).strip()
    
    # If empty after cleanup, return 0
    if not value:
        return 0
    
    multipliers = {'T': 1e12, 'B': 1e9, 'M': 1e6, 'K': 1e3}
    
    for suffix, multiplier in multipliers.items():
        if suffix in value.upper():
            try:
                return float(value.upper().replace(suffix, '').strip()) * multiplier
            except:
                return 0
    
    try:
        return float(value)
    except:
        return 0

def load_data():
    """Load and preprocess the SaaS companies dataset"""
    df = pd.read_csv('top_100_saas_companies_2025.csv')
    
    # Parse money columns
    df['Total Funding Numeric'] = df['Total Funding'].apply(parse_money)
    df['ARR Numeric'] = df['ARR'].apply(parse_money)
    df['Valuation Numeric'] = df['Valuation'].apply(parse_money)
    
    # Parse employees - handle both quoted and unquoted
    df['Employees Numeric'] = df['Employees'].astype(str).str.replace(',', '').str.replace('"', '').astype(float)
    
    return df

def process_query(df, query_type, config):
    """Process data based on query type and configuration"""
    
    if query_type == 'pie':
        # Group by a column and count
        column = config.get('column', 'Industry')
        data = df[column].value_counts().to_dict()
        return {
            'type': 'pie',
            'data': [{'name': k, 'value': v} for k, v in data.items()],
            'title': config.get('title', f'{column} Distribution')
        }
    
    elif query_type == 'scatter':
        # Scatter plot with two numeric columns
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        data = df[[x_col, y_col, 'Company Name']].dropna().to_dict('records')
        return {
            'type': 'scatter',
            'data': data,
            'x_label': x_col,
            'y_label': y_col,
            'title': config.get('title', f'{x_col} vs {y_col}')
        }
    
    elif query_type == 'bar':
        # Bar chart
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        chart_data = df[[x_col, y_col]].dropna().to_dict('records')
        return {
            'type': 'bar',
            'data': chart_data,
            'x_label': x_col,
            'y_label': y_col,
            'title': config.get('title', f'{y_col} by {x_col}')
        }
    
    elif query_type == 'table':
        # Table with specified columns
        columns = config.get('columns', df.columns.tolist())
        data = df[columns].head(config.get('limit', 20)).to_dict('records')
        return {
            'type': 'table',
            'data': data,
            'columns': columns,
            'title': config.get('title', 'Data Table')
        }
    
    elif query_type == 'line':
        # Line chart
        x_col = config.get('x_column')
        y_col = config.get('y_column')
        
        chart_data = df[[x_col, y_col]].dropna().sort_values(x_col).to_dict('records')
        return {
            'type': 'line',
            'data': chart_data,
            'x_label': x_col,
            'y_label': y_col,
            'title': config.get('title', f'{y_col} over {x_col}')
        }
    
    return None