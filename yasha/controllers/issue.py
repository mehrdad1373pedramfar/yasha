
from nanohttp import RestController, json, HttpNotFound

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
