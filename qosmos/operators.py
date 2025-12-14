# qosmos/operators.py
from __future__ import annotations

from .contracts import XI_FUSION_KEY, enforce_non_arithmetic_fusion, enforce_xi_invariant
from .memory import Memory
from .types import Context, Fusion, Gamma, Psi, PsiReflexive


class ReflexiveProjection:
    """
    Πᴽ : Ψ → Ψ  (implemented here as producing a typed ψᴽ artifact)
    """
    name = "Πᴽ"

    def project(self, psi: Psi, ctx: Context, mem: Memory) -> PsiReflexive:
        # Minimal, auditable projection: snapshot/summary payload
        return PsiReflexive(
            source_id=psi.id,
            payload={
                "t": psi.t,
                "task": ctx.task,
                "state": psi.data,
            },
        )


class SemanticGradient:
    """
    Γ : Ψ × Ctx → Ψ  (implemented here as producing a typed Γ artifact)
    """
    name = "Γ"

    def compute(self, psi: Psi, ctx: Context, mem: Memory) -> Gamma:
        # Minimal, auditable gradient stub:
        # - magnitude tied to coherence (ρ gate proxy)
        # - direction carries task tag (representation-agnostic)
        return Gamma(
            magnitude=float(psi.coherence),
            direction={
                "task": ctx.task,
                "note": "stub Γ(ψ) — replace with concrete Φ/ρ/∇Φ instantiation",
            },
        )


class XiUpdate:
    """
    Ξ : Ψ → Ψ
    Enforces: Ξ(ψ) = ψᴽ ⊕ Γ(ψ) via typed Fusion artifact.
    """
    name = "Ξ"

    def __init__(self, projector: ReflexiveProjection, gradient: SemanticGradient) -> None:
        self.projector = projector
        self.gradient = gradient

    def apply(self, psi: Psi, ctx: Context, mem: Memory) -> Psi:
        psi_w = self.projector.project(psi, ctx, mem)
        gamma = self.gradient.compute(psi, ctx, mem)

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


class Collapse:
    """
    Λψ : Ψ → Ψ
    Non-smooth projection event, threshold-gated.
    Must emit an explicit collapse artifact if triggered.
    """
    name = "Λψ"

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

        # Non-smooth projection: mark discrete commitment (minimal)
        next_data = dict(psi.data)
        next_data["_collapsed"] = True

        return Psi(
            id=psi.id,
            data=next_data,
            coherence=1.0,  # minimal "post-collapse stabilization" placeholder
            t=psi.t,
        )
