import React, { useState } from 'react';
import axios from 'axios';
import {
  PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer,
  ScatterChart, Scatter, XAxis, YAxis, CartesianGrid,
  BarChart, Bar, LineChart, Line
} from 'recharts';
import './App.css';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8', '#82ca9d', '#ffc658', '#ff7c7c'];

function App() {
  const [prompt, setPrompt] = useState('');
  const [visualizations, setVisualizations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!prompt.trim()) return;

    setLoading(true);
    setError('');

    try {
      const response = await axios.post('http://localhost:5002/visualize', {
        prompt: prompt
      });

      // Check if this is a tweak request
      if (response.data.is_tweak) {
        if (visualizations.length === 0) {
          setError('No visualization to tweak. Create one first!');
          setLoading(false);
          return;
        }

        // Apply modifications to the last visualization
        const modifications = response.data.modifications;
        const updatedVizs = [...visualizations];
        const lastIndex = updatedVizs.length - 1;
        
        // Merge modifications into the last visualization
        updatedVizs[lastIndex] = {
          ...updatedVizs[lastIndex],
          styles: {
            ...updatedVizs[lastIndex].styles,
            ...modifications
          }
        };

        setVisualizations(updatedVizs);
        setPrompt('');
      } else {
        // Add new visualization
        setVisualizations([...visualizations, { 
          id: Date.now(), 
          ...response.data,
          styles: {} // Initialize empty styles
        }]);
        setPrompt('');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to generate visualization');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderVisualization = (viz) => {
    const chartColor = viz.styles?.color || '#8884d8';
    const fillColors = COLORS;

    switch (viz.type) {
      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <PieChart>
              <Pie
                data={viz.data}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {viz.data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={viz.styles?.color || fillColors[index % fillColors.length]} 
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <ScatterChart>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x_label} name={viz.x_label} />
              <YAxis dataKey={viz.y_label} name={viz.y_label} />
              <Tooltip cursor={{ strokeDasharray: '3 3' }} />
              <Legend />
              <Scatter name={viz.title} data={viz.data} fill={chartColor} />
            </ScatterChart>
          </ResponsiveContainer>
        );

      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={viz.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x_label} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={viz.y_label} fill={chartColor} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={400}>
            <LineChart data={viz.data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={viz.x_label} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey={viz.y_label} stroke={chartColor} />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'table':
        const headerStyle = {
          fontWeight: viz.styles?.bold ? 'bold' : '600',
          fontSize: viz.styles?.fontSize || 'inherit'
        };

        return (
          <div style={{ overflowX: 'auto', maxHeight: '400px' }}>
            <table className="data-table">
              <thead>
                <tr>
                  {viz.columns.map((col) => (
                    <th key={col} style={headerStyle}>{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {viz.data.map((row, idx) => (
                  <tr key={idx}>
                    {viz.columns.map((col) => (
                      <td key={col}>{row[col]}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );

      default:
        return <p>Unsupported visualization type</p>;
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SaaS Data Visualizer</h1>
        <p>Ask questions about the top 100 SaaS companies</p>
      </header>

      <div className="container">
        <form onSubmit={handleSubmit} className="prompt-form">
          <input
            type="text"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g., Create a pie chart representing industry breakdown"
            className="prompt-input"
            disabled={loading}
          />
          <button type="submit" disabled={loading} className="submit-btn">
            {loading ? 'Generating...' : 'Visualize'}
          </button>
        </form>

        {error && <div className="error">{error}</div>}

        <div className="visualizations">
          {visualizations.map((viz) => (
            <div key={viz.id} className="viz-card">
              <h3>{viz.title}</h3>
              {renderVisualization(viz)}
              <button 
                onClick={() => setVisualizations(visualizations.filter(v => v.id !== viz.id))}
                className="remove-btn"
              >
                Remove
              </button>
            </div>
          ))}
        </div>

        {visualizations.length === 0 && !loading && (
          <div className="empty-state">
            <p>No visualizations yet. Try asking:</p>
            <ul>
              <li>"Create a pie chart representing industry breakdown"</li>
              <li>"Create a scatter plot of founded year and valuation"</li>
              <li>"Show me which investors appear most frequently"</li>
            </ul>
            <p style={{marginTop: '1rem', fontStyle: 'italic', color: '#888'}}>
              After creating a chart, you can tweak it with prompts like:<br/>
              "Change the color to light blue" or "Make the header row bold"
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;