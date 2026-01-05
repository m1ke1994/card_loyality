import logging


class RedactAuthorizationFilter(logging.Filter):
    def filter(self, record):
        if isinstance(record.args, dict) and "HTTP_AUTHORIZATION" in record.args:
            record.args["HTTP_AUTHORIZATION"] = "***"
        return True
