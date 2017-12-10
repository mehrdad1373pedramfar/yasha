from restfulpy.testing import FormParameter

from yasha.models.issue import Issue
from yasha.tests.helpers import WebTestCase, As


class IssueTestCase(WebTestCase):
    url = '/apiv1/issues'
    __model__ = Issue

    @classmethod
    def mockup(cls):
        issues = []
        for i in range(5):
            # noinspection PyArgumentList
            issues.append(Issue(title=f'issue {i}'))
        cls.session.add_all(issues)
        cls.session.commit()
        cls.issue_ids = [i.id for i in issues]

    def test_get_all(self):
        response, ___ = self.request(As.user, 'GET', self.url)

        self.assertIsNotNone(response[0]['id'])
        self.assertIsNotNone(response[1]['id'])
        self.assertIsNotNone(response[2]['id'])
        self.assertIsNotNone(response[3]['id'])
        self.assertIsNotNone(response[4]['id'])

        self.assertEqual(response[0]['title'], 'issue 0')
        self.assertEqual(response[1]['title'], 'issue 1')
        self.assertEqual(response[2]['title'], 'issue 2')

        response, ___ = self.request(
            As.user, 'GET', self.url,
            query_string=dict(
                take=2,
                sort='title'
            )
        )

        self.assertEqual(len(response), 2)

    def test_get_one(self):
        response, ___ = self.request(
            As.user, 'GET', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=2
            )
        )

        self.assertEqual(response['id'], 2)

        self.request(
            As.user, 'GET', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=999
            ),
            expected_status=404
        )

    def test_post(self):
        response, ___ = self.request(
            As.user, 'CREATE', self.url,
            params=[
                FormParameter('title', 'test issue')
            ]
        )

        self.assertEqual(response['title'], 'test issue')
        self.assertIsNotNone(response['id'])


