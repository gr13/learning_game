from flask import Flask
from datetime import datetime
from flask import request, has_request_context

DT_STRING_FORMAT = "%Y-%m-%d %H:%M:%S"


def register_request_logging(app: Flask):
    """
    Registers request/response logging middleware.
    """
    @app.before_request
    def log_request_info():

        app.logger.info("######################################################")  # noqa: E501
        app.logger.info("Request received")

        now = datetime.now()
        app.logger.info(
            f"datetime: {now.strftime(DT_STRING_FORMAT)}"
        )
        if has_request_context():

            url = request.url
            remote_addr = request.remote_addr

            app.logger.info(
                f"ip: {remote_addr}, url: {url}"
            )
        if request.headers:
            app.logger.info("Headers: %s", dict(request.headers))

        if request.get_data():
            try:
                body = request.get_data().decode("utf-8")
            except Exception:
                body = "<binary data>"

            app.logger.info("Body: %s", body)
        if request.is_json:
            app.logger.info("JSON: %s", request.get_json())
        else:
            app.logger.info("No JSON payload")

        app.logger.info("------------------------------------------------------")  # noqa: E501

    @app.after_request
    def log_response(response):
        """
        Log outgoing response.
        """
        app.logger.info(
            f"Response status: {response.status}"
        )
        app.logger.info("######################################################")  # noqa: E501

        return response
