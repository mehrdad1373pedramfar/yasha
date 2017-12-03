from restfulpy.orm import FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase, Field
from sqlalchemy import Integer, Unicode


class Issue(FilteringMixin, OrderingMixin, PaginationMixin, DeclarativeBase):
    __tablename__ = 'issue'

    id = Field(Integer, primary_key=True)

    title = Field(Unicode(50))
