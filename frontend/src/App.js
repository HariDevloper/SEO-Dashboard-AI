import React, { useState } from "react";
import './App.css';

const Icon = ({ name, size = 18, className = "" }) => {
  const icons = {
    'bar-chart': <path d="M12 20V10M18 20V4M6 20v-6" />,
    'star': <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z" />,
    'settings': <><path d="M12 15a3 3 0 100-6 3 3 0 000 6z" /><path d="M19.4 15a1.65 1.65 0 00.33 1.82l.06.06a2 2 0 010 2.83 2 2 0 01-2.83 0l-.06-.06a1.65 1.65 0 00-1.82-.33 1.65 1.65 0 00-1 1.51V21a2 2 0 01-2 2 2 2 0 01-2-2v-.09A1.65 1.65 0 009 19.4a1.65 1.65 0 00-1.82.33l-.06.06a2 2 0 01-2.83 0 2 2 0 010-2.83l.06-.06a1.65 1.65 0 00.33-1.82 1.65 1.65 0 00-1.51-1H3a2 2 0 01-2-2 2 2 0 012-2h.09A1.65 1.65 0 004.6 9a1.65 1.65 0 00-.33-1.82l-.06-.06a2 2 0 010-2.83 2 2 0 012.83 0l.06.06a1.65 1.65 0 001.82.33H9a1.65 1.65 0 001-1.51V3a2 2 0 012-2 2 2 0 012 2v.09a1.65 1.65 0 001 1.51 1.65 1.65 0 001.82-.33l.06-.06a2 2 0 012.83 0 2 2 0 010 2.83l-.06.06a1.65 1.65 0 00-.33 1.82V9a1.65 1.65 0 001.51 1H21a2 2 0 012 2 2 2 0 01-2 2h-.09a1.65 1.65 0 00-1.51 1z" /></>,
    'file-text': <><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z" /><polyline points="14 2 14 8 20 8" /><line x1="16" y1="13" x2="8" y2="13" /><line x1="16" y1="17" x2="8" y2="17" /><line x1="10" y1="9" x2="8" y2="9" /></>,
    'layers': <><polygon points="12 2 2 7 12 12 22 7 12 2" /><polyline points="2 17 12 22 22 17" /><polyline points="2 12 12 17 22 12" /></>,
    'cpu': <><rect x="4" y="4" width="16" height="16" rx="2" ry="2" /><rect x="9" y="9" width="6" height="6" /><line x1="9" y1="1" x2="9" y2="4" /><line x1="15" y1="1" x2="15" y2="4" /><line x1="9" y1="20" x2="9" y2="23" /><line x1="15" y1="20" x2="15" y2="23" /><line x1="20" y1="9" x2="23" y2="9" /><line x1="20" y1="14" x2="23" y2="14" /><line x1="1" y1="9" x2="4" y2="9" /><line x1="1" y1="14" x2="4" y2="14" /></>,
    'check-circle': <><path d="M22 11.08V12a10 10 0 11-5.93-9.14" /><polyline points="22 4 12 14.01 9 11.01" /></>,
    'alert-triangle': <><path d="M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z" /><line x1="12" y1="9" x2="12" y2="13" /><line x1="12" y1="17" x2="12.01" y2="17" /></>,
    'alert-circle': <><circle cx="12" cy="12" r="10" /><line x1="12" y1="8" x2="12" y2="12" /><line x1="12" y1="16" x2="12.01" y2="16" /></>,
    'search': <><circle cx="11" cy="11" r="8" /><line x1="21" y1="21" x2="16.65" y2="16.65" /></>,
    'award': <><circle cx="12" cy="8" r="7" /><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88" /></>,
    'user-check': <><path d="M16 21v-2a4 4 0 00-4-4H5a4 4 0 00-4 4v2" /><circle cx="8.5" cy="7" r="4" /><polyline points="17 11 19 13 23 9" /></>,
    'lightbulb': <><path d="M9 18h6" /><path d="M10 22h4" /><path d="M15.09 14c.18-.98.65-1.74 1.41-2.5A4.65 4.65 0 0018 8 6 6 0 006 8c0 1 .23 2.23 1.5 3.5A4.61 4.61 0 019 14" /></>,
    'link': <><path d="M10 13a5 5 0 007.54.54l3-3a5 5 0 00-7.07-7.07l-1.72 1.71" /><path d="M14 11a5 5 0 00-7.54-.54l-3 3a5 5 0 007.07 7.07l1.71-1.71" /></>,
    'activity': <polyline points="22 12 18 12 15 21 9 3 6 12 2 12" />,
    'chevron-right': <polyline points="9 18 15 12 9 6" />,
    'chevron-down': <polyline points="6 9 12 15 18 9" />
  };

  return (
    <svg
      xmlns="http://www.w3.org/2000/svg"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
      style={{ display: 'inline-block', verticalAlign: 'middle' }}
    >
      {icons[name] || icons['alert-circle']}
    </svg>
  );
};

function App() {
  const [url, setUrl] = useState("");
  const [maxPages, setMaxPages] = useState(5);
  const [maxDepth, setMaxDepth] = useState(2);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [activeTab, setActiveTab] = useState("overview");
  const [loadingProgress, setLoadingProgress] = useState("");

  const API_BASE = "http://127.0.0.1:5000/api";

  const runAudit = async () => {
    if (!url) {
      setError("Please enter a URL");
      return;
    }

    setLoading(true);
    setError(null);
    setResult(null);
    setLoadingProgress("Crawling and analyzing your website...");

    try {
      const res = await fetch(`${API_BASE}/audit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, max_pages: maxPages, max_depth: maxDepth })
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.error || `Error: ${res.status}`);
      }

      setResult(data);
      setActiveTab("overview");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
      setLoadingProgress("");
    }
  };

  const exportReport = async (format) => {
    if (!result) return;

    try {
      const res = await fetch(`${API_BASE}/export/${format}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          analysis: result.analysis,
          url: result.url
        })
      });

      if (!res.ok) throw new Error("Export failed");

      const blob = await res.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = downloadUrl;

      // Generate filename with timestamp
      const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
      link.download = `seo_audit_${timestamp}.${format}`;

      // Force download attribute
      link.setAttribute('download', link.download);

      // Append to body, click, and remove
      document.body.appendChild(link);
      link.click();

      // Clean up
      setTimeout(() => {
        document.body.removeChild(link);
        window.URL.revokeObjectURL(downloadUrl);
      }, 100);

    } catch (err) {
      alert("Failed to export: " + err.message);
    }
  };

  const getScoreClass = (score) => {
    if (score >= 80) return 'score-excellent';
    if (score >= 60) return 'score-good';
    if (score >= 40) return 'score-needs-improvement';
    return 'score-poor';
  };

  const getStatusClass = (score) => {
    if (score >= 80) return 'status-excellent';
    if (score >= 60) return 'status-good';
    if (score >= 40) return 'status-needs-improvement';
    return 'status-poor';
  };

  const getScoreStatus = (score) => {
    if (score >= 80) return 'Excellent';
    if (score >= 60) return 'Good';
    if (score >= 40) return 'Needs Improvement';
    return 'Poor';
  };

  return (
    <div className="app-layout">
      {/* Top Navbar */}
      {/* Top Navbar */}
      <nav className="navbar">
        <div className="navbar-content">
          <div className="navbar-brand">
            <span style={{ display: 'flex', color: 'var(--primary)', marginRight: '0.75rem' }}>
              <Icon name="activity" size={28} />
            </span>
            <span>SEO Audit Platform</span>
          </div>

          <div className="navbar-controls-wrapper">
            <div className="navbar-search">
              <input
                type="text"
                className="url-input"
                placeholder="Enter website URL (e.g., https://example.com)"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && runAudit()}
              />
            </div>

            <div className="navbar-settings">
              <div className="setting-group">
                <label className="setting-label">Max Pages</label>
                <select
                  className="setting-select"
                  value={maxPages}
                  onChange={(e) => setMaxPages(Number(e.target.value))}
                >
                  <option value={1}>1</option>
                  <option value={5}>5</option>
                  <option value={10}>10</option>
                  <option value={20}>20</option>
                  <option value={50}>50</option>
                  <option value={100}>100</option>
                </select>
              </div>

              <div className="setting-group">
                <label className="setting-label">Depth</label>
                <select
                  className="setting-select"
                  value={maxDepth}
                  onChange={(e) => setMaxDepth(Number(e.target.value))}
                >
                  <option value={0}>Home</option>
                  <option value={1}>1 Lvl</option>
                  <option value={2}>2 Lvl</option>
                  <option value={3}>3 Lvl</option>
                </select>
              </div>

              <button
                className="btn btn-primary"
                onClick={runAudit}
                disabled={loading}
                style={{ flexShrink: 0, height: '42px', marginTop: 'auto' }}
              >
                {loading ? (
                  <>
                    <div className="spinner" style={{ width: '16px', height: '16px', border: '2px solid rgba(255,255,255,0.3)', borderTopColor: 'white', marginRight: '0.5rem' }}></div>
                    Analyzing...
                  </>
                ) : (
                  <>
                    <Icon name="search" size={18} style={{ marginRight: '0.5rem' }} />
                    Analyze
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <div className="main-content">
        {/* Left Sidebar */}
        <aside className="sidebar">
          {result ? (
            <div className="sidebar-section">
              <h3 className="sidebar-title">Export Report</h3>
              <div className="export-buttons">
                <button className="btn-export" onClick={() => exportReport('pdf')}>
                  <Icon name="file-text" size={16} />
                  PDF
                </button>
                <button className="btn-export" onClick={() => exportReport('csv')}>
                  <Icon name="bar-chart" size={16} />
                  CSV
                </button>
                <button className="btn-export" onClick={() => exportReport('json')}>
                  <Icon name="cpu" size={16} />
                  JSON
                </button>
              </div>
            </div>
          ) : (
            <>
              <div className="sidebar-section">
                <h3 className="sidebar-title">About Platform</h3>
                <p className="about-text">
                  AI-powered SEO audit platform that analyzes your website for technical issues, content quality, and accessibility.
                </p>
              </div>
              <div className="sidebar-section">
                <h3 className="sidebar-title">Features</h3>
                <div className="info-item">
                  <div className="info-label">
                    <Icon name="settings" size={16} />
                    Technical SEO
                  </div>
                  <div className="info-description">Checks titles, metas, headings, and more</div>
                </div>
                <div className="info-item">
                  <div className="info-label">
                    <Icon name="file-text" size={16} />
                    Content Analysis
                  </div>
                  <div className="info-description">Word count, readability, keyword usage</div>
                </div>
                <div className="info-item">
                  <div className="info-label">
                    <Icon name="user-check" size={16} />
                    Accessibility
                  </div>
                  <div className="info-description">Alt text, ARIA labels, semantic HTML</div>
                </div>
              </div>
            </>
          )}
        </aside>

        {/* Results Area */}
        <main className="results-area">
          {!loading && !result && !error && (
            <div className="empty-state">
              <div className="empty-state-icon">🔍</div>
              <h2 className="empty-state-title">Ready to Analyze</h2>
              <p className="empty-state-text">
                Enter a website URL above and click "Analyze" to start your SEO audit
              </p>
            </div>
          )}

          {loading && (
            <div className="loading-state">
              <div className="spinner" style={{ width: '64px', height: '64px', marginBottom: '2rem' }}></div>
              <div className="loading-text" style={{ fontSize: '1.5rem', fontWeight: 700, marginBottom: '0.5rem' }}>
                {loadingProgress || "Analyzing..."}
              </div>
              <div style={{ color: 'var(--gray-500)', marginTop: '0.5rem' }}>
                Please wait while we crawl and analyze your website
              </div>
            </div>
          )}

          {error && (
            <div className="error-state">
              <div className="error-title">⚠️ Analysis Failed</div>
              <div className="error-message">{error}</div>
            </div>
          )}

          {result && result.analysis && (
            <div>
              {/* Score Overview */}
              <div className="score-card">
                <div className={`score-value ${getScoreClass(result.analysis.summary.average_scores.overall)}`}>
                  {result.analysis.summary.average_scores.overall}
                </div>
                <div className="score-label">Overall SEO Score</div>
                <span className={`score-status ${getStatusClass(result.analysis.summary.average_scores.overall)}`}>
                  {getScoreStatus(result.analysis.summary.average_scores.overall)}
                </span>
              </div>

              {/* Stats Grid */}
              <div className="stats-grid">
                <div className="stat-card">
                  <div className="stat-header">
                    <span className="stat-title">Technical SEO</span>
                    <span className="stat-icon">⚙️</span>
                  </div>
                  <div className={`stat-value ${getScoreClass(result.analysis.summary.average_scores.technical_seo)}`}>
                    {result.analysis.summary.average_scores.technical_seo}%
                  </div>
                  <div className="stat-label">Meta tags & structure</div>
                  <div className="stat-progress">
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${result.analysis.summary.average_scores.technical_seo}%` }}></div>
                    </div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <span className="stat-title">Content SEO</span>
                    <span className="stat-icon">📝</span>
                  </div>
                  <div className={`stat-value ${getScoreClass(result.analysis.summary.average_scores.content_seo)}`}>
                    {result.analysis.summary.average_scores.content_seo}%
                  </div>
                  <div className="stat-label">Quality & readability</div>
                  <div className="stat-progress">
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${result.analysis.summary.average_scores.content_seo}%` }}></div>
                    </div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <span className="stat-title">Accessibility</span>
                    <span className="stat-icon">♿</span>
                  </div>
                  <div className={`stat-value ${getScoreClass(result.analysis.summary.average_scores.accessibility)}`}>
                    {result.analysis.summary.average_scores.accessibility}%
                  </div>
                  <div className="stat-label">Alt text & links</div>
                  <div className="stat-progress">
                    <div className="progress-bar">
                      <div className="progress-fill" style={{ width: `${result.analysis.summary.average_scores.accessibility}%` }}></div>
                    </div>
                  </div>
                </div>

                <div className="stat-card">
                  <div className="stat-header">
                    <span className="stat-title">Pages Analyzed</span>
                    <span className="stat-icon">📄</span>
                  </div>
                  <div className="stat-value" style={{ color: 'var(--primary)' }}>
                    {result.analysis.summary.total_pages_analyzed}
                  </div>
                  <div className="stat-label">
                    {result.analysis.broken_links.length} broken link{result.analysis.broken_links.length !== 1 ? 's' : ''}
                  </div>
                </div>
              </div>

              {/* Tabs */}
              <div className="tabs">
                <button className={`tab ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>
                  📊 Overview
                </button>
                <button className={`tab ${activeTab === 'positive' ? 'active' : ''}`} onClick={() => setActiveTab('positive')}>
                  ✨ What's Working Well
                </button>
                <button className={`tab ${activeTab === 'technical' ? 'active' : ''}`} onClick={() => setActiveTab('technical')}>
                  ⚙️ Technical Issues
                </button>
                <button className={`tab ${activeTab === 'content' ? 'active' : ''}`} onClick={() => setActiveTab('content')}>
                  📝 Content Analysis
                </button>
                <button className={`tab ${activeTab === 'pages' ? 'active' : ''}`} onClick={() => setActiveTab('pages')}>
                  📄 Page Details
                </button>
                <button className={`tab ${activeTab === 'ai' ? 'active' : ''}`} onClick={() => setActiveTab('ai')}>
                  🤖 AI Insights
                </button>
              </div>

              {/* Tab Content */}
              {activeTab === 'overview' && <OverviewTab result={result} />}
              {activeTab === 'positive' && <PositiveTab result={result} />}
              {activeTab === 'technical' && <TechnicalTab result={result} />}
              {activeTab === 'content' && <ContentTab result={result} />}
              {activeTab === 'pages' && <PagesTab result={result} getScoreClass={getScoreClass} />}
              {activeTab === 'ai' && <AITab result={result} />}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

// Overview Tab Component
function OverviewTab({ result }) {
  const [expandedIssue, setExpandedIssue] = React.useState(null);
  const summary = result.analysis.summary;
  const pages = result.analysis.pages.filter(p => !p.error);

  // Group pages by issue
  const getPagesByIssue = (issueText) => {
    return pages.filter(page => {
      const allIssues = [...(page.issues || []), ...(page.warnings || [])];
      return allIssues.some(i => i.issue === issueText);
    });
  };

  return (
    <div>
      {/* Summary Statistics */}
      <div className="card">
        <div className="card-header">
          <Icon name="bar-chart" size={20} className="text-secondary" style={{ marginRight: '0.75rem' }} />
          <h3 className="card-title">Summary Statistics</h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(59, 130, 246, 0.1)', color: 'var(--primary)' }}>
                <Icon name="layers" size={24} />
              </div>
              <div>
                <div className="stat-label">Pages Crawled</div>
                <div className="stat-value">{summary.total_pages_crawled}</div>
              </div>
            </div>

            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(16, 185, 129, 0.1)', color: 'var(--success)' }}>
                <Icon name="file-text" size={24} />
              </div>
              <div>
                <div className="stat-label">Pages Analyzed</div>
                <div className="stat-value">{summary.total_pages_analyzed}</div>
              </div>
            </div>

            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(239, 68, 68, 0.1)', color: 'var(--danger)' }}>
                <Icon name="link" size={24} />
              </div>
              <div>
                <div className="stat-label">Broken Links</div>
                <div className="stat-value" style={{ color: summary.total_broken_links > 0 ? 'var(--danger)' : 'inherit' }}>
                  {summary.total_broken_links}
                </div>
              </div>
            </div>

            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(245, 158, 11, 0.1)', color: 'var(--warning)' }}>
                <Icon name="alert-triangle" size={24} />
              </div>
              <div>
                <div className="stat-label">Critical Issues</div>
                <div className="stat-value" style={{ color: summary.total_issues.critical > 0 ? 'var(--warning)' : 'inherit' }}>
                  {summary.total_issues.critical}
                </div>
              </div>
            </div>

            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(107, 114, 128, 0.1)', color: 'var(--gray-600)' }}>
                <Icon name="alert-circle" size={24} />
              </div>
              <div>
                <div className="stat-label">Warnings</div>
                <div className="stat-value">{summary.total_issues.warnings}</div>
              </div>
            </div>

            <div className="stat-item">
              <div className="stat-icon-bg" style={{ background: 'rgba(139, 92, 246, 0.1)', color: 'var(--purple-500, #8b5cf6)' }}>
                <Icon name="activity" size={24} />
              </div>
              <div>
                <div className="stat-label">Health Status</div>
                <div className="stat-value" style={{ textTransform: 'capitalize', fontSize: '1.1rem' }}>
                  {summary.health_status.replace('_', ' ')}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* All Crawled Pages */}
      <div className="card">
        <div className="card-header">
          <Icon name="layers" size={20} className="text-secondary" style={{ marginRight: '0.75rem' }} />
          <h3 className="card-title">All Crawled Pages ({pages.length})</h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {pages.map((page, idx) => (
              <div key={idx} style={{
                padding: '1rem',
                background: 'var(--gray-50)',
                borderRadius: '0.5rem',
                border: '1px solid var(--gray-200)',
                transition: 'all 0.2s ease'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flex: 1, minWidth: 0 }}>
                    <div style={{ padding: '0.25rem', background: 'white', borderRadius: '4px', border: '1px solid var(--gray-200)' }}>
                      <Icon name="file-text" size={16} style={{ color: 'var(--gray-500)' }} />
                    </div>
                    <div style={{ fontSize: '0.95rem', fontWeight: 500, color: 'var(--gray-900)', wordBreak: 'break-all' }}>
                      {page.url}
                    </div>
                  </div>
                  <div style={{ marginLeft: '1rem', whiteSpace: 'nowrap' }}>
                    <span className={`page-score-badge ${getScoreClass(page.overall_score)}`}>{page.overall_score}%</span>
                  </div>
                </div>
                <div className="page-metrics-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))', gap: '1rem', fontSize: '0.8rem' }}>
                  <div className="metric-pill">
                    <span className="metric-label">Technical</span>
                    <span className="metric-value">{page.technical_seo.percentage}%</span>
                  </div>
                  <div className="metric-pill">
                    <span className="metric-label">Content</span>
                    <span className="metric-value">{page.content_seo.percentage}%</span>
                  </div>
                  <div className="metric-pill">
                    <span className="metric-label">Accessibility</span>
                    <span className="metric-value">{page.accessibility.percentage}%</span>
                  </div>
                  <div className="metric-pill" style={{ color: (page.issues?.length || 0) + (page.warnings?.length || 0) > 0 ? 'var(--warning)' : 'var(--gray-600)' }}>
                    <span className="metric-label">Issues</span>
                    <span className="metric-value">{(page.issues?.length || 0) + (page.warnings?.length || 0)}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Common Issues - Clickable */}
      {summary.common_issues && summary.common_issues.length > 0 && (
        <div className="card">
          <div className="card-header">
            <Icon name="alert-triangle" size={20} className="text-secondary" style={{ marginRight: '0.75rem' }} />
            <h3 className="card-title">Most Common Issues</h3>
          </div>
          <div className="card-body">
            <div className="issues-list">
              {summary.common_issues.map((issue, idx) => {
                const affectedPages = getPagesByIssue(issue.issue);
                const isExpanded = expandedIssue === idx;

                return (
                  <div key={idx}>
                    <div
                      className="issue-item issue-warning"
                      style={{ cursor: 'pointer' }}
                      onClick={() => setExpandedIssue(isExpanded ? null : idx)}
                    >
                      <div className="issue-header">
                        <Icon
                          name={isExpanded ? "chevron-down" : "chevron-right"}
                          size={16}
                          style={{ marginRight: '0.5rem', transition: 'transform 0.2s' }}
                        />
                        <Icon name="alert-triangle" size={16} style={{ marginRight: '0.5rem', color: 'var(--warning)' }} />
                        {issue.issue}
                      </div>
                      <div className="issue-body">
                        Found on {issue.count} page{issue.count !== 1 ? 's' : ''} - Click to see details
                      </div>
                    </div>

                    {isExpanded && affectedPages.length > 0 && (
                      <div style={{
                        marginTop: '0.5rem',
                        marginLeft: '1.5rem',
                        padding: '1rem',
                        background: 'var(--gray-50)',
                        borderRadius: '0.375rem',
                        border: '1px solid var(--gray-200)'
                      }}>
                        <div style={{ fontWeight: 600, marginBottom: '0.75rem', fontSize: '0.875rem' }}>
                          Affected Pages:
                        </div>
                        {affectedPages.map((page, pidx) => (
                          <div key={pidx} style={{
                            padding: '0.5rem',
                            marginBottom: '0.5rem',
                            background: 'white',
                            borderRadius: '0.25rem',
                            fontSize: '0.875rem',
                            wordBreak: 'break-all',
                            display: 'flex',
                            alignItems: 'center',
                            gap: '0.5rem'
                          }}>
                            <Icon name="link" size={14} style={{ color: 'var(--gray-400)' }} />
                            <a href={page.url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--primary)', textDecoration: 'none' }}>
                              {page.url}
                            </a>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function getScoreClass(score) {
  if (score >= 80) return 'score-excellent';
  if (score >= 60) return 'score-good';
  if (score >= 40) return 'score-needs-improvement';
  return 'score-poor';
}

// Technical Tab Component
function TechnicalTab({ result }) {
  const pages = result.analysis.pages.filter(p => !p.error);
  const allIssues = pages.flatMap(p => p.issues || []);
  const brokenLinks = result.analysis.broken_links || [];

  return (
    <div>
      {allIssues.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Critical Technical Issues ({allIssues.length})</h3>
          </div>
          <div className="card-body">
            <div className="issues-list">
              {allIssues.map((issue, idx) => (
                <div key={idx} className="issue-item issue-critical">
                  <div className="issue-header">
                    🚨 {issue.issue}
                  </div>
                  <div className="issue-body">
                    <strong>Recommendation:</strong> {issue.recommendation}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {brokenLinks.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Broken Links ({brokenLinks.length})</h3>
          </div>
          <div className="card-body">
            <div className="issues-list">
              {brokenLinks.slice(0, 10).map((link, idx) => (
                <div key={idx} className="issue-item issue-critical">
                  <div className="issue-header">
                    <Icon name="link" size={16} style={{ marginRight: '0.5rem' }} /> {link.url}
                  </div>
                  <div className="issue-body">
                    Status: {link.status_code} | Found on: {link.found_on}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {allIssues.length === 0 && brokenLinks.length === 0 && (
        <div className="card">
          <div className="card-body text-center" style={{ padding: '3rem' }}>
            <Icon name="check-circle" size={48} style={{ color: 'var(--success)', marginBottom: '1rem' }} />
            <h3 style={{ color: 'var(--success)', marginBottom: '0.5rem' }}>No Critical Issues Found</h3>
            <p style={{ color: 'var(--gray-600)' }}>Your website has no critical technical SEO issues.</p>
          </div>
        </div>
      )}
    </div>
  );
}

// Content Tab Component
function ContentTab({ result }) {
  const pages = result.analysis.pages.filter(p => !p.error);
  const firstPage = pages[0];

  if (!firstPage) return <div>No content data available</div>;

  const contentDetails = firstPage.content_seo.details;

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">Content Quality Metrics</h3>
        </div>
        <div className="card-body">
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem' }}>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-600)', marginBottom: '0.25rem' }}>Word Count</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{contentDetails.word_count}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-500)', textTransform: 'capitalize' }}>
                {contentDetails.word_count_status?.replace(/_/g, ' ')}
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-600)', marginBottom: '0.25rem' }}>Readability Score</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{contentDetails.flesch_reading_ease || 'N/A'}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-500)' }}>
                {contentDetails.reading_level || 'N/A'}
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-600)', marginBottom: '0.25rem' }}>Tone</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{contentDetails.tone}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-500)' }}>
                Sentiment: {contentDetails.sentiment_polarity}
              </div>
            </div>
            <div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-600)', marginBottom: '0.25rem' }}>Content Structure</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 700 }}>{contentDetails.total_headings}</div>
              <div style={{ fontSize: '0.75rem', color: 'var(--gray-500)' }}>
                Total headings
              </div>
            </div>
          </div>
        </div>
      </div>

      {contentDetails.top_keywords && contentDetails.top_keywords.length > 0 && (
        <div className="card">
          <div className="card-header">
            <h3 className="card-title">Top Keywords (TF-IDF Analysis)</h3>
          </div>
          <div className="card-body">
            <div className="keywords-container">
              {contentDetails.top_keywords.map((kw, idx) => (
                <div key={idx} className="keyword-tag">
                  {kw.keyword} ({kw.count}x, {kw.density}%)
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// Pages Tab Component
function PagesTab({ result, getScoreClass }) {
  const pages = result.analysis.pages.filter(p => !p.error);

  return (
    <div>
      {pages.map((page, idx) => (
        <div key={idx} className="card">
          <div className="card-header">
            <h3 className="card-title" style={{ fontSize: '0.875rem', wordBreak: 'break-all', flex: 1 }}>
              {page.url}
            </h3>
            <div className={`score-value ${getScoreClass(page.overall_score)}`} style={{ fontSize: '1.5rem', marginLeft: '1rem' }}>
              {page.overall_score}%
            </div>
          </div>
          <div className="card-body">
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <strong>Technical SEO:</strong> {page.technical_seo.percentage}%
              </div>
              <div>
                <strong>Content SEO:</strong> {page.content_seo.percentage}%
              </div>
              <div>
                <strong>Accessibility:</strong> {page.accessibility.percentage}%
              </div>
              <div>
                <strong>Issues:</strong> {(page.issues?.length || 0) + (page.warnings?.length || 0)}
              </div>
            </div>

            {(page.issues?.length > 0 || page.warnings?.length > 0) && (
              <div>
                <div style={{ fontWeight: 600, marginBottom: '0.75rem', fontSize: '0.875rem' }}>Issues & Warnings:</div>
                <div className="issues-list">
                  {page.issues?.map((issue, i) => (
                    <div key={i} className="issue-item issue-critical">
                      <div className="issue-header"><Icon name="alert-triangle" size={16} style={{ marginRight: '0.5rem' }} /> {issue.issue}</div>
                      <div className="issue-body">{issue.recommendation}</div>
                    </div>
                  ))}
                  {page.warnings?.map((warning, i) => (
                    <div key={i} className="issue-item issue-warning">
                      <div className="issue-header"><Icon name="alert-circle" size={16} style={{ marginRight: '0.5rem' }} /> {warning.issue}</div>
                      <div className="issue-body">{warning.recommendation}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}

// AI Tab Component
function AITab({ result }) {
  const advice = result.ai_advice || [];

  const getAdviceClass = (type) => {
    switch (type) {
      case 'critical': return 'issue-critical';
      case 'warning': return 'issue-warning';
      case 'success': return 'issue-success';
      default: return 'issue-info';
    }
  };

  const getAdviceIcon = (type) => {
    switch (type) {
      case 'critical': return <Icon name="alert-triangle" size={16} style={{ marginRight: '0.5rem' }} />;
      case 'warning': return <Icon name="alert-circle" size={16} style={{ marginRight: '0.5rem' }} />;
      case 'success': return <Icon name="check-circle" size={16} style={{ marginRight: '0.5rem' }} />;
      default: return <Icon name="lightbulb" size={16} style={{ marginRight: '0.5rem' }} />;
    }
  };

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">AI-Powered Recommendations</h3>
        </div>
        <div className="card-body">
          {advice.length > 0 ? (
            <div className="issues-list">
              {advice.map((item, idx) => (
                <div key={idx} className={`issue-item ${getAdviceClass(item.type)}`}>
                  <div className="issue-header">
                    {getAdviceIcon(item.type)} {item.category}
                  </div>
                  <div className="issue-body">
                    {item.message}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center" style={{ padding: '2rem', color: 'var(--gray-500)' }}>
              No AI recommendations available
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

// Positive Tab Component
function PositiveTab({ result }) {
  const pages = result.analysis.pages.filter(p => !p.error);
  const allHighlights = pages.flatMap(p => p.positive_highlights || []);

  return (
    <div>
      <div className="card">
        <div className="card-header">
          <h3 className="card-title">✨ What's Working Well</h3>
        </div>
        <div className="card-body">
          {allHighlights.length > 0 ? (
            <div className="issues-list">
              {allHighlights.map((item, idx) => (
                <div key={idx} className="issue-item issue-success">
                  <div className="issue-header">
                    {item.icon} {item.highlight}
                  </div>
                  <div className="issue-body">
                    <strong>{item.category}:</strong> {item.detail}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center" style={{ padding: '3rem' }}>
              <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>💪</div>
              <h3 style={{ color: 'var(--gray-700)', marginBottom: '0.5rem' }}>Keep Improving!</h3>
              <p style={{ color: 'var(--gray-600)' }}>
                As you optimize your website, positive highlights will appear here.
              </p>
            </div>
          )}
        </div>
      </div>

      {allHighlights.length > 0 && (
        <div className="card" style={{ background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)', border: '1px solid #86efac' }}>
          <div className="card-body text-center">
            <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>🎉</div>
            <h3 style={{ color: '#166534', marginBottom: '0.5rem' }}>
              {allHighlights.length} Thing{allHighlights.length !== 1 ? 's' : ''} Working Great!
            </h3>
            <p style={{ color: '#15803d' }}>
              Your website has {allHighlights.length} positive SEO aspect{allHighlights.length !== 1 ? 's' : ''}. Keep up the excellent work!
            </p>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;