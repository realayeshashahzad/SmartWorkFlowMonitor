import html
import random
import time

import pandas as pd
import streamlit as st

from workflow_engine import WorkflowEngine


# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="NEXUS | Workflow Control Center",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==================================================
# PREMIUM MIDNIGHT PURPLE THEME
# ==================================================
CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg: #0E0B1C;
    --panel: #171128;
    --panel-2: #1F1735;
    --border: #35264D;
    --border-soft: #2A1F3D;
    --purple: #A78BFA;
    --violet: #8B5CF6;
    --lavender: #C4B5FD;
    --mint: #34D399;
    --amber: #FBBF24;
    --red: #FB7185;
    --text: #F5F3FF;
    --muted: #A99ABD;
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(ellipse at 90% -5%, rgba(139,92,246,.18), transparent 40%),
        radial-gradient(ellipse at -5% 105%, rgba(109,40,217,.12), transparent 40%),
        #0E0B1C;
    color: var(--text);
}

.block-container { max-width: 1480px; padding-top: 1.4rem; padding-bottom: 2rem; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #140F25 0%, #0F0B1E 100%);
    border-right: 1px solid var(--border-soft);
}
section[data-testid="stSidebar"] > div { padding-top: 1.3rem; }
section[data-testid="stSidebar"] h5 {
    font-size: 10.5px; letter-spacing: 1.8px; color: #8D7BAF !important;
    font-weight: 700; margin: 4px 0 6px;
}

/* Typography */
h1, h2, h3 { color: var(--text) !important; letter-spacing: -0.5px; }
h3 { font-size: 20px !important; font-weight: 700 !important; }
p, label, .stMarkdown { color: #DDD6F3; }

/* Brand */
.brand { display:flex; align-items:center; gap:13px; padding: 2px 0 18px; }
.brand-icon {
    width:46px; height:46px; border-radius:14px; display:flex;
    align-items:center; justify-content:center; font-size:23px;
    background: linear-gradient(135deg, #8B5CF6, #5B21B6);
    box-shadow: 0 6px 24px rgba(139,92,246,.35), inset 0 1px 0 rgba(255,255,255,.25);
}
.brand-title { font-size:24px; font-weight:800; color:#fff; letter-spacing:3px; line-height:1.1; }
.brand-subtitle { font-size:9.5px; color:#B9A4E7; letter-spacing:2.4px; margin-top:5px; }

/* Hero */
.hero {
    position: relative; overflow: hidden;
    background: linear-gradient(120deg, #231538 0%, #36205A 55%, #261E52 100%);
    border: 1px solid #4E3672; border-radius: 22px;
    padding: 30px 32px; margin-bottom: 22px;
    box-shadow: 0 18px 50px rgba(0,0,0,.28);
}
.hero::after {
    content:""; position:absolute; right:-80px; top:-80px; width:300px; height:300px;
    background: radial-gradient(circle, rgba(167,139,250,.28), transparent 65%);
}
.hero-top { display:flex; justify-content:space-between; align-items:flex-start; gap:20px; position:relative; z-index:1; }
.hero-label {
    display:inline-block; color:#D8C9FF; background: rgba(167,139,250,.13);
    border:1px solid #60418A; border-radius:20px; padding:6px 12px;
    font-size:10.5px; letter-spacing:1.4px; font-weight:600; margin-bottom:14px;
}
.hero h1 { font-size:34px; font-weight:800; margin:0 0 10px; color:#fff !important; }
.hero p { color:#D4C6EC; font-size:14px; line-height:1.75; margin:0; max-width:640px; }
.hero-chips { display:flex; gap:10px; flex-wrap:wrap; margin-top:20px; position:relative; z-index:1; }
.chip {
    background: rgba(14,11,28,.45); border:1px solid #5A4380; color:#E6DCFF;
    padding:7px 13px; border-radius:10px; font-size:12px; font-weight:500;
    backdrop-filter: blur(6px);
}
.chip b { color:#fff; }

/* Live dot */
.live-dot {
    display:inline-block; width:8px; height:8px; border-radius:50%;
    background: var(--mint); margin-right:8px; box-shadow:0 0 0 0 rgba(52,211,153,.6);
    animation: pulse 2s infinite;
}
@keyframes pulse {
    0% { box-shadow:0 0 0 0 rgba(52,211,153,.55); }
    70% { box-shadow:0 0 0 9px rgba(52,211,153,0); }
    100% { box-shadow:0 0 0 0 rgba(52,211,153,0); }
}

/* KPI cards */
.kpi {
    position:relative; overflow:hidden;
    background: linear-gradient(150deg, #231A38, #171128);
    border:1px solid var(--border); border-radius:18px; padding:20px 22px;
    box-shadow: 0 10px 30px rgba(0,0,0,.18);
    transition: transform .2s ease, border-color .2s ease;
}
.kpi:hover { transform: translateY(-3px); border-color: #6B4FA0; }
.kpi::before {
    content:""; position:absolute; left:0; top:0; bottom:0; width:3px;
    background: var(--accent, #A78BFA);
}
.kpi-top { display:flex; justify-content:space-between; align-items:center; }
.kpi-label { color:#B9A9D3; font-size:12px; font-weight:600; letter-spacing:.6px; text-transform:uppercase; }
.kpi-icon {
    width:32px; height:32px; border-radius:10px; display:flex; align-items:center;
    justify-content:center; font-size:15px; background: rgba(167,139,250,.12);
}
.kpi-value { font-size:34px; font-weight:800; color:#fff; margin-top:10px; letter-spacing:-1px; }
.kpi-sub { color:#8D7BAF; font-size:11.5px; margin-top:2px; }

/* Panels */
.panel {
    background: linear-gradient(160deg, #1C1430, #151024);
    border:1px solid var(--border); border-radius:18px; padding:22px;
    box-shadow: 0 10px 30px rgba(0,0,0,.15);
}
.panel-title { font-size:15px; font-weight:700; color:#fff; margin-bottom:3px; }
.panel-sub { font-size:12px; color:#8D7BAF; margin-bottom:16px; }

/* Success ring */
.ring-wrap { display:flex; align-items:center; gap:22px; }
.ring {
    width:118px; height:118px; border-radius:50%; flex-shrink:0;
    display:flex; align-items:center; justify-content:center;
    background: conic-gradient(var(--ring-color, #34D399) calc(var(--pct) * 1%), #2B2040 0);
}
.ring-inner {
    width:90px; height:90px; border-radius:50%; background:#171128;
    display:flex; flex-direction:column; align-items:center; justify-content:center;
}
.ring-pct { font-size:24px; font-weight:800; color:#fff; line-height:1; }
.ring-lbl { font-size:9.5px; color:#8D7BAF; letter-spacing:1.2px; margin-top:4px; }
.ring-stats div { font-size:13px; color:#CFC3E8; margin:5px 0; }
.ring-stats b { color:#fff; }

/* Pipeline */
.pipe { display:flex; flex-direction:column; gap:10px; }
.step {
    display:flex; align-items:center; gap:14px;
    background:#1B1330; border:1px solid var(--border-soft);
    border-radius:14px; padding:13px 16px;
}
.step.running { border-color:#8B5CF6; box-shadow:0 0 0 1px rgba(139,92,246,.35), 0 0 24px rgba(139,92,246,.15); }
.step.success { border-color: rgba(52,211,153,.35); }
.step.failed { border-color: rgba(251,113,133,.4); }
.step-num {
    width:30px; height:30px; border-radius:9px; background:#2A1F42; color:#C4B5FD;
    display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700;
}
.step-name { flex:1; font-weight:600; color:#F1ECFF; font-size:14px; }
.step-meta { font-weight:400; color:#8D7BAF; font-size:11.5px; margin-top:3px; font-family:'JetBrains Mono', monospace; }

/* Badges */
.badge {
    display:inline-block; padding:4px 11px; border-radius:20px;
    font-size:10.5px; font-weight:700; letter-spacing:.8px;
}
.b-success { color:#34D399; background:rgba(52,211,153,.12); border:1px solid rgba(52,211,153,.3); }
.b-failed { color:#FB7185; background:rgba(251,113,133,.12); border:1px solid rgba(251,113,133,.3); }
.b-running { color:#C4B5FD; background:rgba(139,92,246,.18); border:1px solid rgba(167,139,250,.4); }
.b-pending { color:#A99ABD; background:rgba(169,154,189,.1); border:1px solid rgba(169,154,189,.25); }

/* Empty state */
.empty {
    text-align:center; padding:38px 20px; border:1px dashed #44325F;
    border-radius:16px; background: rgba(31,23,53,.4);
}
.empty-icon { font-size:30px; margin-bottom:8px; }
.empty-title { color:#EDE7FF; font-weight:700; font-size:15px; }
.empty-text { color:#8D7BAF; font-size:12.5px; margin-top:5px; line-height:1.6; }

/* Buttons */
.stButton > button, .stDownloadButton > button {
    border-radius:11px; min-height:44px; font-weight:600;
    border:1px solid #584071; background:#221A36; color:#F5F3FF;
    transition: all .2s ease;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(110deg, #8B5CF6, #6D28D9); color:#fff;
    border:1px solid #A78BFA; box-shadow: 0 6px 20px rgba(139,92,246,.30);
}
.stButton > button:hover, .stDownloadButton > button:hover {
    border-color:#C4B5FD; color:#fff; transform: translateY(-1px);
}

/* Inputs */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div {
    background:#1A1330; border-color:#43315A; border-radius:11px;
}
div[data-baseweb="popover"] { background:#211936; }
span[data-baseweb="tag"] { background:#34236A !important; border-radius:8px !important; }

/* Tables */
div[data-testid="stDataFrame"] {
    border:1px solid var(--border); border-radius:14px; overflow:hidden;
}

/* Progress */
div[data-testid="stProgressBar"] > div { background:#2B2040; border-radius:20px; }
div[data-testid="stProgressBar"] > div > div {
    background: linear-gradient(90deg, #8B5CF6, #C4B5FD); border-radius:20px;
}

div[data-testid="stAlert"] { border-radius:12px; }
hr { border-color:#2A1F3D; margin:1.3rem 0; }
div[data-testid="stCaptionContainer"] { color:#8D7BAF; }

.section-tag {
    color:#A78BFA; font-size:10.5px; font-weight:700; letter-spacing:2px;
    text-transform:uppercase; margin-bottom:4px;
}

.footer { text-align:center; padding:16px 5px 4px; color:#7D6C9F; font-size:12px; line-height:1.8; }

#MainMenu, footer, header[data-testid="stHeader"] { visibility:hidden; }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


# ==================================================
# UI HELPERS
# ==================================================
def h(text):
    return html.escape(str(text))


def compact(markup):
    """Strip indentation so Markdown never turns HTML into a code block."""
    return "".join(line.strip() for line in markup.splitlines())


def badge(state):
    labels = {
        "success": ("SUCCESS", "b-success"),
        "failed": ("FAILED", "b-failed"),
        "running": ("RUNNING", "b-running"),
        "pending": ("PENDING", "b-pending"),
    }
    text, cls = labels[state]
    return f'<span class="badge {cls}">{text}</span>'


def result_state(result):
    """Normalise a task result into 'success' or 'failed'."""
    raw = str(result.get("status", "")).upper()
    if raw:
        return "success" if raw in ("SUCCESS", "COMPLETED", "OK", "PASSED") else "failed"
    if "success" in result:
        return "success" if result["success"] else "failed"
    return "failed"


def kpi_card(label, value, sub, icon, accent):
    return compact(
        f"""
        <div class="kpi" style="--accent:{accent};">
            <div class="kpi-top">
                <div class="kpi-label">{h(label)}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            <div class="kpi-value">{h(value)}</div>
            <div class="kpi-sub">{h(sub)}</div>
        </div>
        """
    )


def empty_state(icon, title, text):
    st.markdown(
        compact(
            f"""
            <div class="empty">
                <div class="empty-icon">{icon}</div>
                <div class="empty-title">{h(title)}</div>
                <div class="empty-text">{h(text)}</div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


def pipeline_html(names, states, details=None):
    details = details or {}
    rows = ""
    for i, name in enumerate(names):
        state = states.get(name, "pending")
        meta = (
            f'<div class="step-meta">{h(details[name])}</div>'
            if name in details
            else ""
        )
        rows += (
            f'<div class="step {state}">'
            f'<div class="step-num">{i + 1}</div>'
            f'<div class="step-name">{h(name)}{meta}</div>'
            f"{badge(state)}</div>"
        )
    return f'<div class="pipe">{rows}</div>'


def style_status_table(df):
    """Colour a 'status' column if one exists."""
    if "status" not in df.columns:
        return df

    palette = {
        "SUCCESS": "color:#34D399;font-weight:700",
        "FAILED": "color:#FB7185;font-weight:700",
        "RETRYING": "color:#FBBF24;font-weight:700",
        "RUNNING": "color:#C4B5FD;font-weight:700",
    }

    def colour(value):
        return palette.get(str(value).upper(), "")

    return df.style.map(colour, subset=["status"])


def show_table(df):
    """Render a results/log table with clean labels and coloured status."""
    config = {
        "task": st.column_config.TextColumn("Task", width="medium"),
        "status": st.column_config.TextColumn("Status", width="small"),
        "attempts": st.column_config.NumberColumn("Attempts", width="small", format="%d"),
        "attempt": st.column_config.NumberColumn("Attempt", width="small", format="%d"),
        "duration_sec": st.column_config.NumberColumn("Duration (s)", width="small", format="%.2f"),
        "output": st.column_config.TextColumn("Output", width="large"),
        "message": st.column_config.TextColumn("Message", width="large"),
        "finished_at": st.column_config.TextColumn("Finished At", width="medium"),
        "timestamp": st.column_config.TextColumn("Timestamp", width="medium"),
    }
    config = {key: value for key, value in config.items() if key in df.columns}

    st.dataframe(
        style_status_table(df),
        use_container_width=True,
        hide_index=True,
        column_config=config,
    )


# ==================================================
# SESSION STATE
# ==================================================
if "workflow_history" not in st.session_state:
    st.session_state.workflow_history = []

if "run_count" not in st.session_state:
    st.session_state.run_count = 0


# ==================================================
# TASK DEFINITIONS
# ==================================================
def generate_report():
    time.sleep(0.4)
    return "Sample report generated successfully"


def validate_data():
    time.sleep(0.3)
    return "Data validation completed successfully"


def prepare_notification():
    time.sleep(0.3)
    return "Demo notification prepared (not sent)"


def simulate_unstable_task():
    time.sleep(0.3)

    if random.random() < 0.7:
        raise RuntimeError("Simulated temporary service error")

    return "Task recovered successfully"


TASKS = {
    "Generate Report": generate_report,
    "Validate Data": validate_data,
    "Prepare Notification": prepare_notification,
    "Simulate Unstable Task": simulate_unstable_task,
}


# ==================================================
# SIDEBAR
# ==================================================
with st.sidebar:
    st.markdown(
        compact(
            """
            <div class="brand">
                <div class="brand-icon">⚡</div>
                <div>
                    <div class="brand-title">NEXUS</div>
                    <div class="brand-subtitle">WORKFLOW CONTROL</div>
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    st.markdown("##### NAVIGATION")

    page = st.radio(
        "Navigation",
        ["Overview", "Execution Logs", "Run History"],
        label_visibility="collapsed",
    )

    st.divider()

    st.markdown("##### WORKFLOW CONFIGURATION")

    selected_tasks = st.multiselect(
        "Select tasks",
        options=list(TASKS.keys()),
        default=["Generate Report", "Validate Data", "Prepare Notification"],
    )

    retries = st.slider(
        "Retry attempts",
        min_value=0,
        max_value=5,
        value=2,
        help="Extra attempts after the initial failure.",
    )

    st.caption(f"{len(selected_tasks)} task(s) selected · {retries} retries each")

    st.divider()

    run_workflow = st.button(
        "▶  Execute Workflow", type="primary", use_container_width=True
    )

    clear_history = st.button("Clear Session History", use_container_width=True)

    st.divider()

    st.markdown("##### SYSTEM STATUS")

    st.markdown(
        compact(
            """
            <div style="background:#1D1534;border:1px solid #432E66;padding:14px;border-radius:14px;">
                <div style="color:#34D399;font-size:12px;font-weight:600;">
                    <span class="live-dot"></span>LOCAL ENGINE READY
                </div>
                <div style="color:#A99ABD;font-size:11px;margin-top:9px;line-height:1.9;">
                    Python Runtime<br>Sequential Execution<br>No API Key Required
                </div>
            </div>
            """
        ),
        unsafe_allow_html=True,
    )


# ==================================================
# CLEAR HISTORY
# ==================================================
if clear_history:
    st.session_state.workflow_history = []
    st.session_state.run_count = 0
    st.rerun()


# ==================================================
# EXECUTE WORKFLOW
# ==================================================
if run_workflow:
    if not selected_tasks:
        st.warning("Select at least one task before execution.")

    else:
        engine = WorkflowEngine()

        st.session_state.run_count += 1
        run_number = st.session_state.run_count

        results = []
        states = {}

        st.markdown(
            '<div class="section-tag">LIVE EXECUTION</div>',
            unsafe_allow_html=True,
        )
        st.markdown(f"### Run #{run_number} in progress")

        progress = st.progress(0)
        details = {}
        pipe_box = st.empty()
        pipe_box.markdown(
            pipeline_html(selected_tasks, states, details), unsafe_allow_html=True
        )

        for index, task_name in enumerate(selected_tasks):
            states[task_name] = "running"
            pipe_box.markdown(
                pipeline_html(selected_tasks, states, details),
                unsafe_allow_html=True,
            )

            result = engine.run_task(
                {"name": task_name, "action": TASKS[task_name]},
                retries=retries,
            )

            results.append(result)
            states[task_name] = result_state(result)

            attempts = result.get("attempts", 1)
            details[task_name] = (
                f"{attempts} attempt{'s' if attempts != 1 else ''} · "
                f"{result.get('duration_sec', 0):.2f}s · "
                f"{result.get('output', '')}"
            )

            pipe_box.markdown(
                pipeline_html(selected_tasks, states, details),
                unsafe_allow_html=True,
            )
            progress.progress((index + 1) / len(selected_tasks))

        st.session_state.workflow_history.append(
            {
                "run": run_number,
                "results": results,
                "summary": engine.get_summary(),
                "logs": engine.get_logs(),
            }
        )

        if engine.get_summary()["failed"] == 0:
            st.success(f"Run #{run_number} finished. All selected tasks completed successfully.")
        else:
            st.warning(
                f"Run #{run_number} finished. Some tasks failed after retry "
                "attempts. Review the execution logs."
            )

        st.divider()


# ==================================================
# CURRENT DATA
# ==================================================
history = st.session_state.workflow_history

if history:
    latest = history[-1]
    summary = latest["summary"]
    results = latest["results"]
    logs = latest["logs"]
else:
    summary = {"total": 0, "successful": 0, "failed": 0, "success_rate": 0}
    results = []
    logs = []


# ==================================================
# HERO
# ==================================================
last_run_text = f"Run #{history[-1]['run']}" if history else "No runs yet"

st.markdown(
    compact(
        f"""
        <div class="hero">
            <div class="hero-top">
                <div>
                    <div class="hero-label">⚡ WORKFLOW INTELLIGENCE PLATFORM</div>
                    <h1>Automation Overview</h1>
                    <p>
                        Your central workspace to execute tasks, monitor outcomes,
                        inspect failures, and track workflow performance in real time.
                    </p>
                </div>
            </div>
            <div class="hero-chips">
                <div class="chip"><span class="live-dot"></span><b>Engine</b> online</div>
                <div class="chip"><b>Latest</b> · {h(last_run_text)}</div>
                <div class="chip"><b>Session runs</b> · {len(history)}</div>
                <div class="chip"><b>Queue</b> · {len(selected_tasks)} task(s)</div>
            </div>
        </div>
        """
    ),
    unsafe_allow_html=True,
)


# ==================================================
# OVERVIEW PAGE
# ==================================================
if page == "Overview":

    st.markdown('<div class="section-tag">REAL-TIME VIEW</div>', unsafe_allow_html=True)
    st.subheader("Execution Metrics")

    rate = float(summary["success_rate"])

    c1, c2, c3, c4 = st.columns(4)
    c1.markdown(
        kpi_card("Total Tasks", summary["total"], "In latest run", "📋", "#A78BFA"),
        unsafe_allow_html=True,
    )
    c2.markdown(
        kpi_card("Successful", summary["successful"], "Completed cleanly", "✅", "#34D399"),
        unsafe_allow_html=True,
    )
    c3.markdown(
        kpi_card("Failed", summary["failed"], "After all retries", "⚠️", "#FB7185"),
        unsafe_allow_html=True,
    )
    c4.markdown(
        kpi_card("Success Rate", f"{rate:.1f}%", "Latest workflow run", "📈", "#C4B5FD"),
        unsafe_allow_html=True,
    )

    st.write("")

    left, right = st.columns([1.55, 1])

    with left:
        st.subheader("Task Execution Results")

        if results:
            show_table(pd.DataFrame(results))
        else:
            empty_state(
                "🚀",
                "No executions yet",
                "Choose tasks in the sidebar and press Execute Workflow "
                "to see results here.",
            )

    with right:
        st.subheader("Workflow Health")

        if summary["total"] > 0:
            ring_color = "#34D399" if summary["failed"] == 0 else "#FBBF24"
            st.markdown(
                compact(
                    f"""
                    <div class="panel">
                        <div class="ring-wrap">
                            <div class="ring" style="--pct:{rate:.0f};--ring-color:{ring_color};">
                                <div class="ring-inner">
                                    <div class="ring-pct">{rate:.0f}%</div>
                                    <div class="ring-lbl">HEALTH</div>
                                </div>
                            </div>
                            <div class="ring-stats">
                                <div><b>{summary['successful']} / {summary['total']}</b> tasks successful</div>
                                <div>{badge('success') if summary['failed'] == 0 else badge('failed')}</div>
                                <div style="color:#8D7BAF;font-size:12px;">
                                    {'All tasks passed.' if summary['failed'] == 0 else str(summary['failed']) + ' task(s) failed.'}
                                </div>
                            </div>
                        </div>
                    </div>
                    """
                ),
                unsafe_allow_html=True,
            )
        else:
            empty_state(
                "🩺",
                "Health unavailable",
                "Health information appears after your first run.",
            )

        st.write("")
        st.markdown(
            compact(
                f"""
                <div class="panel">
                    <div class="panel-title">Current Settings</div>
                    <div class="panel-sub">Configured from the sidebar</div>
                    <div class="ring-stats">
                        <div>Tasks selected · <b>{len(selected_tasks)}</b></div>
                        <div>Retries per task · <b>{retries}</b></div>
                        <div>Session runs · <b>{len(history)}</b></div>
                    </div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

    st.write("")
    st.subheader("Recent Activity")

    if logs:
        recent_logs = pd.DataFrame(logs).tail(6).iloc[::-1]
        show_table(recent_logs)
    else:
        empty_state(
            "🕑",
            "Nothing to show yet",
            "Recent task activity will appear here after a run.",
        )


# ==================================================
# EXECUTION LOGS PAGE
# ==================================================
elif page == "Execution Logs":

    st.markdown('<div class="section-tag">OBSERVABILITY</div>', unsafe_allow_html=True)
    st.subheader("Execution Logs")
    st.caption("Inspect task events, retry attempts, and failure messages.")

    if logs:
        log_df = pd.DataFrame(logs)

        retry_events = int((log_df["status"] == "RETRYING").sum())
        failed_events = int((log_df["status"] == "FAILED").sum())

        m1, m2, m3 = st.columns(3)
        m1.markdown(
            kpi_card("Total Events", len(log_df), "Logged in latest run", "🧾", "#A78BFA"),
            unsafe_allow_html=True,
        )
        m2.markdown(
            kpi_card("Retries Triggered", retry_events, "Recovered or exhausted", "🔁", "#FBBF24"),
            unsafe_allow_html=True,
        )
        m3.markdown(
            kpi_card("Final Failures", failed_events, "After all attempts", "⛔", "#FB7185"),
            unsafe_allow_html=True,
        )

        st.write("")

        f1, f2 = st.columns([1, 3])
        with f1:
            chosen_status = st.selectbox(
                "Filter by status",
                ["ALL", "RUNNING", "RETRYING", "SUCCESS", "FAILED"],
            )

        filtered = log_df.copy()
        if chosen_status != "ALL" and "status" in filtered.columns:
            filtered = filtered[filtered["status"] == chosen_status]

        st.caption(f"Showing {len(filtered)} of {len(log_df)} events")

        show_table(filtered)

        st.download_button(
            "⬇ Export Execution Logs",
            data=log_df.to_csv(index=False).encode("utf-8"),
            file_name="nexus_execution_logs.csv",
            mime="text/csv",
        )
    else:
        empty_state(
            "📜",
            "No logs available",
            "Execute a workflow to generate logs.",
        )


# ==================================================
# RUN HISTORY PAGE
# ==================================================
elif page == "Run History":

    st.markdown('<div class="section-tag">EXECUTION RECORDS</div>', unsafe_allow_html=True)
    st.subheader("Workflow Run History")
    st.caption("Review workflow executions recorded during this session.")

    if history:
        rows = []
        for item in history:
            data = item["summary"]
            rows.append(
                {
                    "Run": item["run"],
                    "Total Tasks": data["total"],
                    "Successful": data["successful"],
                    "Failed": data["failed"],
                    "Success Rate": f"{data['success_rate']:.1f}%",
                }
            )

        history_df = pd.DataFrame(rows)

        if len(history) > 1:
            trend = pd.DataFrame(
                {
                    "Run": [f"#{item['run']}" for item in history],
                    "Success rate (%)": [
                        float(item["summary"]["success_rate"]) for item in history
                    ],
                }
            ).set_index("Run")

            st.markdown("##### SUCCESS RATE TREND")
            st.area_chart(trend, color="#A78BFA", height=220)

        st.dataframe(history_df, use_container_width=True, hide_index=True)

        all_results = []
        for item in history:
            for result in item["results"]:
                row = result.copy()
                row["run"] = item["run"]
                all_results.append(row)

        st.download_button(
            "⬇ Export All Run Results",
            data=pd.DataFrame(all_results).to_csv(index=False).encode("utf-8"),
            file_name="nexus_run_history.csv",
            mime="text/csv",
        )

    else:
        empty_state(
            "🗂️",
            "No previous runs",
            "Execute your first workflow to start building a session history.",
        )


# ==================================================
# FOOTER
# ==================================================
st.markdown(
    compact(
        """
        <hr>
        <div class="footer">
            <b style="color:#C4B5FD;letter-spacing:1px;">NEXUS · SMART WORKFLOW MONITOR</b><br>
            Built with Python and Streamlit<br>
            Local educational automation demo · No external AI model
        </div>
        """
    ),
    unsafe_allow_html=True,
)