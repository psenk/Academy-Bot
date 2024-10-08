import logging
import discord

from utils import Constants


def create_logger(filename: str) -> logging.Logger:
    logger = logging.getLogger(filename)
    if not logger.handlers:
        handler = logging.FileHandler(
            filename=f'logs/{filename}.log', encoding='utf-8', mode='w')
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
    return logger


def get_current_overseer(guild: discord.Guild) -> str:
    overseer_role = guild.get_role(Constants.TEST_OVERSEER_ROLE)
    overseer = overseer_role.members[0].display_name
    return overseer