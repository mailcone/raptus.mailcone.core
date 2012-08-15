import grok
import martian

from megrok import rdb

from zope.schema import interfaces

from sqlalchemy.orm import relation, mapper
from sqlalchemy import Column, Table, MetaData, ForeignKey
from sqlalchemy.types import Integer, Unicode, DateTime, UnicodeText, Boolean
from sqlalchemy.orm.collections import InstrumentedList as BaseInstrumentedList
from raptus.mailcone.core import database





class InstrumentedList(BaseInstrumentedList):

    def __getattribute__(self, name):
        if name == '_sa_appender':
            return self._mc_appender
        if name == 'append':
            return self._mc_append
        return BaseInstrumentedList.__getattribute__(self, name)

    def _mc_appender(self, obj, **kwargs):
        func = BaseInstrumentedList.__getattribute__(self, '_sa_appender')
        func(self.__list_type_class__(obj.value), **kwargs)
        
    def _mc_append(self, value):
        func = BaseInstrumentedList.__getattribute__(self, 'append')
        func(self.__list_type_class__(value))



class ListString(unicode):

    def __init__(self, value):
        super(ListString, self).__init__(value)
        self.value = value



class Schema(martian.ClassGrokker):
    martian.component(rdb.Model)
    martian.directive(database.schema, name='schemas')
    martian.directive(rdb.tablename)
    
    def execute(self, class_, schemas, tablename, config):
        for schema in schemas:
            for attr in schema:
                value = getattr(class_, attr, None)
                if not interfaces.IField.providedBy(schema.get(attr)) or hasattr(class_, attr):
                    continue
                field = schema.get(attr, None)
                if interfaces.IList.providedBy(field):
                    cls = type('%s@%s' % (ListString.__name__,field.__name__,), (ListString,),
                                          dict(ListString.__dict__))
                    metadata = database.create_metadata
                    name = 'list_%s' % field.__name__
                    
                    #column = Column(field.__name__, Integer, primary_key=True, unique=True)
                    column = None
                    for key, value in class_.__dict__.iteritems():
                        if isinstance(value, Column) and value.primary_key:
                            column = value
                            break
                    if column is None:
                        raise NotImplementedError('you need specified one primary_key')
                    
                    listtype = self.column(field.value_type, field.__name__)
                    table = Table(name, metadata,
                                  Column('id_rel_%s' % tablename, Integer, primary_key=True, unique=True),
                                  Column('rel_%s' % tablename, Integer, ForeignKey(column)),
                                  listtype,)
                    mapped = mapper(cls, table, properties=dict(
                                        value=table.c.get(field.__name__),
                                    ))
                    cls_list = type('%s@%s' % (InstrumentedList.__name__,field.__name__,), (BaseInstrumentedList,),
                                              dict(InstrumentedList.__dict__))
                    cls_list.__list_type_class__ = cls
                    column = relation(mapped, collection_class=cls_list, lazy='immediate')
                else:
                    column = self.column(field)
                setattr(class_, attr, column)

        return True

    def column(self, field, name=None):
        if name is None:
            name = field.__name__
        column = None
        if interfaces.ITextLine.providedBy(field):
            column = Column(name, Unicode(field.max_length))

        elif (interfaces.IDate.providedBy(field) or 
              interfaces.IDatetime.providedBy(field)):
            column = Column(name, DateTime)

        elif interfaces.IInt.providedBy(field):
            column = Column(name, Integer)

        elif interfaces.IBool.providedBy(field):
            column = Column(name, Boolean)

        elif interfaces.IText.providedBy(field):
            column = Column(name, UnicodeText)
        return column
        

