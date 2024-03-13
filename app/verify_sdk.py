import sentry_sdk
from flask import Flask

sentry_sdk.init(
    dsn="https://289b22b6ef4db3b6fec473d26ce82c96@o4506808768397312.ingest.sentry.io/4506808771936256",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

@app.route("/")
def hello_world():
    1/0  # raises an error
    return "<p>Hello, World!</p>"