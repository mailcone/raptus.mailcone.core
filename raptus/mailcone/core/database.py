import grok

from megrok import rdb

from zope.event import notify
from zope.lifecycleevent import modified
from zope.schema.interfaces import IField
from zope.interface.interfaces import IInterface
from zope.lifecycleevent import ObjectRemovedEvent

from sqlalchemy.engine.url import URL
from sqlalchemy.orm.interfaces import SessionExtension
from z3c.saconfig import EngineFactory, GloballyScopedSession
from z3c.saconfig.interfaces import IEngineFactory, IScopedSession, IEngineCreatedEvent

from martian.error import GrokError
from martian import Directive, CLASS, MULTIPLE

from raptus.mailcone.app import config



def engine():
    urlconf = dict()
    dbconf = config.local_configuration.get('mail_database')
    # we get all params of __init__ function
    vars = URL.__init__.im_func.func_code.co_varnames
    for var in vars:
        if var in dbconf:
            urlconf[var] = dbconf.get(var)
    url = URL(**urlconf)
    dbconf = dict([(k,v) for k,v in dbconf.iteritems() if k not in urlconf.keys()])
    return EngineFactory(url, **dbconf)

grok.global_utility(engine(), provides=IEngineFactory, direct=True)



class SQLAlchemyEvent(SessionExtension):

    def before_flush(self, session, flush_context, instances):
        for obj in session.deleted:
            parent = getattr(obj, '__parent__', None)
            name = unicode(getattr(obj, 'id', None))
            notify(ObjectRemovedEvent(obj, parent, name))


    def before_commit(self, session):
        for i in session:
            modified(i)



class GloballyScopedSessionMailcone(GloballyScopedSession):

    def __init__(self, engine=u'', **kw):
        super(GloballyScopedSessionMailcone, self).__init__(engine, **kw)
        zopeex = self.kw['extension']
        self.kw['extension'] = (SQLAlchemyEvent(), zopeex)


scoped_session = GloballyScopedSessionMailcone()
grok.global_utility(scoped_session, provides=IScopedSession, direct=True)



skip_create_metadata = rdb.MetaData()
create_metadata = rdb.MetaData()

@grok.subscribe(IEngineCreatedEvent)
def create_engine_created(event):
    rdb.setupDatabase(create_metadata)

@grok.subscribe(IEngineCreatedEvent)
def skip_create_engine_created(event):
    rdb.setupDatabaseSkipCreate(skip_create_metadata)





class schema(Directive):
    scope = CLASS
    store = MULTIPLE
    default = u''

    def factory(self, schema):
        if not IInterface.providedBy(schema):
            raise GrokImportError(
                "You can only pass an interface to the "
                "provides argument of %s." % self.name)
        return schema
        