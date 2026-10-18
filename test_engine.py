
from workflow_engine import WorkflowEngine


engine = WorkflowEngine()


def successful_task():
    return "Report generated successfully"


def failing_task():
    raise ValueError("Simulated task failure")


tasks = [
    {
        "name": "Generate Report",
        "action": successful_task,
    },
    {
        "name": "Test Failure Handling",
        "action": failing_task,
    },
]

results = engine.run_workflow(tasks, retries=2)

print("\nWORKFLOW RESULTS")
for result in results:
    print(result)

print("\nSUMMARY")
print(engine.get_summary())

print("\nEXECUTION LOGS")
for log in engine.get_logs():
    print(log)
