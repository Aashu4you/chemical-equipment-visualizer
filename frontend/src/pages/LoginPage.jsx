import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AuthPages.css';

const LoginPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        // Store the token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Navigate to dashboard
        navigate('/dashboard');
      } else {
        setError(data.message || 'Login failed. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
      console.error('Login error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-grid-bg"></div>
      
      <div className="auth-content">
        <div className="auth-left">
          <div className="auth-brand" onClick={() => navigate('/')}>
            <span className="brand-icon">⚗</span>
            <span className="brand-text">ChemViz</span>
          </div>
          
          <div className="auth-info">
            <h1 className="auth-info-title">
              Welcome Back to
              <span className="title-gradient"> ChemViz</span>
            </h1>
            <p className="auth-info-subtitle">
              Sign in to access your chemical equipment data visualizations and continue your analysis workflow.
            </p>
            
            <div className="auth-features">
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Secure data storage</span>
              </div>
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Real-time visualization</span>
              </div>
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Export to PDF & CSV</span>
              </div>
            </div>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrapper">
            <div className="auth-form-header">
              <h2 className="auth-form-title">Sign In</h2>
              <p className="auth-form-subtitle">Enter your credentials to access your account</p>
            </div>

            {error && (
              <div className="auth-error">
                <span className="error-icon">⚠</span>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="email" className="form-label">Email Address</label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="your.email@example.com"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="password" className="form-label">Password</label>
                <input
                  type="password"
                  id="password"
                  name="password"
                  value={formData.password}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Enter your password"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-options">
                <label className="checkbox-label">
                  <input type="checkbox" className="form-checkbox" />
                  <span>Remember me</span>
                </label>
                <a href="#" className="forgot-link">Forgot password?</a>
              </div>

              <button type="submit" className="form-submit" disabled={loading}>
                {loading ? (
                  <>
                    <span className="loading-spinner"></span>
                    Signing In...
                  </>
                ) : (
                  <>
                    Sign In
                    <span className="submit-arrow">→</span>
                  </>
                )}
              </button>
            </form>

            <div className="auth-footer">
              <p className="auth-footer-text">
                Don't have an account?{' '}
                <span className="auth-link" onClick={() => navigate('/signup')}>
                  Sign Up
                </span>
              </p>
            </div>

            <div className="auth-back">
              <span className="back-link" onClick={() => navigate('/')}>
                ← Back to Home
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;