import asyncio
import random


async def simulate_latency(*, mean: float, stddev: float):
    latency = random.normalvariate(mean, stddev)
    await asyncio.sleep(latency)
