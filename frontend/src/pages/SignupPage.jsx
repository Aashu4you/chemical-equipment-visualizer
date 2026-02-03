import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './AuthPages.css';

const SignupPage = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: ''
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

  const validateForm = () => {
    if (formData.password.length < 6) {
      setError('Password must be at least 6 characters long');
      return false;
    }
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      return false;
    }
    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (!validateForm()) {
      return;
    }

    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/api/signup', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: formData.name,
          email: formData.email,
          password: formData.password
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Store the token and user data
        localStorage.setItem('token', data.token);
        localStorage.setItem('user', JSON.stringify(data.user));
        
        // Navigate to dashboard
        navigate('/dashboard');
      } else {
        setError(data.message || 'Signup failed. Please try again.');
      }
    } catch (err) {
      setError('Network error. Please check your connection and try again.');
      console.error('Signup error:', err);
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
              Start Your Journey with
              <span className="title-gradient"> ChemViz</span>
            </h1>
            <p className="auth-info-subtitle">
              Create your account to unlock powerful chemical equipment data visualization and analysis tools.
            </p>
            
            <div className="auth-features">
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Upload unlimited CSV files</span>
              </div>
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Generate custom visualizations</span>
              </div>
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Export comprehensive reports</span>
              </div>
              <div className="auth-feature">
                <div className="feature-check">✓</div>
                <span>Statistical analysis tools</span>
              </div>
            </div>
          </div>
        </div>

        <div className="auth-right">
          <div className="auth-form-wrapper">
            <div className="auth-form-header">
              <h2 className="auth-form-title">Create Account</h2>
              <p className="auth-form-subtitle">Fill in your details to get started</p>
            </div>

            {error && (
              <div className="auth-error">
                <span className="error-icon">⚠</span>
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-group">
                <label htmlFor="name" className="form-label">Full Name</label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="John Doe"
                  required
                  disabled={loading}
                />
              </div>

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
                  placeholder="At least 6 characters"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label htmlFor="confirmPassword" className="form-label">Confirm Password</label>
                <input
                  type="password"
                  id="confirmPassword"
                  name="confirmPassword"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className="form-input"
                  placeholder="Re-enter your password"
                  required
                  disabled={loading}
                />
              </div>

              <div className="form-terms">
                <label className="checkbox-label">
                  <input type="checkbox" className="form-checkbox" required />
                  <span>I agree to the Terms of Service and Privacy Policy</span>
                </label>
              </div>

              <button type="submit" className="form-submit" disabled={loading}>
                {loading ? (
                  <>
                    <span className="loading-spinner"></span>
                    Creating Account...
                  </>
                ) : (
                  <>
                    Create Account
                    <span className="submit-arrow">→</span>
                  </>
                )}
              </button>
            </form>

            <div className="auth-footer">
              <p className="auth-footer-text">
                Already have an account?{' '}
                <span className="auth-link" onClick={() => navigate('/login')}>
                  Sign In
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

export default SignupPage;