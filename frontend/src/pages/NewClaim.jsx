import React, { useState } from 'react';
import { Upload, CheckCircle2, AlertTriangle, ShieldAlert, ArrowRight, FileText } from 'lucide-react';
import { claimAPI } from '../services/api';

export default function NewClaim({ onClaimSubmitted }) {
  const [claimObject, setClaimObject] = useState('car');
  const [userClaim, setUserClaim] = useState('');
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [verdict, setVerdict] = useState(null);

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFiles(Array.from(e.target.files));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (selectedFiles.length === 0) {
      setError('Please upload at least one visual evidence image.');
      return;
    }
    setError('');
    setLoading(true);
    setVerdict(null);

    const formData = new FormData();
    formData.append('claim_object', claimObject);
    formData.append('user_claim', userClaim);
    selectedFiles.forEach((file) => {
      formData.append('images', file);
    });

    try {
      const res = await claimAPI.verify(formData);
      setVerdict(res);
      if (onClaimSubmitted) onClaimSubmitted(res);
    } catch (err) {
      setError(err?.response?.data?.detail || 'Verification error occurred. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">New Visual Evidence Submission</h1>
          <p className="page-subtitle">Submit policyholder damage claims for automated AI visual verification</p>
        </div>
      </div>

      <div className="grid-2">
        <div className="card">
          <h2 style={{ fontSize: '1.1rem', fontWeight: 600, marginBottom: '1.25rem', borderBottom: '1px solid #334155', paddingBottom: '0.75rem' }}>
            Incident Reporting Details
          </h2>

          {error && (
            <div style={{ padding: '0.75rem', backgroundColor: 'rgba(220, 38, 38, 0.15)', border: '1px solid #dc2626', borderRadius: '6px', color: '#fca5a5', fontSize: '0.85rem', marginBottom: '1.25rem' }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Insured Object Category</label>
              <select
                className="form-select"
                value={claimObject}
                onChange={(e) => setClaimObject(e.target.value)}
              >
                <option value="car">Automobile (Vehicle Body, Bumper, Mirror, Windshield)</option>
                <option value="laptop">Electronics / Laptop (Screen, Hinge, Keyboard, Lid)</option>
                <option value="package">Logistics / Package (Shipping Box, Seal, Packaging)</option>
              </select>
            </div>

            <div className="form-group">
              <label className="form-label">Policyholder Stated Claim (Chat Transcript)</label>
              <textarea
                className="form-textarea"
                rows="4"
                placeholder="Describe the incident explicitly (e.g. 'Parked car was hit on the front driver door leaving a deep dent and paint scrape.')"
                value={userClaim}
                onChange={(e) => setUserClaim(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Visual Evidence Images (Upload 1 or more)</label>
              <div
                style={{
                  border: '2px dashed #334155',
                  borderRadius: '6px',
                  padding: '2rem',
                  textAlign: 'center',
                  backgroundColor: '#0f172a',
                  cursor: 'pointer'
                }}
                onClick={() => document.getElementById('file-upload').click()}
              >
                <Upload size={28} color="#64748b" style={{ margin: '0 auto 0.5rem' }} />
                <p style={{ fontSize: '0.9rem', color: '#f8fafc', fontWeight: 500 }}>
                  Click to browse or drag photographic evidence
                </p>
                <p style={{ fontSize: '0.75rem', color: '#64748b' }}>Supports JPEG, PNG (High resolution recommended)</p>
                <input
                  id="file-upload"
                  type="file"
                  multiple
                  accept="image/*"
                  style={{ display: 'none' }}
                  onChange={handleFileChange}
                />
              </div>
              {selectedFiles.length > 0 && (
                <div style={{ marginTop: '0.75rem', fontSize: '0.85rem', color: '#34d399', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <CheckCircle2 size={16} /> Selected {selectedFiles.length} image file(s): {selectedFiles.map(f => f.name).join(', ')}
                </div>
              )}
            </div>

            <button type="submit" className="btn btn-primary" style={{ width: '100%', marginTop: '1rem', padding: '0.8rem' }} disabled={loading}>
              {loading ? 'Executing AI Verification Engine...' : 'Run Automated Adjudication Engine'}
            </button>
          </form>
        </div>

        <div>
          {loading && (
            <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem' }}>
              <div style={{ fontSize: '1.25rem', fontWeight: 600, color: '#3b82f6', marginBottom: '0.5rem' }}>
                Analyzing Visual Evidence...
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                Google GenAI Vision Model inspecting quality flags, structural part alignment, and damage severity against history flags.
              </p>
            </div>
          )}

          {verdict && (
            <div className="card" style={{ border: '1px solid #3b82f6' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
                <h2 style={{ fontSize: '1.1rem', fontWeight: 600 }}>Real-Time Automated Verdict</h2>
                <span className={`badge badge-${verdict.claim_status === 'not_enough_information' ? 'nei' : verdict.claim_status}`}>
                  {verdict.claim_status.replace(/_/g, ' ')}
                </span>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <div className="metric-label">Adjudication Justification</div>
                <p style={{ fontSize: '0.95rem', color: '#f8fafc', marginTop: '0.35rem' }}>
                  {verdict.claim_status_justification}
                </p>
              </div>

              <div className="grid-2" style={{ marginBottom: '1rem', gap: '0.75rem' }}>
                <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                  <div className="metric-label">Detected Issue Type</div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, textTransform: 'capitalize', color: '#f8fafc', marginTop: '0.25rem' }}>
                    {verdict.issue_type} ({verdict.object_part})
                  </div>
                </div>
                <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                  <div className="metric-label">Damage Severity</div>
                  <div style={{ fontSize: '1rem', fontWeight: 600, textTransform: 'capitalize', color: '#f8fafc', marginTop: '0.25rem' }}>
                    {verdict.severity}
                  </div>
                </div>
              </div>

              <div style={{ backgroundColor: '#0f172a', padding: '0.85rem', borderRadius: '6px', border: '1px solid #334155', marginBottom: '1rem' }}>
                <div className="metric-label">Evidence Standard Adjudication</div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginTop: '0.35rem', fontSize: '0.85rem' }}>
                  {verdict.evidence_standard_met ? (
                    <span style={{ color: '#34d399' }}>✓ Met Minimum Evidence Requirements</span>
                  ) : (
                    <span style={{ color: '#f87171' }}>✗ Failed Standard: {verdict.evidence_standard_met_reason}</span>
                  )}
                </div>
              </div>

              {verdict.risk_flags && verdict.risk_flags.length > 0 && verdict.risk_flags[0] !== 'none' && (
                <div>
                  <div className="metric-label" style={{ marginBottom: '0.4rem' }}>Risk & Quality Flags</div>
                  {verdict.risk_flags.map((flag, idx) => (
                    <span key={idx} className="badge badge-flag">{flag}</span>
                  ))}
                </div>
              )}
            </div>
          )}

          {!loading && !verdict && (
            <div className="card" style={{ backgroundColor: '#0f172a', borderStyle: 'dashed', textAlign: 'center', padding: '3rem 2rem' }}>
              <FileText size={36} color="#475569" style={{ margin: '0 auto 0.75rem' }} />
              <h3 style={{ fontSize: '1rem', fontWeight: 600, color: '#f8fafc' }}>Awaiting Evidence Submission</h3>
              <p style={{ fontSize: '0.85rem', color: '#64748b', marginTop: '0.35rem' }}>
                Fill out the claim transcript on the left and upload photographic proof to initiate instant adjudication.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
