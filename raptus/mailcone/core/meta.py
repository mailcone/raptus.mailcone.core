import grok
import martian

from megrok import rdb

from zope.schema import interfaces

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Date, Text, Boolean

from raptus.mailcone.core import database




class Schema(martian.ClassGrokker):
    martian.component(rdb.Model)
    martian.directive(database.schema, name='schemas')
    
    def execute(self, class_, schemas, config):
        for schema in schemas:
            for attr in schema:
                value = getattr(class_, attr, None)
                if not interfaces.IField.providedBy(schema.get(attr)) or isinstance(value, Column):
                    continue
                field = schema.get(attr, None)
                column = None
                if interfaces.ITextLine.providedBy(field):
                    column = Column(field.__name__, String(field.max_length))
    
                elif interfaces.IDate.providedBy(field):
                    column = Column(field.__name__, Date)
    
                elif interfaces.IInt.providedBy(field):
                    column = Column(field.__name__, Integer)
    
                elif interfaces.IBool.providedBy(field):
                    column = Column(field.__name__, Boolean)
    
                elif interfaces.IText.providedBy(field):
                    column = Column(field.__name__, Text)
                    
                setattr(class_, attr, column)

        return True




