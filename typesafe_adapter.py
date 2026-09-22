"""Thin HTTP boundary between AMR-Jev ORIENT and TypeSafe System One."""

import json
from urllib.request import Request, urlopen

from amr_jev import build_orient_request, reduce_orient_answers

SYSTEM_ONE_URL = "https://api.typesafe.ai/v1/systemone"


def route_orient(
    state,
    api_key,
    *,
    model="jev-latest",
    endpoint=SYSTEM_ONE_URL,
    timeout=25,
    opener=urlopen,
):
    """Send one ORIENT request and reduce the validated Noul answers through AMR policy."""
    if not isinstance(api_key, str) or not api_key.strip():
        return {
            "status": "SETUP_REQUIRED",
            "reason": "missing_typesafe_credential",
            "provider": "typesafe",
            "required_setting": "TYPESAFE_API_KEY",
        }

    request = Request(
        endpoint,
        data=json.dumps(build_orient_request(state, model=model)).encode(),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(request, timeout=timeout) as response:
            status = getattr(response, "status", 200)
            raw = response.read()
    except OSError as exc:
        raise RuntimeError("TypeSafe request failed; no route was produced") from exc

    if not 200 <= status < 300:
        raise RuntimeError(f"TypeSafe returned HTTP {status}; no route was produced")

    try:
        payload = json.loads(raw)
        answers = payload["answers"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ValueError("Malformed TypeSafe response") from exc

    return reduce_orient_answers(answers)
