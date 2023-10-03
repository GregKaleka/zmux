import re
from time import sleep

import click
from libtmux import Server, Window

TMUX_SESSION_NAME = "zmux"
TMUX_LAYOUT_SETTLE_SECS = 5
TMUX_PANE_SETTLE_SECS = 1


@click.group()
@click.version_option()
def cli():
    """A tmux parameterizer"""


def get_mapping_for_template(command_template):
    variables = re.findall(r"(?<!\\)\{(.+?)}", command_template)
    mapping = {}
    pane_count = 0
    for var in variables:
        vals = click.prompt(f"Supply {pane_count or 'up to 6'} values for {var}")
        vals_list = vals.replace(",", "").split(" ")
        val_count = len(vals_list)
        if val_count > 6:
            raise ValueError(
                f"NeuMux can send commands to a maximum of 6 apps simultaneously. Got {val_count}!"
            )
        if not pane_count:
            pane_count = val_count
        elif val_count != pane_count:
            raise ValueError(
                "You must supply the same number of values for each variable. "
                f"Expected {pane_count} but got {val_count}!"
            )
        mapping[var] = vals_list
    return mapping


@cli.command(name="launch")
@click.argument("command_template")
def launch(command_template):
    """Command description goes here"""
    mapping = get_mapping_for_template(command_template)

    first_set_of_values = next(iter(mapping.values()))
    pane_count = len(first_set_of_values)

    window = create_tmux_layout(pane_count)

    send_command_to_window_panes(window, command_template, mapping, num_panes=pane_count)

    window.session.attach_session()


def create_tmux_layout(num_panes: int) -> Window:
    """Create layout and panes in the window."""

    click.echo("\n💅 Creating tmux layout\n")
    tmux = Server()
    for live_session in tmux.sessions:
        if live_session.name == TMUX_SESSION_NAME:
            click.secho(f"Existing {TMUX_SESSION_NAME} session found! Killing.\n", fg="red")
            live_session.kill_session()
    session = tmux.new_session(TMUX_SESSION_NAME)
    window = session.attached_window
    pane = window.attached_pane
    split_vertically = [
        x % 2 == 0  # split every other pane vertically
        for x in range(num_panes - 1)  # but don't split the last pane at all
    ]

    for split_vert in split_vertically:
        pane = pane.split_window(vertical=split_vert)

    window.select_layout(layout="tiled")
    sleep(TMUX_LAYOUT_SETTLE_SECS)

    return window


def send_command_to_window_panes(
    window: Window, template: str, mapping: dict[str, list], num_panes: int
):
    """Send command to each pane in the window."""

    for idx in range(num_panes):
        sleep(TMUX_PANE_SETTLE_SECS)
        pane = window.panes[idx]
        click.echo(f"🚀 Sending command to pane {idx + 1}/{num_panes}")
        pane.send_keys("", enter=True)  # blank line required
        single_map = {variable: values[idx] for variable, values in mapping.items()}
        cmd = template.format(**single_map)
        pane.send_keys(cmd)

    click.echo("\n")
