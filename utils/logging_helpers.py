import os
import sys
import time
from pathlib import Path

from loguru import logger

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "bot.log"

logger.remove()

logger.add(
    sys.stdout,
    level="INFO",
    colorize=True,
    format="<green>[{time:YYYY-MM-DD HH:mm:ss}]</green> <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

logger.add(
    LOG_FILE,
    level="DEBUG",
    format="[{time:YYYY-MM-DD HH:mm:ss}] [{level}] {name}:{function}:{line} - {message}",
    rotation="5 MB",
    retention=10,
    compression="zip",
    backtrace=True,
    diagnose=True,
)

if os.getenv("DEBUG_MODE", "0") == "1":
    logger.level("DEBUG")
else:
    logger.level("INFO")

logger.disable("discord")


def setup_command_hooks(bot):
    @bot.before_invoke
    async def before_command(ctx):
        ctx.command_start = time.perf_counter()
        logger.info("Command '{}' started by {}", ctx.command, ctx.author)

    @bot.after_invoke
    async def after_command(ctx):
        duration = time.perf_counter() - ctx.command_start
        logger.info("Command '{}' finished in {:.2f}s", ctx.command, duration)

    @bot.event
    async def on_command_error(ctx, error):
        logger.error("Error in command '{}': {}", ctx.command, error, exc_info=True)


def log_cog_load_success(name):
    logger.info("Loaded cog: {}", name)


def log_cog_load_failure(name, error):
    logger.error("Failed to load cog '{}': {}", name, error, exc_info=True)


def log_cog_add_success(cog_name: str):
    logger.info("Successfully loaded extension: {}", cog_name)


def log_cog_add_failure(cog_instance_or_name, error):
    name = cog_instance_or_name.__class__.__name__ if not isinstance(cog_instance_or_name, str) else cog_instance_or_name
    logger.error("Failed to add cog '{}': {}", name, error, exc_info=True)


def log_api_call(name):
    logger.debug("Calling external API: {}", name)


def log_api_response(name, status):
    logger.debug("API '{}' responded with status {}", name, status)


def log_api_failure(name, error):
    logger.error("API '{}' call failed: {}", name, error, exc_info=True)
