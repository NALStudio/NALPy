from __future__ import annotations as _annotations
from enum import Enum as _Enum
import platform as _platform

class OSPlatform(_Enum):
    WINDOWS = "Windows"
    LINUX = "Linux"
    MAC_OS = "Darwin"
    JAVA = "Java"

    @property
    def value(self) -> str:
        """The platform system name"""
        val = super().value
        assert isinstance(val, str)
        return val

def get_os_platform() -> OSPlatform:
    return OSPlatform(_platform.system())

def is_os_platform(os_platform: OSPlatform) -> bool:
    return _platform.system() == os_platform.value
