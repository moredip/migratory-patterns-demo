from asgi_correlation_id import CorrelationIdMiddleware, correlation_id
from openfeature import api as openfeature
from openfeature.evaluation_context import EvaluationContext
from opentelemetry import trace
from fastapi import FastAPI, Request, Response

from feature_flags import init_feature_flags
from latency import simulate_latency
from otel import instrument_app

import db

tracer = trace.get_tracer(__name__)

init_feature_flags()

pinecone = db.PineconeStore()
postgres = db.PostgresStore()

feature_flags = openfeature.get_client()

app = FastAPI()


@app.middleware("http")
async def use_request_id_as_open_feature_identity(request: Request, call_next):
    request_id = correlation_id.get()
    if request_id:
        openfeature.set_evaluation_context(EvaluationContext(targeting_key=request_id))
    return await call_next(request)


app.add_middleware(CorrelationIdMiddleware)


@app.get("/")
async def root():
    return Response("Hello, World!")


@app.get("/calculate")
async def calculate():
    use_postgres = feature_flags.get_boolean_value("postgres_vector_store", False)
    with tracer.start_as_current_span("fetch"):
        if use_postgres:
            await postgres.fetch()
        else:
            await pinecone.fetch()

    with tracer.start_as_current_span("calculate"):
        await simulate_latency(mean=0.1, stddev=0.1)

    return Response(
        f"I calculated something using {"postgres" if use_postgres else "pinecone"}"
    )


instrument_app(app)
