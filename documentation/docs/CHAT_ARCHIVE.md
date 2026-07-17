# Preserving the original ChatGPT conversation

This repository contains a structured handoff, not a word-for-word copy of the entire ChatGPT conversation.

## Recommended two-layer archive

### 1. Keep the working chat in a ChatGPT Project

Create a project named `Veilshot`, move this conversation into it when the **Move to project** option is available, and add the latest source archive and key project documents. This keeps related chats, files, and project instructions together.

Recommended project instruction:

```text
Before changing Veilshot, read AGENTS.md, docs/PROJECT_CONTEXT.md,
docs/PRODUCT_REQUIREMENTS.md, docs/ARCHITECTURE.md, and docs/DECISION_LOG.md.
Preserve the intentionally small scope. Do not publish or run sudo without approval.
```

### 2. Export the raw account data

Use ChatGPT **Settings → Data controls → Export data**. The resulting ZIP contains chat history and account data. Keep it outside the public repository because it can contain unrelated and private conversations.

## Optional local archive

After receiving the export:

1. Store the original ZIP in a private backup location.
2. Extract `conversations.json` only in a private folder.
3. Do not commit the export to Git.
4. Add only a manually reviewed, redacted transcript if one is genuinely useful.

## Repository context files

For future coding work, use these instead of rereading the entire chat:

- `AGENTS.md`
- `docs/PROJECT_CONTEXT.md`
- `docs/PRODUCT_REQUIREMENTS.md`
- `docs/DECISION_LOG.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
