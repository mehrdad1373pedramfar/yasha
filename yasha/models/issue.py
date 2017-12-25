from restfulpy.orm import FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase, Field
from sqlalchemy import Integer, Unicode, Column, ForeignKey, orm

class Issue(FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase):
    __tablename__ = 'issue'

    id = Field(Integer, primary_key=True)

    title = Field(Unicode(50))
    description = Field(Unicode(200))
    # user_id = Column(Integer, ForeignKey('users.id'))
    work_group_id = Column(Integer, ForeignKey('work_group.id'))
    work_group = orm.relationship("WorkGroup", back_populates="issue")
    #parent_id = Column(Integer, ForeignKey('parent.id'))
