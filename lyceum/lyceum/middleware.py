import re

from django.conf import settings

__all__ = ()


class SimpleMiddleware:
    n = 0

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not settings.ALLOW_REVERSE:
            return response

        if self.check_settings():
            response.content = self.reverse_russian_words(
                response.content.decode("utf-8"),
            )

        return response

    @staticmethod
    def reverse_russian_words(text):
        russian_words_pattern = re.compile(r"^\b[а-яА-яЁё]+\b$")
        words = re.findall(r"\w+|\w+", text)
        reversed_text = []
        for word in words:
            if re.fullmatch(russian_words_pattern, word):
                reversed_word = word[::-1]
                reversed_text.append(reversed_word)
            else:
                reversed_text.append(word)
        pattern = re.compile(r"\b(" + "|".join(map(re.escape, words)) + r")\b")
        return pattern.sub(lambda x: reversed_text.pop(0), text)

    @classmethod
    def check_settings(cls):
        cls.n += 1
        if settings.ALLOW_REVERSE and cls.n % 10 == 0:
            return True
        return False
