"""Class Dadu."""
import random


class Dadu:
    """Dadu enam sisi.

    # ENCAPSULATION: nilai terakhir disimpan private dan hanya bisa dibaca.
    """

    def __init__(self):
        self.__nilai = 1

    @property
    def nilai(self):
        return self.__nilai

    def kocok(self):
        """Mengacak nilai 1-6 dan mengembalikannya."""
        self.__nilai = random.randint(1, 6)
        return self.__nilai
