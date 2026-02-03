import React from 'react';
import { useNavigate } from 'react-router-dom';
import './LandingPage.css';

const LandingPage = () => {
  const navigate = useNavigate();

  return (
    <div className="landing-container">
      <div className="landing-grid-bg"></div>
      
      <nav className="landing-nav">
        <div className="nav-logo">
          <span className="logo-icon">⚗</span>
          <span className="logo-text">ChemViz</span>
        </div>
        <div className="nav-actions">
          <button className="nav-btn" onClick={() => navigate('/login')}>
            Sign In
          </button>
          <button className="nav-btn nav-btn-primary" onClick={() => navigate('/signup')}>
            Get Started
          </button>
        </div>
      </nav>

      <main className="landing-main">
        <div className="hero-section">
          <div className="hero-label">
            <span className="label-dot"></span>
            Data Visualization Platform
          </div>
          
          <h1 className="hero-title">
            Transform Chemical Equipment Data into
            <span className="title-highlight"> Actionable Insights</span>
          </h1>
          
          <p className="hero-subtitle">
            Upload CSV files, generate stunning visualizations, and export comprehensive PDF reports with statistical analysis—all in one seamless workflow.
          </p>

          <div className="hero-cta">
            <button className="cta-primary" onClick={() => navigate('/signup')}>
              Start Visualizing
              <span className="cta-arrow">→</span>
            </button>
            <button className="cta-secondary" onClick={() => navigate('/login')}>
              Sign In
            </button>
          </div>

          <div className="hero-stats">
            <div className="stat-item">
              <div className="stat-number">CSV</div>
              <div className="stat-label">Data Import</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">PDF</div>
              <div className="stat-label">Export Reports</div>
            </div>
            <div className="stat-divider"></div>
            <div className="stat-item">
              <div className="stat-number">∞</div>
              <div className="stat-label">Visualizations</div>
            </div>
          </div>
        </div>

        <div className="features-section">
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">📊</div>
              <h3 className="feature-title">Advanced Visualization</h3>
              <p className="feature-description">
                Generate professional charts and graphs using Matplotlib and Pyplot. Customize colors, labels, and layouts.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📈</div>
              <h3 className="feature-title">Statistical Analysis</h3>
              <p className="feature-description">
                Automatic calculation of averages, trends, and key metrics from your chemical equipment data.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">📄</div>
              <h3 className="feature-title">PDF Reports</h3>
              <p className="feature-description">
                Download comprehensive reports combining data tables, visualizations, and statistical summaries.
              </p>
            </div>

            <div className="feature-card">
              <div className="feature-icon">💾</div>
              <h3 className="feature-title">CSV Export</h3>
              <p className="feature-description">
                Export processed data and analysis results back to CSV format for further analysis.
              </p>
            </div>
          </div>
        </div>

        <div className="workflow-section">
          <h2 className="section-title">How It Works</h2>
          <div className="workflow-steps">
            <div className="workflow-step">
              <div className="step-number">01</div>
              <div className="step-content">
                <h3 className="step-title">Upload Data</h3>
                <p className="step-description">Import your chemical equipment data via CSV file</p>
              </div>
            </div>
            
            <div className="workflow-connector"></div>
            
            <div className="workflow-step">
              <div className="step-number">02</div>
              <div className="step-content">
                <h3 className="step-title">Visualize</h3>
                <p className="step-description">Automatic chart generation and statistical analysis</p>
              </div>
            </div>
            
            <div className="workflow-connector"></div>
            
            <div className="workflow-step">
              <div className="step-number">03</div>
              <div className="step-content">
                <h3 className="step-title">Export</h3>
                <p className="step-description">Download as PDF report or CSV file</p>
              </div>
            </div>
          </div>
        </div>

        <div className="cta-section">
          <div className="cta-box">
            <h2 className="cta-title">Ready to Transform Your Data?</h2>
            <p className="cta-text">
              Join researchers and engineers using ChemViz for chemical equipment data analysis
            </p>
            <button className="cta-final" onClick={() => navigate('/signup')}>
              Create Free Account
              <span className="cta-arrow">→</span>
            </button>
          </div>
        </div>
      </main>

      <footer className="landing-footer">
        <div className="footer-content">
          <div className="footer-logo">
            <span className="logo-icon">⚗</span>
            <span className="logo-text">ChemViz</span>
          </div>
          <p className="footer-text">© 2026 Chemical Equipment Visualizer. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;