import grok

from zope import security
from zope import publisher

def getRequest():
    i = security.management.getInteraction() # raises NoInteraction
    for p in i.participations:
        if publisher.interfaces.IRequest.providedBy(p):
            return p
    raise RuntimeError('Could not find current request.')
