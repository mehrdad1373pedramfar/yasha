
from nanohttp import html, json, RestController
from restfulpy.controllers import RootController

import yasha
from yasha.controllers.issue import IssueController
from yasha.controllers.work_group import WorkGroupController


class ApiV1(RestController):
    issues = IssueController()
    work_groups = WorkGroupController()

    @json
    def version(self):
        return {
            'version': yasha.__version__
        }


class Root(RootController):
    apiv1 = ApiV1()

    @html
    def index(self):
        return 'Index'
