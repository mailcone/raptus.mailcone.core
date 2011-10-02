import grok

from zope import security
from zope import publisher
from zope.i18n.locales import LocaleDates


def getRequest():
    i = security.management.getInteraction() # raises NoInteraction
    for p in i.participations:
        if publisher.interfaces.IRequest.providedBy(p):
            return p
    raise RuntimeError('Could not find current request.')


def parent(object):
    return object.__parent__


def formatdate(value):
    """ return a datetime object to a string
        http://mirrors.creativecommons.org/developer/doc/p6/current/public/zope.i18n.locales.LocaleDates.html
    """
    calendar = getRequest().locale.dates.calendars['gregorian']
    dates = LocaleDates()
    dates.calendars = {'gregorian': calendar}
    formatter = dates.getFormatter('dateTime')
    return formatter.format(value)