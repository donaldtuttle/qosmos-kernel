# qosmos/memory.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class Memory:
    """
    Minimal memory stack (append-only) for auditability.

    - trace: step artifacts (e.g., Fusion from Ξ ticks)
    - events: discrete events (e.g., Λψ collapse artifacts)
    """
    trace: List[Any] = field(default_factory=list)
    events: List[Dict[str, Any]] = field(default_factory=list)
