# Discord: the shared demonstration bench

Name: **Modulo Workshop**. Bot working name: **Remainder**. Tone: dry cosmic bureaucracy, original language and artwork. Tagline: “The universe has returned a remainder. Please retain your workings.”

State: adapter written, not connected or tested against a live Discord server. Scope: three slash commands. Visual anchor: README.md, including upload boundary and unresolved live behavior.

vocational_verb: DRAFT
recommendation_effect: ADVISORY_ONLY
automatic_execution: FORBIDDEN
residual_posture: OPEN_ACKNOWLEDGED
sovereign_boundary: EXTERNAL_HUMAN_DISPOSITION_REQUIRED
authority_effect: NONE
crown: DETACHED

| Server area | Candidate purpose | Status |
|---|---|---|
| #arrivals | Purpose, rules, first example | Proposed, absent |
| #the-bench | Slash-command experiments | Proposed, absent |
| #build-blueprints | Git links and bounded briefs | Proposed, absent |
| #show-your-work | Peer demonstrations and counterexamples | Proposed, absent |
| #screening-room | Reviewed episode and music links | Proposed, absent |

Text equivalent: a welcome area leads to experiments, repository briefs, peer checks and reviewed media. Channels are candidate organization, not an existing server or a permission map. Credentials and public posting remain separate from this proposal.

## Setup interface

The [Discord Developer Portal](https://discord.com/developers/applications) supplies the application and bot credentials. This adapter uses a guild installation with `bot` and `applications.commands` scopes. Minimum bot channel permissions: View Channel, Send Messages and Attach Files; no Administrator permission or privileged message-content intent. The human installation flow determines the destination server and permissions.

Optional dependency command:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-discord.txt
```

Required process environment variables:

| Variable | Meaning |
|---|---|
| DISCORD_BOT_TOKEN | Secret supplied locally; never pasted into a chat or Git |
| DISCORD_GUILD_ID | One server's numeric ID |
| DISCORD_ALLOWED_USER_IDS | Comma-separated numeric member IDs; empty means startup refusal |

Entrypoint: `.\.venv\Scripts\python.exe discord_bot.py`. Starting it registers the three guild commands with Discord and maintains a gateway connection. `/demo` uploads a generated MP4 privately to the invoking allowlisted member through Discord; this is an external transmission. `/blueprint` uploads this repository's SPEC.md. No Reddit/YouTube publication exists in the bot.

`/modulo start:10 steps:5 modulus:12` returns the identity. `/demo` produces the matching silent video. `/blueprint` returns the AI-readable brief. The configured member can inspect the preview before separately sharing it.

Pilot limitations: no durable queue, no per-member daily quota, no scheduled file cleanup, no agent-generated code execution, no narration. Live command registration, denied-user behavior, attachment delivery and reconnect behavior remain unverified. Locally generated artifacts stay in ignored `renders/` until the operator handles retention.
