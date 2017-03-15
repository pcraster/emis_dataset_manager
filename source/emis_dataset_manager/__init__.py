import json
import sys
import traceback
from flask import Config
import pika
from .configuration import configuration
from .manage_dataset import scan


class DataManager(object):

    def __init__(self):
        self.config = Config(__name__)


    def properties_uri(self,
            route):
        route = route.lstrip("/")
        return "http://{}:{}/{}".format(
            self.config["EMIS_PROPERTY_HOST"],
            self.config["EMIS_PROPERTY_PORT"],
            route)


    def on_message(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}\n".format(body))
        sys.stdout.flush()

        try:
            body = body.decode("utf-8")
            data = json.loads(body)
            uri = self.properties_uri("properties")
            pathnames = data["pathnames"]
            rewrite = data["rewrite"].split(":") if "rewrite" in data else None
            assert rewrite is None or len(rewrite) == 2, rewrite

            scan(uri, pathnames, rewrite)

        except Exception as exception:

            sys.stderr.write("{}\n".format(traceback.format_exc()))
            sys.stderr.flush()


        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        self.credentials = pika.PlainCredentials(
            self.config["EMIS_RABBITMQ_DEFAULT_USER"],
            self.config["EMIS_RABBITMQ_DEFAULT_PASS"]
        )
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
            virtual_host=self.config["EMIS_RABBITMQ_DEFAULT_VHOST"],
            credentials=self.credentials,
            # Keep trying for 8 minutes.
            connection_attempts=100,
            retry_delay=5  # Seconds
        ))
        self.channel = self.connection.channel()
        self.channel.queue_declare(
            queue="scan")
        self.channel.basic_consume(
            self.on_message,
            queue="scan")

        try:
            sys.stdout.write("Start consuming...\n")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...\n")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = DataManager()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
