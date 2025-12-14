# qosmos/types.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Protocol


# ---------- Core State ----------

@dataclass
class Psi:
    """
    ψ — Observer state container (representation-agnostic).
    - data: opaque payload (embeddings/graphs/etc.)
    - coherence: ρ(ψ) proxy in [0, 1] by default
    - t: discrete tick
    """
    id: str
    data: Dict[str, Any]
    coherence: float
    t: int = 0


@dataclass
class Context:
    """
    ctx — Execution context.
    Minimal fields match the spec: task, mode, limits envelope.
    """
    task: str
    mode: str
    limits: Dict[str, Any]


# ---------- Typed Artifacts ----------

@dataclass(frozen=True)
class PsiReflexive:
    """
    ψᴽ — Reflexive self-model projection of ψ (typed).
    """
    source_id: str
    payload: Dict[str, Any]


@dataclass(frozen=True)
class Gamma:
    """
    Γ(ψ) — Semantic gradient term (typed), Ψ-valued in the sense it targets Ψ update.
    This kernel keeps it representation-agnostic.
    """
    magnitude: float
    direction: Dict[str, Any]


@dataclass(frozen=True)
class Fusion:
    """
    ⊕ — Typed fusion artifact proving Ξ(ψ) = ψᴽ ⊕ Γ(ψ).
    This is an artifact, not arithmetic.
    """
    psi_reflexive: PsiReflexive
    gamma: Gamma


# ---------- Operator Protocol ----------

class Operator(Protocol):
    name: str
    def apply(self, psi: Psi, ctx: Context, mem: "Memory") -> Psi: ...
