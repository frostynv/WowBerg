
from data_service.blizzard_client import BlizzardOAuthClient
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

    ## Test code
    blizzard_client = BlizzardOAuthClient()
    token = blizzard_client.fetch_token()
    print("Fetched token:", token)




if __name__ == "__main__":
    main()
    



