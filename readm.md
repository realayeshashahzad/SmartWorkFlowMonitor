# ⚡ NEXUS | Workflow Control Center

A Python and Streamlit dashboard for **executing automation tasks, handling failures with retries, and monitoring every step through live status and detailed execution logs**.

> A workflow isn't complete just because it runs. Understanding and monitoring its execution matters too.

---

## 🔗 Live Demo
[(https://smartworkflowmonitor.streamlit.app/)]
## 📸 Screenshots

| Overview | Execution Logs |
|---|---|
| _Add screenshot_ | _Add screenshot_ |

---

## ✨ Features

- **Task selection:** choose which tasks to include in each workflow run
- **Sequential execution:** tasks run in order with a live pipeline view (Pending → Running → Success / Failed)
- **Automatic retries:** failed tasks are retried with exponential backoff (0.5s, 1s, 2s, up to 4s)
- **Detailed execution logs:** timestamp, task, status, attempt number and message for every event
- **Performance metrics:** total tasks, successful, failed, success rate, retries used and duration
- **Workflow health ring:** at-a-glance success rate for the latest run
- **Run history:** compare runs during a session, with a success-rate trend chart
- **CSV export:** download execution logs and run results
- **Premium dark UI:** custom midnight-purple theme, KPI cards and status badges
- **No API key required:** runs fully locally

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| UI | Streamlit |
| Data handling | Pandas |
| Styling | Custom CSS |

---

## 📁 Project Structure

```
nexus-workflow-control-center/
├── app.py                # Streamlit dashboard (UI)
├── workflow_engine.py    # Task execution, retries and logging
├── requirements.txt      # Dependencies
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/realayeshashahzad/<your-repo-name>.git
cd <your-repo-name>
```

### 2. (Optional) Create a virtual environment

```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS / Linux
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

---

## 🧭 How to Use

1. Open the sidebar and select the tasks you want to run.
2. Set the number of **retry attempts** (extra attempts after the first failure).
3. Click **▶ Execute Workflow** and watch the live pipeline.
4. Review results on **Overview**, inspect events on **Execution Logs**, and compare runs on **Run History**.
5. Export logs or results as CSV when needed.

> Tip: **Simulate Unstable Task** fails randomly on purpose. Use 2-3 retries to see retry handling in action.

---

## ⚙️ How It Works

`WorkflowEngine` runs each task and records structured logs and results.

```
Task starts → Attempt 1
   ├─ success → SUCCESS logged, result saved
   └─ error   → RETRYING logged → wait (exponential backoff) → next attempt
                   └─ attempts exhausted → FAILED logged, result saved
```

**Result fields:** `task`, `status`, `attempts`, `output`, `duration_sec`, `finished_at`
**Log fields:** `timestamp`, `task`, `status`, `attempt`, `message`

### Built-in demo tasks

| Task | Behavior |
|---|---|
| Generate Report | Returns a sample report message |
| Validate Data | Simulates data validation |
| Prepare Notification | Prepares a demo notification (nothing is sent) |
| Simulate Unstable Task | Fails ~70% of the time to demonstrate retries |

---

## 🔮 Future Improvements

- Persistent run history (SQLite)
- Custom task definitions from the UI
- Scheduled workflow runs
- Parallel task execution
- Email / webhook alerts on failure

---

## 👩‍💻 Author

**Ayesha Shahzad**
BS-IT student at Orbit Institute, Lahore, learning AI agents, Python, APIs and automation.

- GitHub: [realayeshashahzad](https://github.com/realayeshashahzad)
- LinkedIn: [Ayesha Shahzad](https://linkedin.com/in/ayesha-shahzad-792501423)

🙏 Thanks to **Sir Iqbal Gill** for his guidance and encouragement.

---

## 📄 License

This project is for educational purposes. Add a license of your choice (for example MIT) if you plan to share it publicly.
