# SaaS Data Visualizer

A full-stack application that generates data visualizations from natural language prompts using AI.

## Features

- Natural language to visualization conversion
- Multiple chart types: Pie, Scatter, Bar, Line, Table
- Support for multiple simultaneous visualizations
- Interactive chart tweaking through prompts
- Docker containerized setup

## Tech Stack

- **Frontend**: React, Recharts, Axios
- **Backend**: Python, Flask, Pandas, OpenAI API
- **Infrastructure**: Docker, Docker Compose

## Prerequisites

- Docker and Docker Compose installed
- OpenAI API key

## Setup Instructions

### 1. Clone or extract the project

### 2. Add OpenAI API Key

Create a `.env` file in the root directory:
```bash
echo "OPENAI_API_KEY=your_actual_api_key_here" > .env
```

### 3. Ensure the CSV file is in the backend folder
```bash
cp top_100_saas_companies_2025.csv backend/
```

### 4. Build and run with Docker Compose
```bash
docker-compose up --build
```

This will:
- Build both frontend and backend containers
- Start the backend on `http://localhost:5001`
- Start the frontend on `http://localhost:3000`

### 5. Access the application

Open your browser and navigate to `http://localhost:3000`

## Usage Examples

Try these prompts:

1. **Easy**: "Create a pie chart representing industry breakdown"
2. **Medium**: "Create a scatter plot of founded year and valuation"
3. **Hard**: "Show me which investors appear most frequently"
4. **Extreme**: "Give me the best representation of data if I want to understand the correlation of ARR and Valuation"

## Stopping the Application
```bash
docker-compose down
```

## Development

To run without Docker:

**Backend**:
```bash
cd backend
pip install -r requirements.txt
python app.py
```

**Frontend**:
```bash
cd frontend
npm install
npm start
```

## API Endpoints

- `POST /visualize` - Generate visualization from natural language prompt
- `GET /health` - Health check endpoint
- `GET /data` - Get dataset information

## Project Structure
```
project-root/
├── docker-compose.yml
├── .env
├── README.md
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── data_processor.py
│   ├── llm_service.py
│   └── top_100_saas_companies_2025.csv
└── frontend/
    ├── Dockerfile
    ├── package.json
    ├── public/
    │   └── index.html
    └── src/
        ├── App.js
        ├── App.css
        ├── index.js
        └── index.css
```

## Notes

- The application uses GPT-4 for natural language processing
- Visualizations are rendered client-side using Recharts
- Data processing happens server-side with Pandas