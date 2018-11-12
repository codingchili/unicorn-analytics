from datetime import date, timedelta

DATE_FORMAT = '%Y-%m-%d'


def today():
    """ get todays date formatted for use with the GOOGLE APIs. """
    return date.today().strftime(DATE_FORMAT)


def yesterday():
    """ get yesterdays date formatted for use with the GOOGLE APIs. """
    return (date.today() - timedelta(1)).strftime(DATE_FORMAT)


def week():
    """ the date 7 days back formatted for use with the GOOGLE APIs. """
    return (date.today() - timedelta(7)).strftime(DATE_FORMAT)