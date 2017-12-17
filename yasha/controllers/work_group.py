from nanohttp import RestController, json, HttpNotFound
from restfulpy.orm import DBSession, commit
from restfulpy.validation import validate_form

from yasha.models.work_group import WorkGroup


class WorkGroupController(RestController):
    __model__ = WorkGroup

    @staticmethod
    def _ensure(id_):
        instance = WorkGroup.query.filter(WorkGroup.id == id_).one_or_none()

        if instance is None:
            raise HttpNotFound('Cannot find any work_group with id %s' % id_)

        return instance

    @json
    @WorkGroup.expose
    def get(self, id_: int=None):

        if id_ is None:
            return WorkGroup.query

        return self._ensure(id_)

    @json
    @WorkGroup.expose
    @commit
    @validate_form(blacklist=['id'], requires=['title', 'description'])
    def post(self):
        instance = WorkGroup()
        instance.update_from_request()
        DBSession.add(instance)
        return instance

    @json
    @WorkGroup.expose
    @commit
    @validate_form(blacklist=['id'])
    def put(self, id: int):
        instance = self._ensure(id)
        instance.update_from_request()
        DBSession.add(instance)
        return instance

    @json
    @WorkGroup.expose
    @commit
    @validate_form(blacklist=['id', 'title', 'description', 'priority'])
    def delete(self, id: int):
        instance = self._ensure(id)
        DBSession.delete(instance)
        return instance
