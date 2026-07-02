import React from 'react';
import { ShieldCheck, LayoutDashboard, FileText, BarChart3, Database, LogOut, User } from 'lucide-react';

export default function Navbar({ currentTab, setCurrentTab, user, onLogout }) {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <ShieldCheck color="#2563eb" size={26} />
        <span className="sidebar-title">ClaimPulse</span>
      </div>

      <div className="sidebar-nav">
        <div
          className={`nav-item ${currentTab === 'dashboard' ? 'active' : ''}`}
          onClick={() => setCurrentTab('dashboard')}
        >
          <LayoutDashboard size={18} />
          <span>{user?.role === 'adjuster' ? 'Adjudication Desk' : 'My Recent Claims'}</span>
        </div>

        <div
          className={`nav-item ${currentTab === 'new_claim' ? 'active' : ''}`}
          onClick={() => setCurrentTab('new_claim')}
        >
          <FileText size={18} />
          <span>Submit Claim</span>
        </div>


        {user?.role === 'adjuster' && (
          <>
            <div
              className={`nav-item ${currentTab === 'batch' ? 'active' : ''}`}
              onClick={() => setCurrentTab('batch')}
            >
              <Database size={18} />
              <span>Batch Runner</span>
            </div>

            <div
              className={`nav-item ${currentTab === 'analytics' ? 'active' : ''}`}
              onClick={() => setCurrentTab('analytics')}
            >
              <BarChart3 size={18} />
              <span>Platform Analytics</span>
            </div>
          </>
        )}
      </div>

      <div className="sidebar-footer">
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
          <User size={18} color="#94a3b8" />
          <div>
            <div style={{ fontSize: '0.8rem', fontWeight: 600 }}>{user?.full_name || user?.username}</div>
            <div style={{ fontSize: '0.7rem', color: '#64748b', textTransform: 'capitalize' }}>{user?.role}</div>
          </div>
        </div>
        <button
          onClick={onLogout}
          style={{ background: 'transparent', border: 'none', color: '#94a3b8', cursor: 'pointer' }}
          title="Sign Out"
        >
          <LogOut size={18} />
        </button>
      </div>
    </div>
  );
}
