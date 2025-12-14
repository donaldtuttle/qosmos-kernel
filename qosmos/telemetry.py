# qosmos/telemetry.py
from __future__ import annotations

from .memory import Memory
from .types import Psi


def psi_meta(psi: Psi, mem: Memory) -> dict:
    """
    Minimal Ψmeta-style telemetry snapshot (audit-friendly).
    """
    return {
        "t": psi.t,
        "psi_id": psi.id,
        "coherence": psi.coherence,
        "trace_len": len(mem.trace),
        "event_len": len(mem.events),
        "collapsed": bool(psi.data.get("_collapsed", False)),
    }
