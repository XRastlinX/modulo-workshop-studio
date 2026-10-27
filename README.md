# Modulo Workshop

**Odd ideas. Small experiments. Inspectable results.**

A starter studio for soft tek, agent tools and short MP4 explanations. Its first demonstration separates a number from its remainder: 10 + 5 lands at 3 on a twelve-position dial, while the full total remains 15.

The command-driven Discord interface recalls the shared workshop experience of early generative bots. The output here is an explanation you can inspect, with the calculation alongside the picture.

## Current artifact and boundaries

Artifact: Modulo Workshop starter, 2026-10-27. Scope: local integer demonstration, MP4 renderer, two MCP tools, optional Discord adapter. State: source written; observed verification in ACCEPTANCE.md. Diagram arrows describe code paths, not proof or permission.

```text
Episode question -> integer model -> checks -> local MP4 + receipt
                         ^
MCP host --------------- |  two calculation/inspection tools
Discord /modulo -------- |  calculation reply
Discord /demo ----------> bounded local render -> private preview upload
Discord /blueprint -----> SPEC.md attachment

Human review .......> Reddit / YouTube / other publication
```

Solid arrows: implemented paths, Discord requires configuration and a live connection. Dotted arrow: external publication, absent from the bot and MCP server. Open residuals: live Discord behavior, audience comprehension, narration, captions, moderation, retention and multi-user load. Text equivalent: all interfaces share one arithmetic model; only the optional Discord adapter can upload its generated preview to its configured server. No interface publishes to Reddit or YouTube. Visual presence carries no authority.

## Windows command reference

Python 3.11+ and FFmpeg/ffprobe with libx264 are prerequisites. This machine's observed environment was Python 3.14.4 and FFmpeg 9.0.1. These commands describe the setup interface; they do not connect a social account.

```powershell
git clone https://github.com/XRastlinX/modulo-workshop-studio.git
cd modulo-workshop-studio
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe tests\mcp_smoke.py
.\.venv\Scripts\python.exe render_demo.py
```

The render produces `renders/modulo-clock.mp4` and a JSON receipt with its hash and media checks. Existing outputs are preserved; `--output renders/another-name.mp4` selects a new name. Each position lasts two seconds, with no narration or music. Negative steps work too.

## MCP interface

`server.py` is a local stdio MCP server pinned to SDK v1.30.0. A host's configuration syntax varies. Its executable is this checkout's `.venv/Scripts/python.exe`, its sole argument is the absolute path to `server.py`, and its working directory is this checkout. No host has been connected by this repository.

- `demonstrate_modulo(start, steps, modulus)`: bounded integer calculation.
- `inspect_episode_plan(plan)`: required-field inspection. Presence of fields does not verify their claims.

Neither tool can render video, execute shell input or publish. The video CLI and optional Discord adapter are separate interfaces.

## Episode format

Each episode record carries a question, why it matters, demonstration, check, challenge, sources and unresolved questions. `examples/episode-01.json` is a real example. A possible falsifier must address the actual claim: for this episode a wrong quotient/remainder identity or mislabeled dial would count. This is a finite educational example, with no claim about P versus NP.

## Repository map

`SPEC.md` is the AI build brief; `AGENTS.md` gives contributor boundaries; `DISCORD.md` describes the optional bot and server layout; `COMMUNITY.md` contains the public introduction and community description. No open-source license has been selected.

Advisory design declaration: vocational_verb: DRAFT; recommendation_effect: ADVISORY_ONLY; automatic_execution: FORBIDDEN; residual_posture: OPEN_ACKNOWLEDGED; sovereign_boundary: EXTERNAL_HUMAN_DISPOSITION_REQUIRED; authority_effect: NONE; crown: DETACHED. Explicit human requests are separate authorization sources.
