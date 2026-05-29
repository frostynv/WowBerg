"""FastAPI application entrypoint for WowBerg."""

from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create the WowBerg HTTP application."""

    app = FastAPI(title="WowBerg API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()