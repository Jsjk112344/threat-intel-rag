import React, { useState } from 'react';
import QueryInput from './components/QueryInput';
import ResponseDisplay from './components/ResponseDisplay';
import { ingestCVEs, queryThreats } from './api';
import './App.css';

function App() {
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [ingesting, setIngesting] = useState(false);
  const [error, setError] = useState(null);

  const handleIngest = async () => {
    setIngesting(true);
    setError(null);
    try {
      const result = await ingestCVEs(30, 100);
      alert(`Successfully ingested ${result.count} CVEs`);
    } catch (err) {
      setError('Failed to ingest CVEs: ' + err.message);
    } finally {
      setIngesting(false);
    }
  };

  const handleQuery = async (query) => {
    setLoading(true);
    setError(null);
    setResponse(null);
    
    try {
      const result = await queryThreats(query);
      setResponse(result);
    } catch (err) {
      setError('Failed to query: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header style={styles.header}>
        <h1>🔒 Threat Intelligence RAG</h1>
        <p>Search and analyze cybersecurity vulnerabilities</p>
        <button 
          onClick={handleIngest} 
          style={styles.ingestButton}
          disabled={ingesting}
        >
          {ingesting ? 'Ingesting...' : 'Ingest Latest CVEs'}
        </button>
      </header>

      <main style={styles.main}>
        <QueryInput onQuery={handleQuery} loading={loading} />
        
        {error && (
          <div style={styles.error}>{error}</div>
        )}
        
        {loading && (
          <div style={styles.loading}>Analyzing threats...</div>
        )}
        
        <ResponseDisplay response={response} />
      </main>
    </div>
  );
}

const styles = {
  header: {
    backgroundColor: '#282c34',
    padding: '2rem',
    color: 'white',
    textAlign: 'center',
  },
  main: {
    maxWidth: '900px',
    margin: '2rem auto',
    padding: '0 1rem',
  },
  ingestButton: {
    marginTop: '1rem',
    padding: '0.5rem 1.5rem',
    backgroundColor: '#28a745',
    color: 'white',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    fontSize: '0.9rem',
  },
  error: {
    backgroundColor: '#f8d7da',
    color: '#721c24',
    padding: '1rem',
    borderRadius: '8px',
    marginBottom: '1rem',
  },
  loading: {
    textAlign: 'center',
    padding: '2rem',
    fontSize: '1.2rem',
    color: '#666',
  },
};

export default App;