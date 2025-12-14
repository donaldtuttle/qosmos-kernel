# qosmos/operators.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .contracts import XI_FUSION_KEY, enforce_non_arithmetic_fusion, enforce_xi_invariant
from .memory import Memory
from .types import Context, Fusion, Gamma, Psi, PsiReflexive


# -----------------------------------------------------------------------------
# Protocols (keeps XiUpdate clean + enforces the "operator shape" consistently)
# -----------------------------------------------------------------------------

class Projector(Protocol):
    name: str
    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> PsiReflexive: ...


class GradientComputer(Protocol):
    name: str
    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> Gamma: ...


# -----------------------------------------------------------------------------
# Πᴽ — Reflexive Projection
# -----------------------------------------------------------------------------

@dataclass
class ReflexiveProjection:
    """
    Πᴽ : Ψ → Ψ  (implemented here as producing a typed ψᴽ artifact)
    """
    name: str = "Πᴽ"

    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> PsiReflexive:
        # Minimal, auditable projection: snapshot/summary payload
        return PsiReflexive(
            source_id=psi.id,
            payload={
                "t": psi.t,
                "task": ctx.task,
                "mode": ctx.mode,
                "state": psi.data,
            },
        )


# -----------------------------------------------------------------------------
# Γ — Semantic Gradient
# -----------------------------------------------------------------------------

@dataclass
class SemanticGradient:
    """
    Γ : Ψ × Ctx → Ψ  (implemented here as producing a typed Γ artifact)
    """
    name: str = "Γ"

    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> Gamma:
        # Minimal, auditable gradient stub:
        # - magnitude tied to coherence (ρ gate proxy)
        # - direction carries task tag (representation-agnostic)
        return Gamma(
            magnitude=float(psi.coherence),
            direction={
                "task": ctx.task,
                "mode": ctx.mode,
                "note": "stub Γ(ψ) — replace with concrete Φ/ρ/∇Φ instantiation",
            },
        )


# -----------------------------------------------------------------------------
# Ξ — Recursive Update (contract-enforced)
# -----------------------------------------------------------------------------

@dataclass
class XiUpdate:
    """
    Ξ : Ψ → Ψ
    Enforces: Ξ(ψ) = ψᴽ ⊕ Γ(ψ) via typed Fusion artifact.
    """
    name: str = "Ξ"
    projector: Projector = None  # type: ignore[assignment]
    gradient: GradientComputer = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.projector is None:
            self.projector = ReflexiveProjection()
        if self.gradient is None:
            self.gradient = SemanticGradient()

    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> Psi:
        psi_w = self.projector.apply(psi, ctx, mem)
        gamma = self.gradient.apply(psi, ctx, mem)

        fusion = Fusion(psi_reflexive=psi_w, gamma=gamma)
        enforce_non_arithmetic_fusion(fusion)

        psi_next = Psi(
            id=psi.id,
            data={XI_FUSION_KEY: fusion},
            coherence=psi.coherence,
            t=psi.t + 1,
        )

        enforce_xi_invariant(psi_next)

        # Append-only trace for audit
        mem.trace.append(
            {
                "t": psi_next.t,
                "op": "Ξ",
                "psi_id": psi_next.id,
                "artifact": fusion,
            }
        )
        return psi_next


# -----------------------------------------------------------------------------
# Λψ — Collapse / Projection (non-smooth, logged)
# -----------------------------------------------------------------------------

@dataclass
class Collapse:
    """
    Λψ : Ψ → Ψ
    Non-smooth projection event, threshold-gated.
    Must emit an explicit collapse artifact if triggered.
    """
    name: str = "Λψ"

    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> Psi:
        threshold = float(ctx.limits.get("collapse_threshold", 1.0))
        triggered = psi.coherence >= threshold

        if not triggered:
            return psi

        # Emit explicit collapse record
        mem.events.append(
            {
                "type": "collapse",
                "op": "Λψ",
                "t": psi.t,
                "psi_id": psi.id,
                "threshold": threshold,
                "coherence": psi.coherence,
            }
        )

        # Non-smooth projection marker (minimal)
        next_data = dict(psi.data)
        next_data["_collapsed"] = True

        return Psi(
            id=psi.id,
            data=next_data,
            coherence=1.0,  # minimal "post-collapse stabilization" placeholder
            t=psi.t,
        )
