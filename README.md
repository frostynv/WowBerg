# WowBerg
Bloomberg Terminal for World of Warcraft


## Documentation
https://community.developer.battle.net/documentation/world-of-warcraft

## AI Context
Copilot project instructions are in .github/copilot-instructions.md so chat responses can consistently use the WoW API documentation context.

## Copilot Customization Structure
- Always-on instructions: `.github/copilot-instructions.md`
- Shared agent operating guide: `.github/AGENTS.md`
- File-scoped instructions: `.github/instructions/*.instructions.md`
- Reusable slash prompts: `.github/prompts/*.prompt.md`
- Specialist agents: `.github/agents/*.agent.md`
- Runtime policy hooks: `.github/hooks/*.json`

## Docker Environment
### Services
- `api`: FastAPI backend on `http://localhost:8000`
- `db`: TimescaleDB/PostgreSQL on `localhost:5432`

### Start
```bash
docker compose up --build
```

### Start With Watch (Auto Sync + Reload)
```bash
docker compose watch
```

This syncs `src/` changes into the running container and automatically reloads the API process.

### Verify
Open:
- `http://localhost:8000/health`
- `http://localhost:8000/docs`

### Stop
```bash
docker compose down
```
