
from nanohttp import RestController, json, HttpNotFound
from restfulpy.orm import DBSession, commit

from yasha.models.issue import Issue


class IssueController(RestController):
    __model__ = Issue

    @staticmethod
    def ensure_issue(id_):
        issue = Issue.query.filter(Issue.id == id_).one_or_none()

        if issue is None:
            raise HttpNotFound('Cannot find any issue with id %s' % id_)

        return issue

    @json
    @Issue.expose
    def get(self, issue_id: int=None):

        if issue_id is None:
            return Issue.query

        return self.ensure_issue(issue_id)

    @json
    @Issue.expose
    @commit
    def post(self):
        issue = Issue()
        issue.update_from_request()
        DBSession.add(issue)
        return issue

