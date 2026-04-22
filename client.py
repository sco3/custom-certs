import asyncio, ssl

import certifi, httpx


async def main():
    transport = httpx.AsyncHTTPTransport(
        verify=ssl.create_default_context(cafile=certifi.where()), retries=0
    )
    async with httpx.AsyncClient(transport=transport, timeout=10.0) as client:
        print("shared client ssl test")
        print(f"public: {(await client.get('https://jsonplaceholder.typicode.com/todos/1')).status_code}")
        try:
            print(f"local: {(await client.get('https://127.0.0.1:8443/health')).status_code}")
        except Exception as exc:
            print(f"local: {type(exc).__name__}")
        print("done")


if __name__ == "__main__":
    asyncio.run(main())
