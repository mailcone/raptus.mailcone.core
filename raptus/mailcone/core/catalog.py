import grok
from grok import index

from zope.app.component.hooks import getSite
from zope.interface import providedBy
from zc.catalog.catalogindex import ValueIndex

from raptus.mailcone.core import interfaces
from raptus.mailcone.customers.contents import Customer



class Value(index.IndexDefinition):
    index_class = ValueIndex


class ContentIndexes(grok.Indexes):
    """
        Sitewide indexes for objects providing ISearchableContent
    """
    grok.context(interfaces.ISearchable)
    grok.site(interfaces.IMailcone)
    grok.name ('catalog')

    counter = Value()

    id = index.Field()
    url = index.Field()
    implements = index.Set()
    text = index.Text()

    name = index.Field()
    address = index.Field()


class Searchable(grok.Adapter):
    """ Searchable object
    """
    grok.baseclass()
    grok.implements(interfaces.ISearchable)
    
    fulltext_attributes = []
    
    @property
    def id(self):
        return getattr(self.context, 'id', None)
    
    @property
    def implements(self):
        implements = []
        for iface in providedBy(self.context):
            implements.append(iface.__identifier__)
            implements.extend([base.__identifier__ for base in iface.getBases()])
        return implements

    @property
    def text(self):
        text = list()
        for i in self.fulltext_attributes:
            text.append(unicode(getattr(self.context, i)))
        return u' '.join(text)


class SearchableCustomer(Searchable):
    grok.context(Customer)
    fulltext_attributes = ['name', 'address']
    
    