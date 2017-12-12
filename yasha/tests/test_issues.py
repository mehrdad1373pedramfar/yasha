import unittest
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
            issues.append(Issue(title=f'issue {i}', description=f'des {i}'))
        cls.session.add_all(issues)
        cls.session.commit()
        cls.issue_ids = [i.id for i in issues]

    def test_get_all(self):
        response, ___ = self.request(As.user, 'GET', self.url)

        self.assertIsNotNone(response[0]['id'])
        self.assertIsNotNone(response[1]['id'])
        self.assertIsNotNone(response[2]['id'])
        self.assertIsNotNone(response[3]['id'])

        self.assertEqual(response[0]['title'], 'issue 0')
        self.assertEqual(response[1]['title'], 'issue 1')
        self.assertEqual(response[2]['title'], 'issue 2')
        self.assertEqual(response[0]['description'], 'des 0')
        self.assertEqual(response[1]['description'], 'des 1')
        self.assertEqual(response[2]['description'], 'des 2')

        response, ___ = self.request(
            As.user, 'GET', self.url,
            query_string=dict(
                take=2,
                sort='title'
            )
        )

        self.assertEqual(len(response), 2)

        response, ___ = self.request(
            As.user, 'GET', self.url,
            query_string=dict(
                take=3,
                sort='description'
            )
        )

        self.assertEqual(len(response), 3)

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
            As.user, 'POST', self.url,
            params=[
                FormParameter('title', 'test issue'),
                FormParameter('description', 'test description')
            ]
        )

        self.assertEqual(response['title'], 'test issue')
        self.assertEqual(response['description'], 'test description')
        self.assertIsNotNone(response['id'])

        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('id', 2)
            ],
            expected_status=400
        )

        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('title1', 'test issue')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('title', 'test issue')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('description', 'test description')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('description1', 'test description')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'POST', self.url,
            expected_status=400
        )

    def test_put(self):
        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=2
            ),
            params=[
                FormParameter('title', 'updated issue'),
                FormParameter('description', 'updated description')
            ]
        )

        self.assertEqual(response['id'], 2)
        self.assertEqual(response['title'], 'updated issue')
        self.assertEqual(response['description'], 'updated description')

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=0
            ),
            params=[
                FormParameter('title', 'updated issue'),
                FormParameter('description', 'updates description')
            ],
            expected_status=404
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=2
            ),
            expected_status=400
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=1
            ),
            params=[
                FormParameter('id', 2)
            ],
            expected_status=400
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=1
            ),
            params=[
                FormParameter('title', 'test')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=1
            ),
            params=[
                FormParameter('description', 'test')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=0
            ),
            params=[
                FormParameter('title2', 'test')
            ],
            expected_status=400
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=1
            ),
            params=[
                FormParameter('description2', 'test')
            ],
            expected_status=400
        )

    def test_delete(self):
        response, ___ = self.request(
            As.user, 'DELETE', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=4
            )
        )
        self.assertEqual(response['id'], 4)

        self.request(
            As.user, 'GET', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=4
            ),
            expected_status=404
        )

        self.request(
            As.user, 'DELETE', f'{self.url}/%(issue_id)s',
            url_params=dict(
                issue_id=4
            ),
            expected_status=404
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
