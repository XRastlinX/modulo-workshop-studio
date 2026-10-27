"""Guild-scoped, allowlisted slash-command adapter. No connection on import."""
import asyncio
import os
from pathlib import Path
import sys
import uuid

import discord
from discord import app_commands
from studio_core import modulo_walk

ROOT = Path(__file__).resolve().parent


def main():
    token = os.environ.get("DISCORD_BOT_TOKEN", "")
    guild_id = int(os.environ.get("DISCORD_GUILD_ID", "0"))
    allowed = {int(item.strip()) for item in os.environ.get("DISCORD_ALLOWED_USER_IDS", "").split(",") if item.strip()}
    if not token or guild_id <= 0 or not allowed:
        raise SystemExit("Required: DISCORD_BOT_TOKEN, DISCORD_GUILD_ID, DISCORD_ALLOWED_USER_IDS")
    guild = discord.Object(id=guild_id)

    class Workshop(discord.Client):
        def __init__(self):
            super().__init__(intents=discord.Intents.none())
            self.tree = app_commands.CommandTree(self)
            self.render_lock = asyncio.Lock()

        async def setup_hook(self):
            await self.tree.sync(guild=guild)

    client = Workshop()

    async def permitted(interaction):
        if interaction.guild_id != guild_id or interaction.user.id not in allowed:
            await interaction.response.send_message("This pilot is limited to its configured workshop members.", ephemeral=True)
            return False
        return True

    @client.tree.command(name="modulo", description="Show the whole turns and remainder", guild=guild)
    async def modulo(interaction: discord.Interaction, start: int = 10, steps: int = 5, modulus: int = 12):
        if not await permitted(interaction):
            return
        try:
            result = modulo_walk(start, steps, modulus)["final"]
        except ValueError as error:
            await interaction.response.send_message(str(error), ephemeral=True)
            return
        await interaction.response.send_message(
            f"{result['total']} = {result['quotient']} × {modulus} + {result['residue']}. "
            "The remainder alone does not identify the original total.", ephemeral=True)

    @client.tree.command(name="demo", description="Render a small clock demonstration as MP4", guild=guild)
    async def demo(interaction: discord.Interaction, start: int = 10, steps: int = 5, modulus: int = 12):
        if not await permitted(interaction):
            return
        try:
            modulo_walk(start, steps, modulus)
        except ValueError as error:
            await interaction.response.send_message(str(error), ephemeral=True)
            return
        if client.render_lock.locked():
            await interaction.response.send_message("The demonstration bench is busy. Try again after this render.", ephemeral=True)
            return
        await interaction.response.defer(ephemeral=True, thinking=True)
        async with client.render_lock:
            filename = f"renders/discord-{uuid.uuid4().hex}.mp4"
            process = await asyncio.create_subprocess_exec(
                sys.executable, str(ROOT / "render_demo.py"), "--start", str(start),
                "--steps", str(steps), "--modulus", str(modulus), "--output", filename,
                cwd=ROOT, stdout=asyncio.subprocess.DEVNULL, stderr=asyncio.subprocess.PIPE)
            try:
                _, error = await asyncio.wait_for(process.communicate(), timeout=120)
            except asyncio.TimeoutError:
                process.kill()
                await process.wait()
                await interaction.followup.send("Render exceeded its two-minute limit.", ephemeral=True)
                return
            if process.returncode:
                await interaction.followup.send("Render failed. Inspect the local environment and FFmpeg installation.", ephemeral=True)
                return
            target = ROOT / filename
            if target.stat().st_size > 8_000_000:
                await interaction.followup.send("Result exceeds the pilot's 8 MB upload limit; retained locally.", ephemeral=True)
                return
            await interaction.followup.send("Preview for your review; no social publication was performed.",
                                            file=discord.File(target), ephemeral=True)

    @client.tree.command(name="blueprint", description="Read the workshop blueprint", guild=guild)
    async def blueprint(interaction: discord.Interaction):
        if await permitted(interaction):
            await interaction.response.send_message(file=discord.File(ROOT / "SPEC.md"), ephemeral=True)

    client.run(token)


if __name__ == "__main__":
    main()
