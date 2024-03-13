import sentry_sdk
from sentry_sdk.crons import monitor

# Add this decorator to instrument your python function
@monitor(monitor_slug='f1kart')
def tell_the_world(msg):
    print(msg)