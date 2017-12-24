from restfulpy.orm import FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase, Field
from sqlalchemy import Integer, Unicode, orm


class WorkGroup(FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase):
    __tablename__ = 'work_group'

    id = Field(Integer, primary_key=True)

    title = Field(Unicode(50))
    description = Field(Unicode(200))
    priority = Field(Integer, nullable=True)
    issue = orm.relationship("Issue", uselist=False, back_populates="work_group")
    #child = relationship("Child", uselist=False, backref="parent")