import React, { useState } from 'react';
import { Database, Play, Download, CheckCircle2, AlertTriangle } from 'lucide-react';
import { claimAPI } from '../services/api';

export default function BatchProcessing() {
  const [dataset, setDataset] = useState('sample_claims.csv');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState('');

  const handleRunBatch = async () => {
    setError('');
    setLoading(true);
    setResults(null);
    try {
      const res = await claimAPI.runBatch(dataset);
      setResults(res);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Failed to execute batch run.');
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!results || !results.items) return;
    const headers = ['claim_id', 'submitted_by', 'claim_object', 'issue_type', 'object_part', 'claim_status', 'severity', 'evidence_standard_met'];
    const rows = results.items.map(item => [
      item.claim_id,
      item.submitted_by,
      item.claim_object,
      item.issue_type,
      item.object_part,
      item.claim_status,
      item.severity,
      item.evidence_standard_met
    ]);

    const csvContent = 'data:text/csv;charset=utf-8,' + [
      headers.join(','),
      ...rows.map(r => r.join(','))
    ].join('\n');

    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `batch_output_${dataset}`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Enterprise Batch Execution Runner</h1>
          <p className="page-subtitle">Run automated claim adjudication at scale across dataset repositories</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Database size={18} color="#2563eb" /> Batch Configuration
          </h2>

          {error && (
            <div style={{ padding: '0.75rem', backgroundColor: 'rgba(220, 38, 38, 0.15)', border: '1px solid #dc2626', borderRadius: '6px', color: '#fca5a5', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              {error}
            </div>
          )}

          <div className="form-group">
            <label className="form-label">Target Dataset Repository</label>
            <select
              className="form-select"
              value={dataset}
              onChange={(e) => setDataset(e.target.value)}
            >
              <option value="sample_claims.csv">dataset/sample_claims.csv (Development & Verification Sample)</option>
              <option value="claims.csv">dataset/claims.csv (Full Competition Evaluation Dataset)</option>
            </select>
          </div>

          <div style={{ backgroundColor: '#0f172a', padding: '1rem', borderRadius: '6px', border: '1px solid #334155', fontSize: '0.85rem', color: '#94a3b8', marginBottom: '1.5rem' }}>
            <strong>Operational Note:</strong> Batch execution iterates over CSV rows sequentially, running each record through <code>gemini_analyzer</code>, <code>evidence_engine</code>, <code>risk_engine</code>, and <code>decision_engine</code>.
          </div>

          <button className="btn btn-primary" style={{ width: '100%', padding: '0.75rem' }} onClick={handleRunBatch} disabled={loading}>
            {loading ? 'Processing Batch Rows...' : (
              <>
                <Play size={16} /> Execute Batch Adjudication
              </>
            )}
          </button>
        </div>

        <div>
          {loading && (
            <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
              <div style={{ fontSize: '1.15rem', fontWeight: 600, color: '#3b82f6', marginBottom: '0.5rem' }}>
                Batch Evaluation in Progress...
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                Iterating records against visual pipeline. Rate limiting applied automatically.
              </p>
            </div>
          )}

          {results && (
            <div className="card" style={{ border: '1px solid #059669' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', color: '#34d399', fontWeight: 600 }}>
                  <CheckCircle2 size={20} /> Batch Completed
                </div>
                <button className="btn btn-secondary" style={{ padding: '0.4rem 0.75rem' }} onClick={downloadCSV}>
                  <Download size={14} /> Export CSV
                </button>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                Processed <strong>{results.processed_count}</strong> claim rows from <code>{dataset}</code>.
              </div>

              <div style={{ maxHeight: '320px', overflowY: 'auto', border: '1px solid #334155', borderRadius: '6px' }}>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>Claim ID</th>
                      <th>Object</th>
                      <th>Verdict</th>
                    </tr>
                  </thead>
                  <tbody>
                    {results.items.map((item) => (
                      <tr key={item.claim_id}>
                        <td style={{ fontWeight: 600, color: '#3b82f6' }}>{item.claim_id}</td>
                        <td style={{ textTransform: 'capitalize' }}>{item.claim_object}</td>
                        <td>
                          <span className={`badge badge-${item.claim_status === 'not_enough_information' ? 'nei' : item.claim_status}`}>
                            {item.claim_status.replace(/_/g, ' ')}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
