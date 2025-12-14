# qosmos/runtime.py
from __future__ import annotations

from typing import Dict

from .errors import UndefinedOperator
from .memory import Memory
from .types import Context, Operator, Psi


class Runtime:
    """
    Minimal operator runtime:
    - explicit operator registry
    - fail-fast on undefined operators
    """
    def __init__(self) -> None:
        self.operators: Dict[str, Operator] = {}

    def register(self, op: Operator) -> None:
        self.operators[op.name] = op

    def step(self, name: str, psi: Psi, ctx: Context, mem: Memory) -> Psi:
        op = self.operators.get(name)
        if op is None:
            raise UndefinedOperator(f"Operator '{name}' is not registered.")
        return op.apply(psi, ctx, mem)
