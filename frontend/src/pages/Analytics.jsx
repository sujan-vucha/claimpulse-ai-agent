import React, { useState, useEffect } from 'react';
import { BarChart3, TrendingUp, Clock, AlertCircle, CheckCircle, HelpCircle, RefreshCw } from 'lucide-react';
import { claimAPI } from '../services/api';

export default function Analytics() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchAnalytics = async () => {
    setLoading(true);
    try {
      const res = await claimAPI.getAnalytics();
      setData(res);
    } catch (err) {
      console.error('Failed to load analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAnalytics();
  }, []);

  if (loading) {
    return <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>Loading enterprise platform metrics...</div>;
  }

  const stats = data || {
    total_claims: 0,
    supported: 0,
    contradicted: 0,
    not_enough_information: 0,
    approval_rate_pct: 0,
    avg_processing_sec: 0,
    high_risk_count: 0
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Platform Performance & Adjudication Analytics</h1>
          <p className="page-subtitle">Real-time enterprise metrics aggregated from our AI adjudication engines</p>
        </div>
        <button className="btn btn-secondary" onClick={fetchAnalytics}>
          <RefreshCw size={16} /> Refresh Metrics
        </button>
      </div>

      <div className="grid-4" style={{ marginBottom: '2rem' }}>
        <div className="metric-card">
          <div className="metric-label">Total Processed Claims</div>
          <div className="metric-value">{stats.total_claims}</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Supported Ratio</div>
          <div className="metric-value" style={{ color: '#34d399' }}>{stats.approval_rate_pct}%</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">High Risk Profiles</div>
          <div className="metric-value" style={{ color: '#f87171' }}>{stats.high_risk_count}</div>
        </div>

        <div className="metric-card">
          <div className="metric-label">Avg Adjudication Time</div>
          <div className="metric-value">{stats.avg_processing_sec}s</div>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
            Adjudication Status Distribution
          </h2>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                <span style={{ color: '#34d399', fontWeight: 600 }}>Supported Claims</span>
                <span>{stats.supported} records</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#0f172a', height: '10px', borderRadius: '5px', overflow: 'hidden' }}>
                <div style={{ width: `${stats.total_claims ? (stats.supported / stats.total_claims) * 100 : 0}%`, backgroundColor: '#34d399', height: '100%' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                <span style={{ color: '#f87171', fontWeight: 600 }}>Contradicted Claims</span>
                <span>{stats.contradicted} records</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#0f172a', height: '10px', borderRadius: '5px', overflow: 'hidden' }}>
                <div style={{ width: `${stats.total_claims ? (stats.contradicted / stats.total_claims) * 100 : 0}%`, backgroundColor: '#f87171', height: '100%' }} />
              </div>
            </div>

            <div>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.85rem', marginBottom: '0.35rem' }}>
                <span style={{ color: '#fbbf24', fontWeight: 600 }}>Insufficient Evidence / Unclear</span>
                <span>{stats.not_enough_information} records</span>
              </div>
              <div style={{ width: '100%', backgroundColor: '#0f172a', height: '10px', borderRadius: '5px', overflow: 'hidden' }}>
                <div style={{ width: `${stats.total_claims ? (stats.not_enough_information / stats.total_claims) * 100 : 0}%`, backgroundColor: '#fbbf24', height: '100%' }} />
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
            System Infrastructure Overview
          </h2>
          <table className="data-table">
            <tbody>
              <tr>
                <td style={{ fontWeight: 600, color: '#94a3b8' }}>Vision Layer Model</td>
                <td>Google GenAI (gemini-3.1-flash-lite)</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600, color: '#94a3b8' }}>Evidence Engine</td>
                <td>Deterministic Structural Rules</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600, color: '#94a3b8' }}>Database Engine</td>
                <td>MongoDB PyMongo Driver (With Local Persistence)</td>
              </tr>
              <tr>
                <td style={{ fontWeight: 600, color: '#94a3b8' }}>API Throughput</td>
                <td>Sequential Throttling Enabled (5 RPM compliant)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
