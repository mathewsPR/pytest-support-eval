from __future__ import annotations


def provider_not_configured() -> None:
    raise RuntimeError("promptfoo provider is not configured yet")
