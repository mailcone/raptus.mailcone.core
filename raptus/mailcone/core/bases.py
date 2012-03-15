import grok

from megrok import rdb

from zope import component

from z3c.saconfig.interfaces import IScopedSession
from z3c.saconfig import Session

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
        obj = grok.getSite()
        for i in self.splitedpath:
            obj = obj[i]
        return obj



class Container(grok.Container):
    """ A container for objects implementing IIntId
    """
    grok.implements(interfaces.IContainer)
    grok.baseclass()
    
    id = None
    
    def build_id(self, raw_id):
        """ create a id with the name attribute from the object.
            if this object has no name attribute this method must be overrided
        """
        return component.getUtility(interfaces.ITextIdManager).idFromName(self, raw_id)
    
    def add_object(self, obj, raw_id=None):
        """ Adds a new object and returns the generated id
        """
        if raw_id is None:
            raw_id = str(component.getUtility(interfaces.IIntIdManager).nextId(self))
        
        obj.id = self.build_id(raw_id)
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



class QueryContainer(rdb.QueryContainer, Container):
    grok.baseclass()
    """ a base container for a root container on a sql database.
    
        Note: you need to override query method.
    """


    def get(self, key, default=None):
        try:
            id = int(key)
        except ValueError:
            return default
        try:
            return self[id]
        except KeyError:
            return default

    @property
    def session(self):
        return Session()



class ORMModel(rdb.Model):
    """ fixed __name__
    """
    grok.baseclass()
    
    __unicode_name__ = None
    
    @property
    def __name__(self):
        return self.__unicode_name__
    
    @__name__.setter
    def __name__(self, name):
        self.__unicode_name__ = unicode(name)
    
    
    






