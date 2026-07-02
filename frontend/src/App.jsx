import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import NewClaim from './pages/NewClaim';
import ClaimDetail from './pages/ClaimDetail';
import BatchProcessing from './pages/BatchProcessing';
import Analytics from './pages/Analytics';
import { authAPI } from './services/api';

export default function App() {
  const [user, setUser] = useState(null);
  const [currentTab, setCurrentTab] = useState('dashboard');
  const [selectedClaim, setSelectedClaim] = useState(null);

  useEffect(() => {
    const handleUnauth = () => {
      setUser(null);
    };
    window.addEventListener('auth_unauthorized', handleUnauth);

    const token = localStorage.getItem('token');
    const existingUser = authAPI.getCurrentUser();
    if (existingUser && token) {
      authAPI.verifyToken().then((validUser) => {
        setUser(validUser);
        if (validUser.role === 'policyholder') {
          setCurrentTab('new_claim');
        }
      }).catch(() => {
        authAPI.logout();
        setUser(null);
      });
    } else {
      authAPI.logout();
      setUser(null);
    }

    return () => window.removeEventListener('auth_unauthorized', handleUnauth);
  }, []);

  const handleLogout = () => {
    authAPI.logout();
    setUser(null);
  };

  const handleSelectClaim = (claim) => {
    setSelectedClaim(claim);
    setCurrentTab('claim_detail');
  };

  if (!user) {
    return <Login onLoginSuccess={(u) => {
      setUser(u);
      setCurrentTab(u.role === 'adjuster' ? 'dashboard' : 'new_claim');
    }} />;
  }

  return (
    <div className="app-container">
      <Navbar
        currentTab={currentTab}
        setCurrentTab={(tab) => {
          setSelectedClaim(null);
          setCurrentTab(tab);
        }}
        user={user}
        onLogout={handleLogout}
      />
      <div className="main-content">
        {currentTab === 'dashboard' && (
          <Dashboard user={user} onSelectClaim={handleSelectClaim} />
        )}
        {currentTab === 'new_claim' && (
          <NewClaim onClaimSubmitted={(res) => {
            // Automatically switch to audit detail view when claim submitted
            setSelectedClaim(res);
            setCurrentTab('claim_detail');
          }} />
        )}
        {currentTab === 'claim_detail' && (
          <ClaimDetail claim={selectedClaim} onBack={() => setCurrentTab('dashboard')} />
        )}
        {currentTab === 'batch' && user.role === 'adjuster' && (
          <BatchProcessing />
        )}
        {currentTab === 'analytics' && user.role === 'adjuster' && (
          <Analytics />
        )}
      </div>
    </div>
  );
}
