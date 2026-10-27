"""Offline registration and deny/allow checks; no Discord network connection."""
import asyncio
import os
from types import SimpleNamespace
import unittest
from unittest.mock import AsyncMock, patch
import discord_bot


class AdapterChecks(unittest.TestCase):
    def test_requires_explicit_configuration(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(SystemExit):
                discord_bot.main()

    def test_guild_commands_and_allowlist(self):
        captured = []
        with patch.dict(os.environ, {"DISCORD_BOT_TOKEN": "offline-placeholder", "DISCORD_GUILD_ID": "123", "DISCORD_ALLOWED_USER_IDS": "456"}, clear=True):
            with patch("discord.Client.run", lambda client, token: captured.append(client)):
                discord_bot.main()
        client = captured[0]
        commands = {c.name: c for c in client.tree.get_commands(guild=discord_bot.discord.Object(id=123))}
        self.assertEqual(set(commands), {"modulo", "demo", "blueprint"})
        self.assertEqual(client.tree.get_commands(), [])

        async def checks():
            for guild_id, user_id in [(999, 456), (123, 999)]:
                response = SimpleNamespace(send_message=AsyncMock())
                interaction = SimpleNamespace(guild_id=guild_id, user=SimpleNamespace(id=user_id), response=response)
                await commands["modulo"].callback(interaction, 10, 5, 12)
                self.assertIn("limited", response.send_message.call_args.args[0])
            response = SimpleNamespace(send_message=AsyncMock())
            interaction = SimpleNamespace(guild_id=123, user=SimpleNamespace(id=456), response=response)
            await commands["modulo"].callback(interaction, 10, 5, 12)
            self.assertIn("15 = 1 × 12 + 3", response.send_message.call_args.args[0])
        asyncio.run(checks())
