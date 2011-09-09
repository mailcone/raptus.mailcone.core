from zope import interface



class IMailcone(interface.Interface):
    """ Marker interface for Mailcone applications
    """

class IContainer(interface.Interface):
    """ base interface for all container objects
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
    name = interface.Attribute('name')
    address = interface.Attribute('address')
