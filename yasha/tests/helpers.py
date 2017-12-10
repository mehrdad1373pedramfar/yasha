from restfulpy.testing import ModelRestCrudTestCase

import yasha


class WebTestCase(ModelRestCrudTestCase):
    application = yasha.yasha

    @classmethod
    def mockup(cls):
        """This is a template method to give a chance to testers for adding some mockup data before starting test
        """
        pass


class As:
    god = 'God'
    user = 'User'
    github = 'Github'
    member = '|'.join((god, user))
    anonymouse = 'Anonymouse'

