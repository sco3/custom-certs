# custom-certs

Small FastAPI HTTPS lab for checking how `httpx.AsyncClient` behaves with public TLS and a local self-signed certificate.

## Setup

```bash
uv sync
uv run generate-cert
```

## Run

Start the HTTPS server:

```bash
uv run run-server
```

In another terminal run the client:

```bash
uv run run-client
```

## What the client does

The client uses one `httpx.AsyncClient` with `mounts`:

- `https://127.0.0.1:8443` uses a transport that trusts `certs/localhost.crt`
- `https://` uses a transport that trusts the normal public CA bundle from `certifi`

So one client object routes requests to different transports.

## Observed behavior

Running the sample produced:

```text
mounted client ssl test
public: 200
local: 200
done
```

## Conclusion

- A single plain `httpx` transport/pool does not switch SSL context per request.
- A single `httpx.AsyncClient` can still talk to both endpoints if you use `mounts`.
- Each mounted transport has its own SSL context and its own connection pool.

## Files

- `server.py` — FastAPI app
- `generate_cert.py` — creates the self-signed certificate
- `run_server.py` — starts uvicorn with TLS
- `client.py` — async client test