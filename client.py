import asyncio, ssl

import certifi, httpx
import ctx


class ClientManager:
    def __init__(self):
        self._clients = {
            "default": httpx.AsyncClient(
                verify=ssl.create_default_context(cafile=certifi.where()), timeout=10.0
            )
        }

    async def get_client(self, context_id="default", **kwargs):
        if context_id not in self._clients:
            self._clients[context_id] = httpx.AsyncClient(timeout=10.0, **kwargs)
        return self._clients[context_id]

    async def shutdown(self):
        for client in self._clients.values():
            await client.aclose()


async def async_main():
    manager = ClientManager()
    try:
        client = await manager.get_client()
        print("client manager ssl test")
        print(f"public: {(await client.get('https://jsonplaceholder.typicode.com/todos/1')).status_code}")

        try:
            print(f"local before new client: {(await client.get('https://127.0.0.1:8443/health')).status_code}")
        except Exception as exc:
            print(f"local before new client: {type(exc).__name__}")

        client = await manager.get_client(
            "local", verify=ssl.create_default_context(cafile="certs/localhost.crt")
        )
        print(f"local after new client: {(await client.get('https://127.0.0.1:8443/health')).status_code}")
        print(f"default ssl contexts created: {ctx.SSLValidator.count}")
    finally:
        await manager.shutdown()


def main():
    asyncio.run(async_main())


if __name__ == "__main__":
    main()