import base64
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

module_dir = Path(__file__).resolve().parent
repo_root = module_dir.parents[3]
project_env_path = module_dir.parent.parent / ".env"
legacy_env_path = module_dir.parent / ".env"
repo_env_path = repo_root / ".env"
for env_path in (repo_env_path, project_env_path, legacy_env_path):
    if env_path.exists():
        load_dotenv(env_path)

# Message timeout: agentic tasks can run 10–60+ min. Default 1 hour.
MESSAGE_TIMEOUT = int(os.getenv("OPENCODE_MESSAGE_TIMEOUT", "3600"))


class OpenCodeClient:
    """HTTP client for the OpenCode server.

    Supports both the classic flat API (v1: /session, /session/:id/message)
    and the prefix-routed v2 API (everything under /api/..., prompt via
    POST /session/:id/prompt, responses wrapped in {"data": ...}).

    Set OPENCODE_BASE_URL / OPENCODE_API_URL to e.g. http://localhost:4096/api
    on v2 servers; the paths below are appended to it unchanged.
    """

    def __init__(self):
        self.base_url = os.getenv("OPENCODE_BASE_URL") or os.getenv("OPENCODE_API_URL") or "http://localhost:4096"
        self.username = os.getenv("OPENCODE_USERNAME", "opencode")
        self.password = os.getenv("OPENCODE_PASSWORD")

        self.headers = {}
        if self.password:
            credentials = f"{self.username}:{self.password}"
            encoded = base64.b64encode(credentials.encode()).decode()
            self.headers = {"Authorization": f"Basic {encoded}"}
        # API mode: v2 servers mount everything under /api/..., flat paths
        # only serve the web UI (SPA catch-all).
        self._api_mode = "v2" if self.base_url.rstrip("/").endswith("/api") else "v1"
        # Timestamp (ms) of the last send_message; used by wait_for_session_complete
        # to detect a *new* v2 idle event rather than one from a previous prompt.
        self._last_send_time_ms = 0

    @staticmethod
    def _unwrap(payload):
        """v2 responses wrap payloads as {"location": ..., "data": ...}."""
        if isinstance(payload, dict) and "data" in payload:
            return payload["data"]
        return payload

    def _url(self, path):
        return f"{self.base_url}{path}"

    def list_sessions(self):
        """GET /session - list all sessions."""
        try:
            response = requests.get(self._url("/session"), headers=self.headers, timeout=30)
            response.raise_for_status()
            data = self._unwrap(response.json())
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return data.get("sessions") or data.get("sessionsList") or []
            return []
        except Exception as e:
            print(f"Error listing sessions: {e}")
            return []

    def create_session(self, title):
        try:
            response = requests.post(
                self._url("/session"),
                json={"title": title},
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = self._unwrap(response.json())
            return data['id']
        except Exception as e:
            print(f"Error creating session: {e}")
            return None

    def _suggest_models(self, provider_id, requested_model_id, limit=5):
        try:
            response = requests.get(self._url("/provider"), headers=self.headers, timeout=10)
            response.raise_for_status()
            data = self._unwrap(response.json())
            providers = data.get("all", []) if isinstance(data, dict) else (data or [])
            provider = None
            for p in providers:
                if not isinstance(p, dict):
                    continue
                inner = p.get("data") if isinstance(p.get("data"), dict) else None
                candidate = p.get("id") or (inner or {}).get("id")
                if candidate == provider_id:
                    provider = inner if inner and inner.get("id") == provider_id else p
                    break
            if not provider:
                return []
            models = provider.get("models") or {}
            model_ids = list(models.keys())
            if requested_model_id in model_ids:
                return [requested_model_id]

            related = [m for m in model_ids if requested_model_id in m or m in requested_model_id]
            if related:
                return related[:limit]

            stem = requested_model_id.rsplit("-", 1)[0] if "-" in requested_model_id else requested_model_id
            related = [m for m in model_ids if stem and stem in m]
            return related[:limit]
        except Exception:
            return []

    def _wait_for_first_assistant_message(self, session_id, max_wait=45, poll_interval=3):
        started = time.time()
        while (time.time() - started) < max_wait:
            messages = self.get_session_messages(session_id) or []
            if any(
                (m.get("type") == "assistant")
                or ((m.get("info") or {}).get("role") == "assistant")
                for m in messages if isinstance(m, dict)
            ):
                return True
            time.sleep(poll_interval)
        return False

    def send_message(self, session_id, message, model_id="antigravity-gemini-3-flash", provider_id=None, agent="build"):
        try:
            # Auto-detect provider from model_id if not specified
            if provider_id is None:
                provider_id = "google"
                if model_id == "glm-5":
                    provider_id = "zai-coding-plan"
                elif model_id.startswith("anthropic") or "/" in model_id:
                    # Handle format like "anthropic/claude-sonnet-4-6"
                    if "/" in model_id:
                        provider_id, model_id = model_id.split("/", 1)
                    else:
                        provider_id = "anthropic"

            self._last_send_time_ms = int(time.time() * 1000)

            # v2 style first: POST /session/:id/prompt (async, wrapped payload).
            prompt_response = requests.post(
                self._url(f"/session/{session_id}/prompt"),
                json={
                    "text": message,
                    "model": {"modelID": model_id, "providerID": provider_id},
                    "agent": agent,
                },
                headers=self.headers,
                timeout=MESSAGE_TIMEOUT,
            )
            if prompt_response.status_code == 404:
                # Flat/v1 server: fall back to the synchronous message endpoint.
                return self._send_message_v1(session_id, message, model_id, provider_id, agent)
            prompt_response.raise_for_status()
            return {"status": "prompt_sent", "session_id": session_id}
        except requests.exceptions.RequestException as e:
            if "Read timed out" not in str(e):
                print(f"Request Exception: {e}")
            return None

    def _send_message_v1(self, session_id, message, model_id, provider_id, agent):
        try:
            response = requests.post(
                self._url(f"/session/{session_id}/message"),
                json={
                    "parts": [{"type": "text", "text": message}],
                    "model": {
                        "modelID": model_id,
                        "providerID": provider_id
                    },
                    "agent": agent
                },
                headers=self.headers,
                timeout=MESSAGE_TIMEOUT,
            )

            if response.status_code != 200:
                print(f"Server returned {response.status_code} Error: {response.text}")

            response.raise_for_status()

            if not response.text.strip():
                has_assistant_reply = self._wait_for_first_assistant_message(session_id)
                if has_assistant_reply:
                    return {
                        "status": "accepted_empty_response",
                        "session_id": session_id,
                    }

                suggestions = self._suggest_models(provider_id, model_id)
                print("Server returned 200 with empty response body; request was likely rejected before agent reply.")
                print(f"Model/provider used: {provider_id}/{model_id}")
                if suggestions and suggestions[0] != model_id:
                    print(f"Try one of these models for provider '{provider_id}': {', '.join(suggestions)}")
                return None

            try:
                return response.json()
            except ValueError as e:
                suggestions = self._suggest_models(provider_id, model_id)
                print(f"Response JSON parse failed: {e}")
                print(f"Model/provider used: {provider_id}/{model_id}")
                print(f"Raw response prefix: {response.text[:200]!r}")
                if suggestions and suggestions[0] != model_id:
                    print(f"Try one of these models for provider '{provider_id}': {', '.join(suggestions)}")
                return None
        except requests.exceptions.RequestException as e:
            if "Read timed out" not in str(e):
                print(f"Request Exception: {e}")
            return None

    def get_session_messages(self, session_id):
        try:
            response = requests.get(
                self._url(f"/session/{session_id}/message"),
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
            data = self._unwrap(response.json())
            if isinstance(data, list):
                return data
            if isinstance(data, dict):
                return data.get("messages") or []
            return []
        except Exception as e:
            print(f"Error getting messages: {e}")
            return None

    def delete_session(self, session_id):
        """DELETE /session/:id - remove session from storage (e.g. after ephemeral task completes)."""
        try:
            response = requests.delete(
                self._url(f"/session/{session_id}"),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return True
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False

    def get_session_info(self, session_id):
        """GET /session/:id - session metadata (e.g. status, running)."""
        try:
            response = requests.get(
                self._url(f"/session/{session_id}"),
                headers=self.headers,
                timeout=10,
            )
            response.raise_for_status()
            return self._unwrap(response.json())
        except Exception as e:
            print(f"Error getting session info: {e}")
            return None

    def wait_for_session_complete(
        self,
        session_id,
        poll_interval=15,
        max_wait=7200,
    ):
        """
        Poll until session is idle. Ensures we don't start the next task before this one finishes.
        Used when send_message times out or returns immediately (v2 prompt endpoint).
        """
        start = time.time()
        baseline_ms = int(start * 1000) - 30000  # slack for clock/latency skew

        while (time.time() - start) < max_wait:
            if self._api_mode == "v2":
                # v2: poll messages until an idle event newer than this prompt arrives.
                messages = self.get_session_messages(session_id)
                if messages:
                    newest_idle_created = 0
                    for m in messages:
                        if isinstance(m, dict) and m.get("type") == "idle":
                            created = (m.get("time") or {}).get("created") or 0
                            newest_idle_created = max(newest_idle_created, created)
                    if newest_idle_created >= baseline_ms:
                        return True
                elapsed = int(time.time() - start)
                print(f"  ... session still running ({elapsed}s elapsed), polling in {poll_interval}s")
                time.sleep(poll_interval)
                continue

            # v1: check session metadata for running/busy state.
            messages = self.get_session_messages(session_id)
            if messages:
                has_assistant = any(
                    (m.get("info") or {}).get("role") == "assistant"
                    for m in messages if isinstance(m, dict)
                )
                if has_assistant:
                    info = self.get_session_info(session_id)
                    if info and not (info.get("running") or info.get("busy")) \
                            and info.get("status", "") not in ("running", "busy"):
                        return True
            elapsed = int(time.time() - start)
            print(f"  ... session still running ({elapsed}s elapsed), polling in {poll_interval}s")
            time.sleep(poll_interval)
        print(f"  wait_for_session_complete: max_wait {max_wait}s exceeded")
        return False
