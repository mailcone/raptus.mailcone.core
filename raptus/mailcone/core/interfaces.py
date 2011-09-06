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