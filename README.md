# WowBerg
Bloomberg Terminal for World of Warcraft


## Documentation
https://community.developer.battle.net/documentation/world-of-warcraft

## AI Context
Copilot project instructions are in [.github/copilot-instructions.md](.github/copilot-instructions.md).
Use [.github/instructions/wowberg-architecture.instructions.md](.github/instructions/wowberg-architecture.instructions.md)
for WowBerg architecture guidance.

## Copilot Customization Structure
- Always-on instructions: `.github/copilot-instructions.md`
- Shared agent operating guide: `.github/AGENTS.md`
- File-scoped instructions: `.github/instructions/*.instructions.md`
- Agent skills: `.github/skills/*/SKILL.md`
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
