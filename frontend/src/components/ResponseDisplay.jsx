import React from 'react';

function ResponseDisplay({ response }) {
  if (!response) return null;

  return (
    <div style={styles.container}>
      <div style={styles.answer}>
        <h3>Analysis</h3>
        <p style={styles.answerText}>{response.answer}</p>
      </div>
      
      {response.sources && response.sources.length > 0 && (
        <div style={styles.sources}>
          <h4>Sources</h4>
          <div style={styles.sourcesList}>
            {response.sources.map((source, index) => (
              <div key={index} style={styles.source}>
                <strong>{source.cve_id}</strong>
                <span style={getSeverityStyle(source.severity)}>
                  {source.severity}
                </span>
                <span>CVSS: {source.cvss_score}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

const getSeverityStyle = (severity) => ({
  ...styles.severity,
  backgroundColor: 
    severity === 'CRITICAL' ? '#dc3545' :
    severity === 'HIGH' ? '#fd7e14' :
    severity === 'MEDIUM' ? '#ffc107' :
    '#28a745',
  color: 'white',
});

const styles = {
  container: {
    backgroundColor: '#f8f9fa',
    borderRadius: '12px',
    padding: '1.5rem',
    marginTop: '1rem',
  },
  answer: {
    marginBottom: '1.5rem',
  },
  answerText: {
    lineHeight: '1.6',
    color: '#333',
  },
  sources: {
    borderTop: '2px solid #dee2e6',
    paddingTop: '1rem',
  },
  sourcesList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.75rem',
    marginTop: '0.75rem',
  },
  source: {
    display: 'flex',
    gap: '1rem',
    alignItems: 'center',
    padding: '0.75rem',
    backgroundColor: 'white',
    borderRadius: '8px',
    border: '1px solid #dee2e6',
  },
  severity: {
    padding: '0.25rem 0.75rem',
    borderRadius: '4px',
    fontSize: '0.875rem',
    fontWeight: 'bold',
  },
};

export default ResponseDisplay;