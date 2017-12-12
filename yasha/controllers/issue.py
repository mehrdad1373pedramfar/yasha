
from nanohttp import RestController, json, HttpNotFound
from restfulpy.orm import DBSession, commit
from restfulpy.validation import validate_form

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
    @validate_form(blacklist=['id'], requires=['title'])
    def post(self):
        issue = Issue()
        issue.update_from_request()
        DBSession.add(issue)
        return issue

    @json
    @Issue.expose
    @commit
    @validate_form(blacklist=['id'], requires=['title'])
    def put(self, issue_id: int):
        issue = self.ensure_issue(issue_id)
        issue.update_from_request()
        DBSession.add(issue)
        return issue

    @json
    @Issue.expose
    @commit
    @validate_form(blacklist=['id', 'title'])
    def delete(self, issue_id: int):
        issue = self.ensure_issue(issue_id)
        DBSession.delete(issue)
        return issue
