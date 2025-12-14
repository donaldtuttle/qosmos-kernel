# qosmos/contracts.py
from __future__ import annotations

from .errors import ContractViolation
from .types import Fusion, Psi


XI_FUSION_KEY = "_xi_fusion"


def enforce_xi_invariant(psi_next: Psi) -> None:
    """
    Enforce: Ξ(ψ) = ψᴽ ⊕ Γ(ψ)
    Minimal proof requirement:
    - psi_next.data contains a typed Fusion artifact under _xi_fusion
    """
    artifact = psi_next.data.get(XI_FUSION_KEY)
    if artifact is None:
        raise ContractViolation("Ξ invariant violated: missing _xi_fusion artifact.")
    if not isinstance(artifact, Fusion):
        raise ContractViolation("Ξ invariant violated: _xi_fusion is not a typed Fusion artifact.")


def enforce_non_arithmetic_fusion(fusion: Fusion) -> None:
    """
    ⊕ must explicitly contain ψᴽ and Γ(ψ) parts (typed).
    """
    if fusion.psi_reflexive is None:
        raise ContractViolation("⊕ fusion invalid: missing ψᴽ component.")
    if fusion.gamma is None:
        raise ContractViolation("⊕ fusion invalid: missing Γ(ψ) component.")
