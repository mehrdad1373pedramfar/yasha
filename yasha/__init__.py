from os.path import dirname, join

from restfulpy.application import Application


from yasha.controllers import Root

__version__ = '0.1.0-planning.0'


class Yasha(Application):

    builtin_configuration = """
    db:
      uri: postgresql://postgres:postgres@localhost/ursa_dev
      test_uri: postgresql://postgres:postgres@localhost/ursa_test
      administrative_uri: postgresql://postgres:postgres@localhost/postgres
      echo: false

    application:
      welcome_url: http://localhost:8081/welcome

    """

    def __init__(self):
        super().__init__(
            self.__class__.__name__.lower(),
            root=Root(),
            root_path=join(dirname(__file__), '..'),
            version=__version__,
        )

    def insert_mockup(self):
        raise NotImplementedError()

    def insert_basedata(self):  # pragma: no cover
        raise NotImplementedError()


yasha = Yasha()
