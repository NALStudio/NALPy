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
#     "x * 2",
#     "2 * x",
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
    "Vector2.angle(x, y)",
    "Vector2.signed_angle(x, y)",
#     "Vector2.distance(x, y)",
#     "Vector2.min(x, y)",
#     "Vector2.max(x, y)",
)
n = 2500
runs = 10000

DELIM: str = 75 * "-"

def run_oldv2_cmd(cmd: str) -> float:
    old_v = timeit(cmd, setup=setup, globals={"Vector2": _Legacy_Vector2}, number=n)
    print(f"Old Vector2: {old_v} seconds for {n} repetitions")
    return old_v

def run_newv2_cmd(cmd: str) -> float:
    new_v = timeit(cmd, setup=setup, globals={"Vector2": Vector2}, number=n)
    print(f"New Vector2: {new_v} seconds for {n} repetitions")
    return new_v

class CommandRan(NamedTuple):
    command: str
    oldspeed: float
    newspeed: float

    @property
    def percent_faster(self) -> float:
        return (1 - (self.newspeed / self.oldspeed)) * 100

cmds_ran: list[CommandRan] = []

for i, cmd in enumerate(commands):
    print(f"Command: {cmd} ({i + 1} / {len(commands)})")
    old_runs: list[float] = []
    for _ in range(runs):
        old_runs.append(run_oldv2_cmd(cmd))

    new_runs: list[float] = []
    for _ in range(runs):
        new_runs.append(run_newv2_cmd(cmd))

    cmds_ran.append(CommandRan(cmd, min(old_runs), min(new_runs)))
    print(DELIM)

ran_sorted: tuple[CommandRan, ...] = tuple(sorted(cmds_ran, key=lambda r: r.percent_faster))

for run in ran_sorted:
    set_foreground_color(ConsoleColor.CYAN)
    set_style(ConsoleStyle.BOLD)
    print(run.command, end="")
    reset_attributes()
    print()
    print(f"{run.oldspeed} seconds / {n} runs")
    print(f"{run.newspeed} seconds / {n} runs")
    set_foreground_color(ConsoleColor.GREEN if run.percent_faster > 0.0 else ConsoleColor.RED)
    print(f"{run.percent_faster} % faster", end="")
    reset_attributes()
    print("\n" + DELIM)
