import grok

from zope import component

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
        obj = component.hooks.getSite()
        for i in self.splitedpath:
            obj = obj[i]
        return obj
    

class Container(grok.Container):
    """ A container for objects implementing IIntId
    """
    grok.implements(interfaces.IContainer)
    grok.baseclass()
    
    def build_id(self, raw_id):
        """ create a id with the name attribute from the object.
            if this object has no name attribute this method must be overrided
        """
        return component.getUtility(interfaces.ITextIdManager).idFromName(self, raw_id)
    
    def add_object(self, obj, raw_id):
        """ Adds a new object and returns the generated id
        """
        obj.id = self.build_id(raw_id)
        self._last = obj
        self[str(obj.id)] = obj
        return obj.id
    
    def get_object(self, id):
        """ Returns the specified object
        """
        return self[str(id)]
    
    def del_object(self, id):
        """ Deletes the specified object
        """
        del self[str(id)]
    
    def objects(self):
        """ Iterator over the contained objects
        """
        return self.values()
    