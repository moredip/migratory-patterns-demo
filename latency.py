import asyncio
from opentelemetry import trace
import random

tracer = trace.get_tracer(__name__)


async def simulate_latency(*, mean: float, stddev: float):
    latency = random.normalvariate(mean, stddev)

    with tracer.start_as_current_span("simulate_latency") as span:
        span.set_attributes(
            {
                "latency.simulated_secs": latency,
                "latency.mean_secs": mean,
                "latency.stddev": stddev,
            }
        )

        await asyncio.sleep(latency)
