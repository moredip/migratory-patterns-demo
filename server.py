from latency import simulate_latency
from otel import instrument_app

from opentelemetry import trace
from fastapi import FastAPI, Response

import db

tracer = trace.get_tracer(__name__)

app = FastAPI()

pinecone = db.PineconeStore()
postgres = db.PostgresStore()


@app.get("/")
async def root():
    return Response("Hello, World!")


@app.get("/calculate")
async def calculate():
    with tracer.start_as_current_span("fetch"):
        await pinecone.fetch()

    with tracer.start_as_current_span("calculate"):
        await simulate_latency(mean=0.5, stddev=0.1)

    return Response("I calculated something!")


instrument_app(app)
