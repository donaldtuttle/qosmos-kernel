# qosmos/errors.py
class QOSMOSError(Exception):
    """Base error for the qosmos-kernel runtime."""
    pass


class ContractViolation(QOSMOSError):
    """Raised when a required contract/invariant is violated."""
    pass


class UndefinedOperator(QOSMOSError):
    """Raised when an operator is requested but not registered."""
    pass


class CollapseError(QOSMOSError):
    """Raised when collapse logic fails (misconfigured thresholds, etc.)."""
    pass
