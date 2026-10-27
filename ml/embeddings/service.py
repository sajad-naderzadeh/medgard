import hashlib
import math


class EmbeddingService:
    """
    Local deterministic embedding baseline.

    This is a development implementation.
    A production medical embedding model can later
    implement the same interface.
    """

    def __init__(self, dimensions: int = 384):
        self.dimensions = dimensions

    def embed(self, text: str) -> list[float]:
        vector = []

        for index in range(self.dimensions):
            digest = hashlib.sha256(
                f"{index}:{text}".encode("utf-8")
            ).digest()

            value = int.from_bytes(
                digest[:4],
                byteorder="big",
            )

            vector.append(
                (value / 2**32) * 2 - 1
            )

        norm = math.sqrt(
            sum(value * value for value in vector)
        )

        if norm == 0:
            return vector

        return [
            value / norm
            for value in vector
        ]
