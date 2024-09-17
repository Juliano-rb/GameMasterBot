import gettext


def get_locale(language_code):
    locale = gettext.translation("base", localedir="locales", languages=[language_code])
    locale.install()
    return locale.gettext
