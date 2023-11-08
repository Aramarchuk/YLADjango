import re

from django.conf import settings

__all__ = ()


class SimpleMiddleware:
    time = 0

    def __init__(self, get_response):
        self.get_response = get_response

    @classmethod
    def check_reverse(cls):
        if not settings.ALLOW_REVERSE:
            return False

        cls.time += 1
        if cls.time == 10:
            cls.time = 0
            return True
        return False

    def reverse_russian_words(self, text):
        unchanged_content = text
        out_con = ""
        end_index = 0
        for match_iter in re.finditer(
            r"\b[а-яА-ЯёЁ]+\b",
            unchanged_content,
        ):
            out_con += unchanged_content[
                end_index : match_iter.start()  # noqa E203
            ]
            out_con += match_iter[0][::-1]
            end_index = match_iter.end()
        out_con += unchanged_content[end_index:]
        return out_con

    def __call__(self, request):
        response = self.get_response(request)

        if self.check_reverse():
            response.content = self.reverse_russian_words(
                response.content.decode("utf-8"),
            )

        return response
