"""FastAPI application entrypoint for WowBerg."""

from fastapi import FastAPI


def run_api() -> FastAPI:
    """Create the WowBerg HTTP application."""

    app = FastAPI(title="WowBerg API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = run_api()



if __name__ == "__main__":
    run_api()         
                
__all__ = ["run_api"]