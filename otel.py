import os
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, BatchSpanProcessor

from settings import Settings

settings = Settings()

HONEYCOMB_DATASET = "canary-launch-demo"
HONEYCOMB_HEADERS = {
    "x-honeycomb-team": settings.honeycomb_api_key,
    "x-honeycomb-dataset": HONEYCOMB_DATASET,
}
HONEYCOMB_ENDPOINT = "https://api.honeycomb.io/v1/traces"

# Resource can be required for some backends, e.g. Jaeger
# If resource wouldn't be set - traces wouldn't appears in Jaeger
resource = Resource(attributes={"service.name": "demo-service"})

trace_provider = TracerProvider(resource=resource)

jaeger_processor = SimpleSpanProcessor(
    OTLPSpanExporter(endpoint="http://localhost:4317", insecure=True)
)
trace_provider.add_span_processor(jaeger_processor)

honeycomb_processor = BatchSpanProcessor(
    OTLPSpanExporter(
        endpoint=HONEYCOMB_ENDPOINT,
        headers=HONEYCOMB_HEADERS,
    )
)
trace_provider.add_span_processor(honeycomb_processor)

trace.set_tracer_provider(trace_provider)


def instrument_app(app):
    FastAPIInstrumentor.instrument_app(app)
