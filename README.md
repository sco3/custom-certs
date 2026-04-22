# custom-certs

Minimal FastAPI HTTPS lab for testing whether one `httpx.Client` with a shared connection pool/transport can make requests using different SSL trust contexts.

## What it does

- starts a local FastAPI server on `https://127.0.0.1:8443`
- generates a self-signed certificate for `localhost` and `127.0.0.1`
- uses one explicit `httpx.HTTPTransport` inside one `httpx.Client`
- sends one request to a public HTTPS API
- sends one request to the local HTTPS server
- passes different `verify=` SSL contexts per request to investigate trust-store behavior

## Project files

- `server.py` - FastAPI app
- `generate_cert.py` - self-signed certificate generator
- `run_server.py` - HTTPS server launcher
- `client.py` - SSL context experiment client

## Setup with uv

```bash
uv sync
```

## Generate certificate

```bash
uv run generate-cert
```

## Run the HTTPS server

```bash
uv run run-server
```

## Run the client experiment

In another terminal:

```bash
uv run run-client
```

## Expected investigation outcome

The client is intentionally written to reuse one explicit `httpx` transport while sending requests with two different SSL contexts:

- public CA context for `https://jsonplaceholder.typicode.com`
- custom trust context for `https://127.0.0.1:8443`

If `httpx` honors per-request `verify=` with the shared transport, both positive requests should succeed, while the negative cross-usage checks should fail with certificate verification errors.
