from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
async def root():
    return Response("Hello, World!")
