WowBerg architecture instructions
=================================

This file contains the project-specific architecture and integration guidance
for WowBerg. Keep the generic Fullstack agent free of project-specific details
and include this file only when the task needs WowBerg context.

Architecture
- Remote backend: asynchronous ingestion, processing/storage, and quant layers
  must stay contract-first and flow inward through interfaces.
- Electron client: main-process caching and filesystem adapters stay separate
  from renderer UI and typed IPC contracts.
- WoW addon: treat the addon as a thin consumer of precomputed SavedVariables.

Usage
- Include this file when a task needs project-specific architecture guidance for
  the WowBerg backend, Electron client, or addon boundaries.
