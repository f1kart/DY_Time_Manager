import sentry_sdk

sentry_sdk.init(
    dsn="https://289b22b6ef4db3b6fec473d26ce82c96@o4506808768397312.ingest.sentry.io/4506808771936256",

    # Enable performance monitoring
    enable_tracing=True,
)

