import grok
from grok import index

from zope.app.component.hooks import getSite
from zope.interface import providedBy
from zc.catalog.catalogindex import ValueIndex

from raptus.mailcone.customers.contents import Customer
from raptus.mailcone.rules.contents import Ruleset
from raptus.mailcone.cronjob.contents import CronJob
from raptus.mailcone.persistentlog.contents import Log

from raptus.mailcone.core import interfaces



class Value(index.IndexDefinition):
    index_class = ValueIndex


class ContentIndexes(grok.Indexes):
    """
        Sitewide indexes for objects providing ISearchable
    """
    grok.context(interfaces.ISearchable)
    grok.site(interfaces.IMailcone)
    grok.name ('catalog')

    counter = Value()

    id = index.Field()
    url = index.Field()
    implements = index.Set()
    text = index.Text()
    
    #Customers
    name = index.Field()
    address = index.Field()

    #Rulesets
    description = index.Field()
    
    #Cronjob
    task = index.Field()
    status = index.Field()
    started = index.Field()
    time_of_next_call = index.Field()

    #Persistent Log
    log_from = index.Field()
    log_to = index.Field()
    category = index.Field()


class Searchable(grok.Adapter):
    """ Searchable object
    """
    grok.baseclass()
    grok.implements(interfaces.ISearchable)
    
    fulltext_attributes = []
    
    def __getattr__(self, name):
        return getattr(self.context, name, None)
    
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
    fulltext_attributes = ['id', 'name', 'address']
    
    
class SearchableRuleset(Searchable):
    grok.context(Ruleset)
    fulltext_attributes = ['id', 'name', 'description']
    

class SearchableCronJob(Searchable):
    grok.context(CronJob)
    fulltext_attributes = ['id', 'task', 'status', 'description']


class SearchableLog(Searchable):
    grok.context(Log)
    fulltext_attributes = ['id', 'log_from', 'log_to', 'category']

