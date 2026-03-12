"""Tokenizer abstraction placeholder for future transformer integration."""

from __future__ import annotations


class TokenizerStub:
    """Temporary tokenizer interface that keeps integration boundaries stable."""

    def tokenize(self, serialized_request: str) -> list[str]:
        """
        Convert canonical string into coarse tokens.

        TODO: Replace with transformer tokenizer (BPE/WordPiece/SentencePiece).
        """
        return serialized_request.split()

