"""NEXUS workflow engine.

Runs local automation tasks sequentially, retries failures with exponential
backoff, and records structured logs and results for the dashboard.
"""

from __future__ import annotations

import time
from datetime import datetime
from typing import Any, Callable, Dict, List

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"


def _now() -> str:
    return datetime.now().strftime(TIME_FORMAT)


class WorkflowEngine:
    """Execute local automation tasks and track their results."""

    BASE_DELAY = 0.5  # seconds before the first retry
    MAX_DELAY = 4.0  # backoff ceiling

    def __init__(self) -> None:
        self.logs: List[Dict[str, Any]] = []
        self.results: List[Dict[str, Any]] = []

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------
    def log(
        self,
        task_name: str,
        status: str,
        message: str,
        attempt: int = 1,
    ) -> Dict[str, Any]:
        """Record a workflow execution event."""
        entry = {
            "timestamp": _now(),
            "task": task_name,
            "status": status,
            "attempt": attempt,
            "message": message,
        }
        self.logs.append(entry)
        return entry

    # ------------------------------------------------------------------
    # Execution
    # ------------------------------------------------------------------
    def _backoff(self, attempt: int) -> float:
        """Exponential backoff: 0.5s, 1s, 2s, 4s (capped)."""
        return min(self.BASE_DELAY * (2 ** (attempt - 1)), self.MAX_DELAY)

    def _build_result(
        self,
        task_name: str,
        status: str,
        attempts: int,
        output: str,
        started: float,
    ) -> Dict[str, Any]:
        return {
            "task": task_name,
            "status": status,
            "attempts": attempts,
            "output": output,
            "duration_sec": round(time.perf_counter() - started, 2),
            "finished_at": _now(),
        }

    def run_task(self, task: Dict[str, Any], retries: int = 2) -> Dict[str, Any]:
        """Run a task and retry it if an error occurs."""
        task_name = task.get("name", "Unnamed Task")
        action: Callable[[], Any] | None = task.get("action")
        max_attempts = max(1, retries + 1)
        started = time.perf_counter()

        self.log(task_name, "RUNNING", "Task execution started.")

        if not callable(action):
            self.log(task_name, "FAILED", "No callable action was provided.")
            result = self._build_result(
                task_name, "FAILED", 0, "Task has no callable action.", started
            )
            self.results.append(result)
            return result

        for attempt in range(1, max_attempts + 1):
            try:
                self.log(
                    task_name,
                    "RUNNING",
                    f"Attempt {attempt} of {max_attempts}",
                    attempt,
                )

                output = action()

                result = self._build_result(
                    task_name, "SUCCESS", attempt, str(output), started
                )
                self.results.append(result)
                self.log(
                    task_name,
                    "SUCCESS",
                    f"Task completed: {output}",
                    attempt,
                )
                return result

            except Exception as error:  # noqa: BLE001 - tasks are user code
                is_last = attempt >= max_attempts
                self.log(
                    task_name,
                    "FAILED" if is_last else "RETRYING",
                    f"{type(error).__name__}: {error}",
                    attempt,
                )
                if not is_last:
                    time.sleep(self._backoff(attempt))

        result = self._build_result(
            task_name,
            "FAILED",
            max_attempts,
            "Task failed after all retry attempts.",
            started,
        )
        self.results.append(result)
        return result

    def run_workflow(
        self, tasks: List[Dict[str, Any]], retries: int = 2
    ) -> List[Dict[str, Any]]:
        """Execute tasks in order and collect their results."""
        return [self.run_task(task, retries) for task in tasks]

    # ------------------------------------------------------------------
    # Reporting
    # ------------------------------------------------------------------
    def get_logs(self) -> List[Dict[str, Any]]:
        """Return all execution logs."""
        return list(self.logs)

    def get_results(self) -> List[Dict[str, Any]]:
        """Return all task results."""
        return list(self.results)

    def get_summary(self) -> Dict[str, Any]:
        """Return workflow execution statistics."""
        total = len(self.results)
        successful = sum(r["status"] == "SUCCESS" for r in self.results)
        failed = sum(r["status"] == "FAILED" for r in self.results)
        retries_used = sum(max(0, r["attempts"] - 1) for r in self.results)
        total_time = sum(r.get("duration_sec", 0) for r in self.results)

        return {
            "total": total,
            "successful": successful,
            "failed": failed,
            "success_rate": round(successful / total * 100, 2) if total else 0,
            "retries_used": retries_used,
            "total_duration_sec": round(total_time, 2),
        }

    def reset(self) -> None:
        """Clear all logs and results."""
        self.logs.clear()
        self.results.clear()