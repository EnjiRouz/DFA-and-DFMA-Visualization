#!/usr/bin/env python3
"""Exception classes specific to pushdown automata."""

from dfma.base.exceptions import AutomatonException


class PDAException(AutomatonException):
    """The base class for all PDA-related errors."""

    pass


class NondeterminismError(PDAException):
    """A DPDA is exhibiting nondeterminism."""

    pass
