import sys
import time
from flask import Config
import pika
import requests
from .configuration import configuration


class DataManager(object):

    def __init__(self):
        self.config = Config(__name__)
        self.credentials = pika.PlainCredentials("blah", "blih")
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host="rabbitmq",
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


    def properties_uri(self,
            route):
        return "http://{}:{}/{}".format(
            self.config["EMIS_PROPERTY_HOST"],
            self.config["EMIS_PROPERTY_PORT"],
            route)


    def on_message(self,
            channel,
            method_frame,
            header_frame,
            body):
        sys.stdout.write("received message: {}".format(body))
        sys.stdout.flush()

        # For now, post an example to the property service.
        payload = {
            "name": "my_name1",
            "pathname": "my_pathname1"
        }
        uri = self.properties_uri("properties")
        response = requests.post(uri, json={"property": payload})

        # TODO Handle errors.
        assert response.status_code == 201, response.text

        channel.basic_ack(delivery_tag=method_frame.delivery_tag)


    def run(self,
            host):

        try:
            sys.stdout.write("Start consuming...")
            sys.stdout.flush()
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        sys.stdout.write("Close connection...")
        sys.stdout.flush()
        self.connection.close()


def create_app(
        configuration_name):

    app = DataManager()

    configuration_ = configuration[configuration_name]
    app.config.from_object(configuration_)
    configuration_.init_app(app)

    return app
