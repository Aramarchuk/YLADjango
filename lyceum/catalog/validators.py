import re

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


__all__ = ()


@deconstructible
class ValidateMustContain:
    words = []

    def __init__(self, *args):
        self.words = args

    def __call__(self, value):
        perfection = False
        for word in self.words:
            if re.search(r"\b{word}\b".format(word=word), value.lower()):
                perfection = True
        if not perfection:
            raise ValidationError((f"There is no perfection in {value}"))

    def __eq__(self, other):
        return (
            isinstance(other, ValidateMustContain)
            and self.words == other.words
        )
