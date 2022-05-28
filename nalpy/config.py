from __future__ import annotations

import json
import os
import re

from nalpy import logging


class Config:
    def __init__(self) -> None:
        """Instantiate config with default settings"""
        self.fullscreen: bool = False
        self.window_w: int = 1280
        self.window_h: int = 720
        self.window_resizable: bool = True
        self.vsync: bool = False
        self.hardware_acceleration: bool = True

        self.volume_master: float = 0.5
        self.volume_effects: float = 1.0
        self.volume_music: float = 1.0
        self.volume_ambience: float = 1.0
        self.volume_ui: float = 1.0

        self.sdl2_experimental: bool = False

    @classmethod
    @property
    def default(cls):
        return cls()

    @staticmethod
    def load(config_path: str) -> Config:
        """Load config with settings from filepath json"""

        def remove_available_comment(content: str) -> str:
            content_parts = content.split("{")
            content_start = re.sub(r"/\*.*?\*/", "", content_parts[0], flags=re.DOTALL)
            content_end = "{" + "{".join(content_parts[1:])
            return content_start + content_end

        data: dict[str, str | int | float | bool]
        if os.path.isfile(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                content = remove_available_comment(f.read())
                data = json.loads(content)
        else:
            logging.warning(f"No config found on path: '{config_path}'\nUsing default settings.", stack_info=False)
            data = {}

        assert isinstance(data, dict)

        conf: Config = Config()
        for k, v in data.items():
            original_value = getattr(conf, k, None)
            if original_value is None:
                logging.error(f"No key '{k}' found to assign value '{v}'")
                continue
            if not isinstance(v, type(original_value)):
                logging.error(f"Value '{v}' cannot be assigned to key '{k}' with value '{original_value}' and will be skipped", True)
                continue

            setattr(conf, k, v)

        return conf

    @staticmethod
    def save(config: Config, config_path: str) -> None:
        default = Config()

        to_save: dict[str, str | int | float | bool] = {}
        for k, v in config.__dict__.items():
            if k.startswith("_"):
                continue
            if getattr(default, k) == v:  # If value is same as default
                continue

            to_save[k] = v

        with open(config_path, "w", encoding="utf-8") as f:
            json_str = json.dumps(to_save, indent=4)
            available_settings = Config._generate_available_settings()
            f.write(f"/*\n{available_settings}\n*/\n{json_str}")

    @staticmethod
    def _generate_available_settings() -> str:
        out = "Available settings (json):\n"
        for k, v in Config().__dict__.items():
            if k.startswith("_"):
                continue

            out += f"\n{k}: {type(v).__name__} (Default: {v})"

        return out


current: Config


def init():
    global current
    current = Config.load(constants.Paths.CONFIG_FILE)


def save():
    Config.save(current, constants.Paths.CONFIG_FILE)

# TODO: Save system
# Save Files are map files when extension is changed to '.laudaturmap'
#
# Save File Structure:
#     ↳ save_0.penis (.zip)
#        ↳ chunk_{x}_{y}.dat (binary)
#            ↳ tiles (list[list[Tile]])
#            ↳ items (list[Item])
#            ↳ entities
#                ↳ explosions
#                ↳ ballistic objects & projectiles
#                ↳ enemies
#         ↳ world.json
#             ↳ Players (list)
#                 ↳ position (tuple[float, float])
#                 ↳ health (float[0, 1])
#                 ↳ stamina (float[0, 1])
#                 ↳ inventory (tuple[Item])
#             ↳ Game
#                 ↳ schedule
#                 ↳ time of day
#                 ↳ day # If we want to make this a papers please -ish game
