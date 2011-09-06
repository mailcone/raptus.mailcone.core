import grok

from zope.app.component.hooks import getSite

from raptus.mailcone.core import interfaces


class BaseLocator(object):
    grok.implements(interfaces.IContainerLocator)
    grok.baseclass()
    
    splitedpath = []
    
    def __call__(self):
        return self._obj()
    
    def path(self):
        return self.splitedpath
    
    def url(self, request):
        return grok.url(request, self._obj())
    
    def _obj(self):
        obj = getSite()
        for i in self.splitedpath:
            obj = obj[i]
        return obj