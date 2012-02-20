from zope import interface



class IMailcone(interface.Interface):
    """ Marker interface for Mailcone applications
    """

class IContainer(interface.Interface):
    """ A container for objects implementing TextIdManager
    """
    
    def add_object(obj):
        """ Adds a new object and returns the generated id
        """
    
    def get_object(id):
        """ Returns the specified object
        """
    
    def del_object(id):
        """ Deletes the specified object
        """
    
    def objects():
        """ Iterator over the contained objects
        """
    

class IContainerLocator(interface.Interface):
    """ Base interface for locate container instances
    """

    def __call__(self):
        """ return the located object
        """
    def path(self):
        """ return a splited path as list
        """
    def url(self):
        """ return the url from the object
        """


class ISearchable(interface.Interface):
    """ Interface for content models, contract used for indexing """
    id = interface.Attribute('id')
    url = interface.Attribute('url')
    implements = interface.Attribute('implements')
    text = interface.Attribute('text')
    name = interface.Attribute('name')
    address = interface.Attribute('address')
    counter = interface.Attribute('counter')
    description = interface.Attribute('description')
    task = interface.Attribute('task')
    status = interface.Attribute('status')
    log_from = interface.Attribute('log_from')
    log_to = interface.Attribute('log_to')
    category = interface.Attribute('category')


class ITextIdManager(interface.Interface):

    def normalize(self, name):
        """ Returns a normalized string usable in URL based on the name provided
        """
    
    def idFromName(self, container, name):
        """ Returns a valid ID from a name
        """
    
    def idCheck(self, container, id):
        """ return True if the the id can be used or False if a view allready are in the way
        """



class IIntIdManager(interface.Interface):
    
    def nextId(self, container):
        """ Returns the next valid ID as Int
        """



