import React, { useState, useEffect } from 'react';
import { Search, Filter, RefreshCw, Eye, AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';
import { claimAPI } from '../services/api';

export default function Dashboard({ user, onSelectClaim }) {
  const [claims, setClaims] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filterStatus, setFilterStatus] = useState('all');
  const [filterObject, setFilterObject] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchClaims = async () => {
    setLoading(true);
    try {
      const data = await claimAPI.getAll();
      setClaims(data);
    } catch (err) {
      console.error('Failed to load claims:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchClaims();
  }, []);

  const filteredClaims = claims.filter((c) => {
    if (filterStatus !== 'all' && c.claim_status !== filterStatus) return false;
    if (filterObject !== 'all' && c.claim_object !== filterObject) return false;
    if (searchQuery) {
      const query = searchQuery.toLowerCase();
      const matchId = strContains(c.claim_id, query);
      const matchUser = strContains(c.submitted_by, query);
      const matchText = strContains(c.user_claim, query);
      if (!matchId && !matchUser && !matchText) return false;
    }
    return true;
  });

  function strContains(str, q) {
    return (str || '').toLowerCase().includes(q);
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">{user?.role === 'adjuster' ? 'Enterprise Claims Adjudication Desk' : 'My Submitted Damage Claims'}</h1>
          <p className="page-subtitle">
            {user?.role === 'adjuster'
              ? 'Admin overview of all damage claims submitted across all policyholders'
              : 'Track the real-time AI adjudication verdicts of your submitted damage claims'}
          </p>

        </div>
        <button className="btn btn-secondary" onClick={fetchClaims}>
          <RefreshCw size={16} /> Refresh Records
        </button>
      </div>

      <div className="card" style={{ padding: '1rem' }}>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flexGrow: 1, minWidth: '240px', position: 'relative' }}>
            <Search size={18} color="#64748b" style={{ position: 'absolute', left: '0.75rem', top: '50%', transform: 'translateY(-50%)' }} />
            <input
              type="text"
              className="form-input"
              style={{ paddingLeft: '2.5rem' }}
              placeholder="Search by Claim ID, Policyholder, or Keyword..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Filter size={16} color="#64748b" />
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8' }}>Status:</span>
            <select
              className="form-select"
              style={{ width: 'auto', padding: '0.5rem 0.75rem' }}
              value={filterStatus}
              onChange={(e) => setFilterStatus(e.target.value)}
            >
              <option value="all">All Verdicts</option>
              <option value="supported">Supported</option>
              <option value="contradicted">Contradicted</option>
              <option value="not_enough_information">Insufficient Info</option>
            </select>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8' }}>Object:</span>
            <select
              className="form-select"
              style={{ width: 'auto', padding: '0.5rem 0.75rem' }}
              value={filterObject}
              onChange={(e) => setFilterObject(e.target.value)}
            >
              <option value="all">All Categories</option>
              <option value="car">Car / Vehicle</option>
              <option value="laptop">Laptop / Electronics</option>
              <option value="package">Package / Shipping</option>
            </select>
          </div>
        </div>
      </div>

      <div className="card" style={{ padding: 0, overflowX: 'auto' }}>
        {loading ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#94a3b8' }}>Loading records...</div>
        ) : filteredClaims.length === 0 ? (
          <div style={{ padding: '3rem', textAlign: 'center', color: '#64748b' }}>No claims matching your criteria.</div>
        ) : (
          <table className="data-table">
            <thead>
              <tr>
                <th>Claim Identifier</th>
                <th>Policyholder</th>
                <th>Object Category</th>
                <th>Visible Issue & Part</th>
                <th>AI Verdict Status</th>
                <th>Evidence Standard</th>
                <th>Severity</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {filteredClaims.map((claim) => {
                const statusClean = (claim.claim_status || 'not_enough_information').replace(/_/g, ' ');
                const isSupported = claim.claim_status === 'supported';
                const isContradicted = claim.claim_status === 'contradicted';
                
                return (
                  <tr key={claim.claim_id}>
                    <td style={{ fontWeight: 600, color: '#3b82f6' }}>{claim.claim_id}</td>
                    <td>{claim.submitted_by}</td>
                    <td style={{ textTransform: 'capitalize' }}>{claim.claim_object}</td>
                    <td>
                      <span style={{ fontWeight: 500, textTransform: 'capitalize' }}>{claim.issue_type}</span>
                      <div style={{ fontSize: '0.75rem', color: '#64748b' }}>Part: {claim.object_part}</div>
                    </td>
                    <td>
                      <span className={`badge badge-${isSupported ? 'supported' : isContradicted ? 'contradicted' : 'nei'}`}>
                        {statusClean}
                      </span>
                    </td>
                    <td>
                      {claim.evidence_standard_met ? (
                        <span style={{ color: '#34d399', fontSize: '0.8rem', fontWeight: 500 }}>✓ Standard Met</span>
                      ) : (
                        <span style={{ color: '#f87171', fontSize: '0.8rem', fontWeight: 500 }}>✗ Failed Standard</span>
                      )}
                    </td>
                    <td style={{ textTransform: 'capitalize', fontWeight: 500 }}>
                      {claim.severity || 'unknown'}
                    </td>
                    <td>
                      <button
                        className="btn btn-secondary"
                        style={{ padding: '0.4rem 0.75rem', fontSize: '0.75rem' }}
                        onClick={() => onSelectClaim(claim)}
                      >
                        <Eye size={14} /> Audit Detail
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
