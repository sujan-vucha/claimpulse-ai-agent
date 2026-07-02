import React, { useState } from 'react';
import { ShieldCheck, Lock, Mail, User, Briefcase, ArrowRight, CheckCircle2 } from 'lucide-react';
import { authAPI } from '../services/api';

export default function Login({ onLoginSuccess }) {
  const [isRegistering, setIsRegistering] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [role, setRole] = useState('policyholder');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      let res;
      if (isRegistering) {
        res = await authAPI.register(username, password, role, fullName);
      } else {
        res = await authAPI.login(username, password);
      }
      onLoginSuccess(res.user);
    } catch (err) {
      const detail = err?.response?.data?.detail;
      if (typeof detail === 'string') {
        setError(detail);
      } else if (Array.isArray(detail)) {
        setError(detail.map(d => d.msg || JSON.stringify(d)).join(', '));
      } else {
        setError('Authentication failed. Please check your credentials.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', minHeight: '100vh', width: '100vw', backgroundColor: '#0A0E17', overflow: 'hidden' }}>
      {/* Left Column - Professional Insurance Human Collaboration Video & Centered Premium Crystal Glass */}
      <div style={{
        flex: '1 1 55%',
        position: 'relative',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
        padding: '3.5rem',
        overflow: 'hidden',
        borderRight: '1px solid rgba(255, 255, 255, 0.08)'
      }}>
        {/* Background Motion Video of Human Insurance Professionals / Consulting */}
        <video
          autoPlay
          loop
          muted
          playsInline
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'brightness(0.45) contrast(1.05)',
            zIndex: 0
          }}
          poster="https://images.unsplash.com/photo-1556761175-5973dc0f32e7?auto=format&fit=crop&w=1920&q=80"
        >
          <source src="https://assets.mixkit.co/videos/preview/mixkit-two-professionals-shaking-hands-in-an-office-43632-large.mp4" type="video/mp4" />
          <source src="https://assets.mixkit.co/videos/preview/mixkit-business-people-meeting-in-a-conference-room-41585-large.mp4" type="video/mp4" />
          <source src="https://assets.mixkit.co/videos/preview/mixkit-hands-holding-a-tablet-with-graphs-41158-large.mp4" type="video/mp4" />
        </video>

        {/* Elegant Dark Vignette Overlay */}
        <div style={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          background: 'linear-gradient(135deg, rgba(10, 14, 23, 0.75) 0%, rgba(10, 14, 23, 0.45) 50%, rgba(10, 14, 23, 0.85) 100%)',
          zIndex: 1
        }} />

        {/* Top Header - Subtle Corporate Identity */}
        <div style={{ position: 'relative', zIndex: 2, display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div style={{
            width: '38px',
            height: '38px',
            borderRadius: '8px',
            background: 'rgba(255, 255, 255, 0.15)',
            backdropFilter: 'blur(10px)',
            border: '1px solid rgba(255, 255, 255, 0.25)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center'
          }}>
            <ShieldCheck color="#ffffff" size={22} />
          </div>
          <div>
            <span style={{ fontSize: '1.3rem', fontWeight: 700, color: '#ffffff', letterSpacing: '-0.02em' }}>ClaimPulse</span>
            <span style={{ fontSize: '0.7rem', display: 'block', color: 'rgba(255, 255, 255, 0.7)', textTransform: 'uppercase', letterSpacing: '0.12em', fontWeight: 600 }}>Enterprise Insurance Suite</span>
          </div>
        </div>

        {/* Perfectly Centered Premium Architectural Crystal Glass Card */}
        <div style={{
          position: 'relative',
          zIndex: 2,
          margin: 'auto 0',
          background: 'rgba(255, 255, 255, 0.08)',
          backdropFilter: 'blur(32px) saturate(180%)',
          WebkitBackdropFilter: 'blur(32px) saturate(180%)',
          border: '1px solid rgba(255, 255, 255, 0.22)',
          borderRadius: '20px',
          padding: '2.75rem',
          maxWidth: '540px',
          boxShadow: '0 30px 60px rgba(0, 0, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.3)'
        }}>
          <div style={{
            display: 'inline-block',
            padding: '0.35rem 0.85rem',
            borderRadius: '50px',
            backgroundColor: 'rgba(255, 255, 255, 0.12)',
            border: '1px solid rgba(255, 255, 255, 0.2)',
            fontSize: '0.75rem',
            fontWeight: 600,
            color: '#ffffff',
            letterSpacing: '0.06em',
            marginBottom: '1.25rem'
          }}>
            INTELLIGENT CLAIMS ADJUDICATION
          </div>

          <h1 style={{ fontSize: '2.1rem', fontWeight: 700, color: '#ffffff', lineHeight: 1.25, marginBottom: '1rem', letterSpacing: '-0.02em' }}>
            Next-Generation Insurance Assessment
          </h1>
          
          <p style={{ fontSize: '1rem', color: 'rgba(255, 255, 255, 0.8)', lineHeight: 1.65, marginBottom: '2.25rem', fontWeight: 400 }}>
            Connecting policyholders and claims adjusters through transparent visual inspection, automated structural rules, and verifiable audit trails.
          </p>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: '1.5rem', borderTop: '1px solid rgba(255, 255, 255, 0.18)', paddingTop: '1.5rem' }}>
            <div>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#ffffff' }}>Instant</div>
              <div style={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.65)' }}>Intake Processing</div>
            </div>
            <div>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#ffffff' }}>100%</div>
              <div style={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.65)' }}>Audit Traceability</div>
            </div>
            <div>
              <div style={{ fontSize: '1.4rem', fontWeight: 700, color: '#ffffff' }}>Enterprise</div>
              <div style={{ fontSize: '0.8rem', color: 'rgba(255, 255, 255, 0.65)' }}>Grade Compliance</div>
            </div>
          </div>
        </div>

        {/* Subtle Footer Tag */}
        <div style={{ position: 'relative', zIndex: 2, fontSize: '0.75rem', color: 'rgba(255, 255, 255, 0.5)' }}>
          © {new Date().getFullYear()} ClaimPulse Platform. Built for professional adjudication.
        </div>
      </div>

      {/* Right Column - Ultra Minimal Authentication Portal */}
      <div style={{
        flex: '1 1 45%',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '3.5rem',
        backgroundColor: '#0A0E17'
      }}>
        <div style={{ width: '100%', maxWidth: '380px' }}>
          <div style={{ marginBottom: '2.5rem' }}>
            <h2 style={{ fontSize: '1.75rem', fontWeight: 700, color: '#ffffff', marginBottom: '0.5rem', letterSpacing: '-0.02em' }}>
              {isRegistering ? 'Create Enterprise Account' : 'Sign in to ClaimPulse'}
            </h2>
            <p style={{ fontSize: '0.9rem', color: '#64748b' }}>
              {isRegistering ? 'Register your user or adjuster credentials' : 'Enter your email and password to continue'}
            </p>
          </div>

          {error && (
            <div style={{
              padding: '0.85rem 1rem',
              backgroundColor: 'rgba(239, 68, 68, 0.1)',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              borderRadius: '8px',
              color: '#f87171',
              fontSize: '0.85rem',
              marginBottom: '1.5rem',
              lineHeight: 1.4
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            {isRegistering && (
              <div style={{ marginBottom: '1.25rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.4rem' }}>
                  Full Name
                </label>
                <div style={{ position: 'relative' }}>
                  <User size={16} color="#64748b" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)' }} />
                  <input
                    type="text"
                    style={{
                      width: '100%',
                      backgroundColor: '#111827',
                      border: '1px solid #1f2937',
                      borderRadius: '8px',
                      padding: '0.75rem 1rem 0.75rem 2.6rem',
                      color: '#ffffff',
                      fontSize: '0.9rem',
                      outline: 'none',
                      transition: 'all 0.2s'
                    }}
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Alex Morgan"
                    required
                  />
                </div>
              </div>
            )}

            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.4rem' }}>
                Email Address
              </label>
              <div style={{ position: 'relative' }}>
                <Mail size={16} color="#64748b" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)' }} />
                <input
                  type="text"
                  style={{
                    width: '100%',
                    backgroundColor: '#111827',
                    border: '1px solid #1f2937',
                    borderRadius: '8px',
                    padding: '0.75rem 1rem 0.75rem 2.6rem',
                    color: '#ffffff',
                    fontSize: '0.9rem',
                    outline: 'none',
                    transition: 'all 0.2s'
                  }}
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="name@company.com"
                  required
                />
              </div>
            </div>

            <div style={{ marginBottom: isRegistering ? '1.25rem' : '1.75rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.4rem' }}>
                Password
              </label>
              <div style={{ position: 'relative' }}>
                <Lock size={16} color="#64748b" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)' }} />
                <input
                  type="password"
                  style={{
                    width: '100%',
                    backgroundColor: '#111827',
                    border: '1px solid #1f2937',
                    borderRadius: '8px',
                    padding: '0.75rem 1rem 0.75rem 2.6rem',
                    color: '#ffffff',
                    fontSize: '0.9rem',
                    outline: 'none',
                    transition: 'all 0.2s'
                  }}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  required
                />
              </div>
            </div>

            {isRegistering && (
              <div style={{ marginBottom: '1.75rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 600, color: '#94a3b8', marginBottom: '0.4rem' }}>
                  Account Role
                </label>
                <div style={{ position: 'relative' }}>
                  <Briefcase size={16} color="#64748b" style={{ position: 'absolute', left: '1rem', top: '50%', transform: 'translateY(-50%)' }} />
                  <select
                    style={{
                      width: '100%',
                      backgroundColor: '#111827',
                      border: '1px solid #1f2937',
                      borderRadius: '8px',
                      padding: '0.75rem 1rem 0.75rem 2.6rem',
                      color: '#ffffff',
                      fontSize: '0.9rem',
                      outline: 'none',
                      cursor: 'pointer'
                    }}
                    value={role}
                    onChange={(e) => setRole(e.target.value)}
                  >
                    <option value="policyholder">Policyholder (Submit & Track Claims)</option>
                    <option value="adjuster">Claims Adjuster (Admin Overview)</option>
                  </select>
                </div>
              </div>
            )}

            <button
              type="submit"
              style={{
                width: '100%',
                backgroundColor: '#2563eb',
                color: '#ffffff',
                border: 'none',
                borderRadius: '8px',
                padding: '0.85rem',
                fontSize: '0.95rem',
                fontWeight: 600,
                cursor: loading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.5rem',
                transition: 'background-color 0.2s',
                boxShadow: '0 4px 12px rgba(37, 99, 235, 0.3)'
              }}
              disabled={loading}
            >
              {loading ? 'Authenticating...' : (
                <>
                  {isRegistering ? 'Create Account' : 'Sign In'} <ArrowRight size={16} />
                </>
              )}
            </button>
          </form>

          <div style={{ marginTop: '2rem', textAlign: 'center', fontSize: '0.85rem', color: '#64748b' }}>
            {isRegistering ? 'Already have an account? ' : "Don't have an account? "}
            <span
              style={{ color: '#60a5fa', cursor: 'pointer', fontWeight: 600, transition: 'color 0.2s' }}
              onClick={() => {
                setIsRegistering(!isRegistering);
                setError('');
              }}
            >
              {isRegistering ? 'Sign In' : 'Create Account'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
