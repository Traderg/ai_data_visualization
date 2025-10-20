from flask import Flask, request, jsonify
from flask_cors import CORS
from data_processor import load_data, process_query
from llm_service import parse_user_query
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load data once at startup
df = load_data()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy', 'rows': len(df)})

@app.route('/visualize', methods=['POST'])
def visualize():
    """Main endpoint to process natural language queries"""
    data = request.json
    user_prompt = data.get('prompt', '')
    
    if not user_prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    
    # Parse user query using LLM
    config = parse_user_query(user_prompt)
    
    if not config:
        return jsonify({'error': 'Could not parse query'}), 400
    
    # Check if this is a tweak request
    if config.get('is_tweak'):
        # Return tweak modifications
        return jsonify({
            'is_tweak': True,
            'modifications': config.get('modifications', {})
        })
    
    query_type = config.get('query_type')
    query_config = config.get('config', {})
    
    # Special handling for investor frequency
    if 'investor' in user_prompt.lower() and 'frequency' in user_prompt.lower():
        # Process investor data
        investors_list = []
        for investors in df['Top Investors'].dropna():
            investors_list.extend([inv.strip() for inv in str(investors).split(',')])
        
        investor_counts = pd.Series(investors_list).value_counts().head(10)
        
        return jsonify({
            'type': 'table',
            'data': [{'Investor': k, 'Frequency': v} for k, v in investor_counts.items()],
            'columns': ['Investor', 'Frequency'],
            'title': 'Most Frequent Investors'
        })
    
    # Process regular queries
    result = process_query(df, query_type, query_config)
    
    if not result:
        return jsonify({'error': 'Could not process query'}), 400
    
    return jsonify(result)

@app.route('/data', methods=['GET'])
def get_data():
    """Return raw dataset info"""
    return jsonify({
        'columns': df.columns.tolist(),
        'rows': len(df),
        'sample': df.head(5).to_dict('records')
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)