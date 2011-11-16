import grok, re

from zope.component import queryMultiAdapter

from raptus.mailcone.core import utils
from raptus.mailcone.core import interfaces


class TextIdManager(grok.GlobalUtility):
    """ Handles text IDs
    """
    grok.implements(interfaces.ITextIdManager)
    re_ws = re.compile(r'\s+')
    re_chars = re.compile(r'[^a-zA-Z0-9-_]')
    
    def normalize(self, name):
        """ Returns a normalized string usable in URL based on the name provided
        """
        return self.re_chars.sub('', self.re_ws.sub('_', name)).lower()
    
    def idFromName(self, container, name):
        """ Returns a valid ID from a name
        """
        id = self.normalize(name)
        if not self.idCheck(container, id):
            i = 2
            while not self.idCheck(container, '%s-%s' % (id, i) ):
                i += 1
            id = '%s-%s' % (id, i)
        return str(id)
    
    def idCheck(self, container, id):
        """ return True if the the id can be used or False if a view allready are in the way
        """
        if id in container:
            return False
        if queryMultiAdapter((container, utils.getRequest()),name=id):
            return False
        return True



class IntIdManager(TextIdManager):
    grok.provides(interfaces.IIntIdManager)
    
    def nextId(self, container):
        """ Returns a valid ID from a name
        """
        id = 1
        while not self.idCheck(container, str(id)):
            id += 1
        return id



