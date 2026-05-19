
from fastapi import FastAPI
import uvicorn

def create_app() -> FastAPI:
    app = FastAPI(title="WowBerg API", version="0.1.0")

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()

def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()
    



