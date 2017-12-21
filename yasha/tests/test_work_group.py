import unittest
from restfulpy.testing import FormParameter

from yasha.models.work_group import WorkGroup
from yasha.tests.helpers import WebTestCase, As

not_exist_id = 9999


class WorkGroupTestCase(WebTestCase):
    url = '/apiv1/work_groups'
    __model__ = WorkGroup

    @classmethod
    def mockup(cls):
        work_groups = []
        for i in range(5):
            # noinspection PyArgumentList
            work_groups.append(WorkGroup(title=f'work_group {i}', description=f'des {i}', priority=i+100))
        cls.session.add_all(work_groups)
        cls.session.commit()
        cls.work_group_ids = [i.id for i in work_groups]
        # print(20000)

    def test_get_all(self):

        response, ___ = self.request(As.user, 'GET', self.url)

        self.assertIsNotNone(response[0]['id'])
        self.assertIsNotNone(response[1]['id'])
        self.assertIsNotNone(response[2]['id'])
        self.assertIsNotNone(response[3]['id'])

        self.assertEqual(response[0]['title'], 'work_group 0')
        self.assertEqual(response[1]['title'], 'work_group 1')
        self.assertEqual(response[2]['title'], 'work_group 2')
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

        response, ___ = self.request(
            As.user, 'GET', self.url,
            query_string=dict(
                take=4,
                sort='priority'
            )
        )

        self.assertEqual(len(response), 4)


    def test_get_one(self):
        response, ___ = self.request(
            As.user, 'GET', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=2
            )
        )

        self.assertEqual(response['id'], 2)

        self.request(
            As.user, 'GET', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=not_exist_id
            ),
            expected_status=404
        )

    def test_post(self):
        response, ___ = self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('title', 'test work_group 1'),
                FormParameter('description', 'test description 1'),
                FormParameter('priority', 10001)
            ]
        )

        self.assertEqual(response['title'], 'test work_group 1')
        self.assertEqual(response['description'], 'test description 1')
        self.assertEqual(response['priority'], 10001)
        self.assertIsNotNone(response['id'])

        response, ___ = self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('title', 'test work_group 2'),
                FormParameter('description', 'test description 2'),
            ]
        )

        self.assertIsNone(response['priority'])


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
                FormParameter('NOTExistField', 'test')
            ],
            expected_status=400
        )


        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('title', 'missing description')
            ],
            expected_status=400
        )


        self.request(
            As.user, 'POST', self.url,
            params=[
                FormParameter('description', 'missing title')
            ],
            expected_status=400
        )

        # no field input
        self.request(
            As.user, 'POST', self.url,
            expected_status=400
        )

    def test_put(self):
        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=2
            ),
            params=[
                FormParameter('title', 'updated work_group 2'),
                FormParameter('description', 'updated description 2')
            ]
        )

        self.assertEqual(response['id'], 2)
        self.assertEqual(response['title'], 'updated work_group 2')
        self.assertEqual(response['description'], 'updated description 2')

        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=3
            ),
            params=[
                FormParameter('priority', '30002')
            ]
        )
        self.assertEqual(response['id'], 3)
        self.assertEqual(response['title'], 'work_group 2')
        self.assertEqual(response['description'], 'des 2')
        self.assertEqual(response['priority'], 30002)

        #  invalid id
        self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=0
            ),
            params=[
                FormParameter('title', 'updated work_group'),
                FormParameter('description', 'updates description')
            ],
            expected_status=404
        )

        # update with no update field
        self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=2
            )
        )

        # id update is not allowed
        self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=1
            ),
            params=[
                FormParameter('id', 2)
            ],
            expected_status=400
        )

        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=1
            ),
            params=[
                FormParameter('title', 'do not update description')
            ]
        )
        self.assertEqual(response['title'], 'do not update description')

        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=2
            ),
            params=[
                FormParameter('description', 'do not update title')
            ]
        )
        self.assertEqual(response['description'], 'do not update title')

        response, ___ = self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=3
            ),
            params=[
                FormParameter('priority', 50003)
            ]
        )
        self.assertEqual(response['priority'], 50003)


        self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=1
            ),
            params=[
                FormParameter('description2', 'test')
            ],
            expected_status=400
        )


    def test_delete(self):
        response, ___ = self.request(
            As.user, 'DELETE', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=4
            )
        )
        self.assertEqual(response['id'], 4)

        self.request(
            As.user, 'GET', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=4
            ),
            expected_status=404
        )

        self.request(
            As.user, 'PUT', f'{self.url}/%(work_group_id)s',
            url_params=dict(
                work_group_id=4
            ),
            expected_status=404
        )


if __name__ == '__main__':  # pragma: no cover
    unittest.main()
