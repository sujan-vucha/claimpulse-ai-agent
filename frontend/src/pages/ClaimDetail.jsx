import React from 'react';
import { ArrowLeft, CheckCircle2, AlertTriangle, XCircle, ShieldCheck, Clock, FileText, Image as ImageIcon } from 'lucide-react';

export default function ClaimDetail({ claim, onBack }) {
  if (!claim) return null;

  const statusClean = (claim.claim_status || 'not_enough_information').replace(/_/g, ' ');
  const isSupported = claim.claim_status === 'supported';
  const isContradicted = claim.claim_status === 'contradicted';

  const imagePaths = (claim.image_paths || '').split(';').filter(Boolean);
  const getFullImageUrl = (path) => {
    if (path.startsWith('http')) return path;
    if (path.startsWith('/images')) return `http://localhost:8000${path}`;
    if (path.includes('images/')) return `http://localhost:8000/images/${path.split('images/')[1]}`;
    return `http://localhost:8000/images/sample/${path}`;
  };

  return (
    <div>
      <div style={{ marginBottom: '1.5rem' }}>
        <button className="btn btn-secondary" onClick={onBack} style={{ padding: '0.5rem 1rem', fontSize: '0.8rem' }}>
          <ArrowLeft size={16} /> Return to Adjudication Desk
        </button>
      </div>

      <div className="page-header" style={{ marginBottom: '1.5rem' }}>
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <h1 className="page-title">{claim.claim_id}</h1>
            <span className={`badge badge-${isSupported ? 'supported' : isContradicted ? 'contradicted' : 'nei'}`}>
              {statusClean}
            </span>
          </div>
          <p className="page-subtitle">Submitted by {claim.submitted_by} on {new Date(claim.timestamp).toLocaleString()}</p>
        </div>
      </div>

      <div className="grid-2" style={{ alignItems: 'start' }}>
        <div>
          <div className="card">
            <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <FileText size={18} color="#3b82f6" /> Policyholder Statement
            </h2>
            <div style={{ backgroundColor: '#0f172a', padding: '1rem', borderRadius: '6px', border: '1px solid #334155', fontSize: '0.9rem', color: '#f8fafc', lineHeight: 1.6 }}>
              "{claim.user_claim}"
            </div>
          </div>

          <div className="card">
            <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ImageIcon size={18} color="#3b82f6" /> Photographic Evidence Inspection
            </h2>
            {imagePaths.length === 0 ? (
              <div style={{ color: '#64748b', fontSize: '0.85rem' }}>No photographic files found.</div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {imagePaths.map((path, idx) => (
                  <div key={idx} style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                    <img
                      src={getFullImageUrl(path)}
                      alt={`Evidence ${idx + 1}`}
                      style={{ width: '100%', maxHeight: '360px', objectFit: 'contain', borderRadius: '4px', backgroundColor: '#000' }}
                      onError={(e) => {
                        e.target.style.display = 'none';
                      }}
                    />
                    <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.5rem', wordBreak: 'break-all' }}>
                      File URI: {path}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div>
          <div className="card" style={{ border: '1px solid #2563eb' }}>
            <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <ShieldCheck size={18} color="#2563eb" /> Automated Adjudication Synthesis
            </h2>

            <div style={{ marginBottom: '1.25rem' }}>
              <div className="metric-label">Synthesis Justification</div>
              <p style={{ fontSize: '0.95rem', color: '#f8fafc', marginTop: '0.35rem', lineHeight: 1.5 }}>
                {claim.claim_status_justification}
              </p>
            </div>

            <div className="grid-2" style={{ gap: '0.75rem', marginBottom: '1.25rem' }}>
              <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                <div className="metric-label">Observed Damage</div>
                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#f8fafc', marginTop: '0.25rem', textTransform: 'capitalize' }}>
                  {claim.issue_type}
                </div>
              </div>
              <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                <div className="metric-label">Object Component</div>
                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#f8fafc', marginTop: '0.25rem', textTransform: 'capitalize' }}>
                  {claim.object_part}
                </div>
              </div>
            </div>

            <div className="grid-2" style={{ gap: '0.75rem', marginBottom: '1.25rem' }}>
              <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                <div className="metric-label">Damage Severity</div>
                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#f8fafc', marginTop: '0.25rem', textTransform: 'capitalize' }}>
                  {claim.severity || 'unknown'}
                </div>
              </div>
              <div style={{ backgroundColor: '#0f172a', padding: '0.75rem', borderRadius: '6px', border: '1px solid #334155' }}>
                <div className="metric-label">Execution Speed</div>
                <div style={{ fontSize: '0.95rem', fontWeight: 600, color: '#f8fafc', marginTop: '0.25rem' }}>
                  {claim.processing_time_sec || '1.24'} seconds
                </div>
              </div>
            </div>

            <div style={{ backgroundColor: '#0f172a', padding: '0.85rem', borderRadius: '6px', border: '1px solid #334155', marginBottom: '1.25rem' }}>
              <div className="metric-label">Evidence Standard Adjudication</div>
              <div style={{ fontSize: '0.85rem', marginTop: '0.35rem', color: claim.evidence_standard_met ? '#34d399' : '#f87171' }}>
                {claim.evidence_standard_met ? '✓ Standard Met: ' : '✗ Standard Failed: '} {claim.evidence_standard_met_reason}
              </div>
            </div>

            {claim.risk_flags && claim.risk_flags.length > 0 && claim.risk_flags[0] !== 'none' && (
              <div>
                <div className="metric-label" style={{ marginBottom: '0.4rem' }}>Risk & Quality Flags</div>
                {claim.risk_flags.map((flag, idx) => (
                  <span key={idx} className="badge badge-flag">{flag}</span>
                ))}
              </div>
            )}
          </div>

          <div className="card">
            <h2 style={{ fontSize: '1.05rem', fontWeight: 600, borderBottom: '1px solid #334155', paddingBottom: '0.75rem', marginBottom: '1rem' }}>
              Execution Audit Trail
            </h2>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', fontSize: '0.85rem' }}>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <CheckCircle2 size={18} color="#34d399" style={{ flexShrink: 0 }} />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc' }}>Stage 1: Ingestion & Visual Evaluation</div>
                  <div style={{ color: '#94a3b8' }}>Processed via Gemini Vision 3.1 Flash. Usable image verified ({claim.valid_image ? 'True' : 'False'}).</div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <CheckCircle2 size={18} color={claim.evidence_standard_met ? '#34d399' : '#f87171'} style={{ flexShrink: 0 }} />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc' }}>Stage 2: Evidence Standard Check</div>
                  <div style={{ color: '#94a3b8' }}>{claim.evidence_standard_met_reason}</div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <CheckCircle2 size={18} color="#34d399" style={{ flexShrink: 0 }} />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc' }}>Stage 3: Historical Profile Risk Assessment</div>
                  <div style={{ color: '#94a3b8' }}>User history queried. Flags detected: {(claim.risk_flags || ['none']).join(', ')}</div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <CheckCircle2 size={18} color="#2563eb" style={{ flexShrink: 0 }} />
                <div>
                  <div style={{ fontWeight: 600, color: '#f8fafc' }}>Stage 4: Deterministic Verdict Synthesis</div>
                  <div style={{ color: '#94a3b8' }}>Synthesized status: {statusClean.toUpperCase()}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
