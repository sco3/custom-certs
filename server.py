from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "custom-cert-server"}


@app.get("/echo/{value}")
async def echo(value: str) -> dict[str, str]:
    return {"echo": value}
