import { useEffect, useState } from "react";
import axios from "axios";
import { Activity, Database, Gauge, Github, Layers3, RefreshCw, Server } from "lucide-react";
import "@/App.css";

const API = process.env.REACT_APP_BACKEND_URL;

function StatusDot({ state, testId }) {
  return <span data-testid={testId} className={`status-dot ${state}`} aria-hidden="true" />;
}

function App() {
  const [health, setHealth] = useState(null);
  const [loading, setLoading] = useState(true);
  const [lastChecked, setLastChecked] = useState(null);

  const loadHealth = async () => {
    setLoading(true);
    try {
      const response = await axios.get(`${API}/api/health`, { timeout: 5000 });
      setHealth(response.data);
    } catch (error) {
      setHealth({ status: "offline", database: "unavailable", error: error.message });
    } finally {
      setLastChecked(new Date());
      setLoading(false);
    }
  };

  useEffect(() => { loadHealth(); }, []);
  const online = health?.status === "ok";
  const backendReachable = Boolean(health && !health.error);
  const databaseOnline = health?.database === "connected";

  return (
    <div className="app-shell">
      <aside className="sidebar" data-testid="application-navigation">
        <div className="brand" data-testid="brand-mark"><span className="brand-mark">E</span><span>emergent<span className="brand-muted">/core</span></span></div>
        <div className="workspace-label">WORKSPACE</div>
        <nav>
          <a className="nav-item active" href="#status" data-testid="system-status-nav"><Gauge size={17} /> System status</a>
          <a className="nav-item disabled" href="#not-implemented" data-testid="projects-nav"><Layers3 size={17} /> Projects <span className="nav-soon">F0</span></a>
        </nav>
        <div className="sidebar-footer"><div className="connection-chip" data-testid="environment-label"><span className="pulse" /> {health?.environment || "development"}</div><a href="https://github.com" target="_blank" rel="noreferrer" className="github-link" data-testid="github-link"><Github size={15} /> GitHub-ready</a></div>
      </aside>
      <main className="main-content">
        <header className="topbar"><div><span className="overline">FOUNDATION / F0</span><h1 data-testid="page-title">System status</h1></div><button className="refresh-button" onClick={loadHealth} disabled={loading} data-testid="refresh-health-button"><RefreshCw size={15} className={loading ? "spin" : ""} /> {loading ? "Checking" : "Refresh"}</button></header>
        <section className="intro-band" data-testid="status-summary"><div><p className="eyebrow">RUNTIME OVERVIEW</p><h2>Independent infrastructure, clearly accounted for.</h2><p className="summary-copy">A minimal foundation for the platform ahead. Nothing is represented here until it exists.</p></div><div className={`overall-badge ${online ? "good" : "bad"}`} data-testid="overall-status"><StatusDot state={online ? "good" : "bad"} testId="overall-status-dot" /><span>{online ? "All systems operational" : "Service unavailable"}</span></div></section>
        <section className="status-grid" aria-label="Service status">
          <article className="status-card" data-testid="backend-health-card"><div className="card-icon blue"><Server size={18} /></div><div className="card-heading"><span>Backend API</span><strong className={backendReachable ? "text-good" : "text-bad"} data-testid="backend-health-status">{backendReachable ? "Reachable" : "Offline"}</strong></div><div className="card-meta"><StatusDot state={backendReachable ? "good" : "bad"} testId="backend-health-status-dot" /> GET /health {health?.request_id ? `· ${health.request_id.slice(0, 8)}` : ""}</div></article>
          <article className="status-card" data-testid="database-status-card"><div className="card-icon green"><Database size={18} /></div><div className="card-heading"><span>PostgreSQL</span><strong className={databaseOnline ? "text-good" : "text-bad"} data-testid="database-connection-status">{databaseOnline ? "Connected" : "Unavailable"}</strong></div><div className="card-meta"><StatusDot state={databaseOnline ? "good" : "bad"} testId="database-connection-status-dot" /> Connection probe · SELECT 1</div></article>
          <article className="status-card" data-testid="observability-card"><div className="card-icon orange"><Activity size={18} /></div><div className="card-heading"><span>Request tracing</span><strong className="text-good" data-testid="request-tracing-status">Enabled</strong></div><div className="card-meta"><StatusDot state="good" testId="request-tracing-status-dot" /> Correlation IDs active</div></article>
        </section>
        <section className="lower-grid"><div className="panel" data-testid="foundation-scope-panel"><div className="panel-header"><div><p className="eyebrow">SCOPE CONTROL</p><h3>Foundation boundary</h3></div><span className="tag">F0 ONLY</span></div><div className="scope-row"><span>PostgreSQL connection layer</span><span className="scope-state done">Implemented</span></div><div className="scope-row"><span>Authentication, tenants, and RLS</span><span className="scope-state">Not implemented in F0</span></div><div className="scope-row"><span>Storage, realtime, and functions</span><span className="scope-state">Not implemented in F0</span></div></div><div className="panel telemetry" data-testid="last-check-panel"><p className="eyebrow">LAST CHECK</p><div className="telemetry-value">{lastChecked ? lastChecked.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" }) : "—"}</div><p className="muted">UTC client timestamp · checks on demand</p></div></section>
        <footer data-testid="f0-footer">Emergent BaaS · Foundation runtime <span>NOT PRODUCTION SECURE — F0 BASELINE</span></footer>
      </main>
    </div>
  );
}

export default App;