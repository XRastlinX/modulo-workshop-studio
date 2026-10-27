# Technical sources

Consulted 2026-10-27. These document API behavior; they do not validate this implementation.

- Python divmod: https://docs.python.org/3/library/functions.html#divmod
- MCP Python SDK v1 compatibility documentation: https://py.sdk.modelcontextprotocol.io/v1/
- SDK transport reference: https://github.com/modelcontextprotocol/python-sdk/blob/main/docs/run/index.md
- FFmpeg CLI: https://www.ffmpeg.org/ffmpeg.html
- discord.py command tree: https://discordpy.readthedocs.io/en/stable/interactions/api.html
- Official discord.py example: https://github.com/Rapptz/discord.py/blob/master/examples/app_commands/basic.py
- Discord guild install scopes: https://github.com/discord/discord-api-docs/blob/main/developers/quick-start/getting-started.mdx
- Community creation: https://support.reddithelp.com/hc/en-us/articles/15484258409492-How-to-create-a-community
- Reddit spam policy: https://support.reddithelp.com/hc/en-us/articles/360043504051-Spam

Dependency targets: MCP 1.30.0 (deliberately v1 API), Pillow 12.3.0, optional discord.py 2.7.1. Python dependencies are pinned directly; transitive dependency resolution and FFmpeg builds can vary.
