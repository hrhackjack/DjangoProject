from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.utils import translation


class LanguageURLSpecifyMiddleware(MiddlewareMixin):
    """
    Checks if url is containing language code like "domain.com/ru/something/",
    and then middleware is activating this language for user
    with using path without language code like "domain.com/something/".

    Made for SEO purposes, normal use of website will not trigger this.
    """

    def process_request(self, request):
        path_split = request.path.split('/')
        if path_split and len(path_split) >= 2:
            language = path_split[1]  # ex. "ru"
            if language in settings.LANGUAGES_SHORT_CODES:
                translation.activate(language)
                request.path_info = '/'+'/'.join(path_split[2:])
                if request.path[-1] != '/':
                    request.path += '/'

    def process_response(self, request, response):
        path_split = request.path.split('/')
        if path_split and len(path_split) >= 2:
            language = path_split[1]  # ex. "ru"
            if language in settings.LANGUAGES_SHORT_CODES:
                translation.activate(language)
                response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
                if request.path[-1] != '/':
                    request.path += '/'
        return response
