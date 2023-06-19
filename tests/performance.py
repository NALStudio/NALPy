from timeit import timeit
from typing import NamedTuple
from nalpy.math import Vector2, _Legacy_Vector2
from nalpy.console_utils import set_foreground_color, set_background_color, reset_attributes, ConsoleColor, set_style, ConsoleStyle

setup: str = "x=Vector2(69.0, 420.0); y=Vector2(-4.0, -5.0)"
commands: tuple[str, ...] = (
#     "Vector2(0.0, 0.0)",
#     "Vector2.zero",
#     "x[0]",
#     "x[1]",
#     "x.x",
#     "x.y",
#     "x + y",
#     "x - y",
#     "x * y",
    "x * 2",
    "2 * x",
#     "x / y",
#     "x / 2",
#     "x // y",
#     "x // 2",
#     "x % y",
#     "x % 2",
#     "divmod(x, y)",
#     "divmod(x, 2)",
#     "-x",
#     "abs(x)",
#     "abs(y)",
#     "x == x",
#     "x == y",
#     "x.magnitude",
#     "x.normalized",
#     "Vector2.dot(x, y)",
#     "Vector2.lerp(x, y, 0.5)",
#     "Vector2.lerp_unclamped(x, y, 1.5)",
#     "Vector2.move_towards(y, x, 15.5)",
#     "Vector2.perpendicular(x)",
#     "Vector2.reflect(x, y)",
#     "Vector2.angle(x, y)",
#     "Vector2.signed_angle(x, y)",
#     "Vector2.distance(x, y)",
#     "Vector2.min(x, y)",
#     "Vector2.max(x, y)",
)

class Configuration(NamedTuple):
    name: str
    Vector2Implementation: type

configurations: tuple[Configuration, ...] = (
#     Configuration("Old Vector2", _Legacy_Vector2),
    Configuration("New Vector2", Vector2),
)

n = 1_000_000
runs = 50

DELIM: str = 75 * "-"

def run_cmd(cmd: str, config: Configuration, index: int, total: int) -> float:
    secs = timeit(cmd, setup=setup, globals={"Vector2": config.Vector2Implementation}, number=n)
    print(f"({index + 1} / {total}) {config.name}: {secs} seconds for {n} repetitions")
    return secs

class CommandRan(NamedTuple):
    command: str
    config_run_seconds: tuple[tuple[Configuration, float], ...]

    def get_percent_faster(self) -> tuple[Configuration, Configuration, float]:
        """Returns the slowest and fastest configurations and the percentage of which the fastest configuration is faster than the slowest."""
        slowest_config, slowest_time = max(self.config_run_seconds, key=lambda s: s[1])
        fastest_config, fastest_time = min(self.config_run_seconds, key=lambda s: s[1])
        percent_faster: float = (1 - (fastest_time / slowest_time)) * 100
        return (slowest_config, fastest_config, percent_faster)

cmds_ran: list[CommandRan] = []

for i, cmd in enumerate(commands):
    print(f"Command: {cmd} ({i + 1} / {len(commands)})")
    configruns: list[tuple[Configuration, float]] = []
    for config in configurations:
        runsofthisconfig: list[float] = []
        for i in range(runs):
            timetaken_seconds: float = run_cmd(cmd, config, i, runs)
            runsofthisconfig.append(timetaken_seconds)
        configruns.append((config, min(runsofthisconfig)))

    cmds_ran.append(CommandRan(cmd, tuple(configruns)))
    print(DELIM)

ran_sorted: tuple[CommandRan, ...] = tuple(sorted(cmds_ran, key=lambda r: r.get_percent_faster()))

def value_to_console_color(value: float):
    if value > 0.0:
        return ConsoleColor.GREEN
    if value < 0.0:
        return ConsoleColor.RED
    return ConsoleColor.YELLOW

for run in ran_sorted:
    set_foreground_color(ConsoleColor.CYAN)
    set_style(ConsoleStyle.BOLD)
    print(run.command, end="")
    reset_attributes()
    print()
    for config, seconds in run.config_run_seconds:
        print(f"{config.name}: {seconds} seconds / {n} runs")
    slowest_config, fastest_config, percent_faster = run.get_percent_faster()
    set_foreground_color(value_to_console_color(percent_faster))
    print(f"{percent_faster}% faster ({slowest_config.name} => {fastest_config.name})", end="")
    reset_attributes()
    print("\n" + DELIM)
