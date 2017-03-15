import os
import tempfile


class Configuration:

    EMIS_RABBITMQ_DEFAULT_USER = os.environ.get("EMIS_RABBITMQ_DEFAULT_USER")
    EMIS_RABBITMQ_DEFAULT_PASS = os.environ.get("EMIS_RABBITMQ_DEFAULT_PASS")
    EMIS_RABBITMQ_DEFAULT_VHOST = os.environ.get("EMIS_RABBITMQ_DEFAULT_VHOST")
    EMIS_PROPERTY_DATA = os.environ.get("EMIS_PROPERTY_DATA") or \
        tempfile.gettempdir()

    EMIS_PROPERTY_HOST = "emis_property"


    @staticmethod
    def init_app(
            app):
        pass


class DevelopmentConfiguration(Configuration):

    EMIS_PROPERTY_PORT = 5000


class TestConfiguration(Configuration):

    EMIS_PROPERTY_PORT = 5000


class ProductionConfiguration(Configuration):

    EMIS_PROPERTY_PORT = 3031


configuration = {
    "development": DevelopmentConfiguration,
    "test": TestConfiguration,
    "acceptance": ProductionConfiguration,
    "production": ProductionConfiguration
}
