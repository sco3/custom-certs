from generate_cert import CERT_PATH, KEY_PATH, generate_self_signed_cert


def ensure_cert_files() -> None:
    if not CERT_PATH.exists() or not KEY_PATH.exists():
        generate_self_signed_cert()


def main() -> None:
    ensure_cert_files()

    import uvicorn

    uvicorn.run(
        "server:app",
        host="127.0.0.1",
        port=8443,
        ssl_certfile=str(CERT_PATH),
        ssl_keyfile=str(KEY_PATH),
        log_level="info",
    )


if __name__ == "__main__":
    main()