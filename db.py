import asyncio
from opentelemetry import trace

from latency import simulate_latency


tracer = trace.get_tracer(__name__)


class PineconeStore:
    @tracer.start_as_current_span("pinecone.fetch")
    async def fetch(self):
        # TODO: simulate sporadic latency
        await simulate_latency(mean=1, stddev=0.5)


class PostgresStore:
    @tracer.start_as_current_span("postgres.fetch")
    async def fetch(self):
        await simulate_latency(mean=0.2, stddev=0.1)
