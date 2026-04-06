"""
ReverseBottom CLI — entry point.

Usage:
    reversebottom                          # interactive mode
    reversebottom --mode destroy "idea"   # direct input
    reversebottom --mode shadow --json    # JSON output
    reversebottom serve                   # start API server
"""

from __future__ import annotations

import json
import sys
from typing import Annotated

import typer
from rich import print as rprint
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Confirm, Prompt
from rich.rule import Rule
from rich.text import Text
from rich.theme import Theme

from .config import Mode, get_settings
from .router import Router

# ── terminal theme ────────────────────────────────────────────────────────────

THEME = Theme(
    {
        "destroy": "bold red",
        "reverse": "bold cyan",
        "shadow": "bold yellow",
        "label": "dim white",
        "error": "bold red",
        "muted": "dim",
    }
)

console = Console(theme=THEME)
app = typer.Typer(
    name="reversebottom",
    help="An anti-assistant. It will not help you feel better about your ideas.",
    add_completion=False,
    no_args_is_help=False,
    rich_markup_mode="rich",
)

# ── helpers ───────────────────────────────────────────────────────────────────

MODE_COLORS: dict[Mode, str] = {
    Mode.DESTROY: "destroy",
    Mode.REVERSE: "reverse",
    Mode.SHADOW: "shadow",
}

MODE_LABELS: dict[Mode, str] = {
    Mode.DESTROY: "DESTROY",
    Mode.REVERSE: "REVERSE",
    Mode.SHADOW: "SHADOW",
}

MODE_DESCRIPTIONS: dict[Mode, str] = {
    Mode.DESTROY: "Find every flaw, contradiction, and risk",
    Mode.REVERSE: "Invert core assumptions and rebuild the logic",
    Mode.SHADOW: "Surface hidden motives, biases, and blind spots",
}


def _print_header() -> None:
    console.print()
    console.print(
        Panel.fit(
            "[bold white]REVERSEBOTTOM[/bold white]\n[dim]An anti-assistant.[/dim]",
            border_style="dim white",
            padding=(0, 2),
        )
    )
    console.print()


def _print_mode_selection() -> Mode:
    console.print("[label]Select mode:[/label]")
    console.print()

    for i, mode in enumerate(Mode, 1):
        color = MODE_COLORS[mode]
        label = MODE_LABELS[mode]
        desc = MODE_DESCRIPTIONS[mode]
        console.print(f"  [{color}][{i}] {label}[/{color}]  [dim]{desc}[/dim]")

    console.print()

    choice = Prompt.ask(
        "[label]Mode[/label]",
        choices=["1", "2", "3"],
        default="1",
    )

    return list(Mode)[int(choice) - 1]


def _print_result(mode: Mode, output: str) -> None:
    color = MODE_COLORS[mode]
    label = MODE_LABELS[mode]

    console.print()
    console.print(Rule(f"[{color}]{label} MODE[/{color}]", style=color))
    console.print()
    console.print(output)
    console.print()
    console.print(Rule(style="dim white"))
    console.print()


def _run_analysis(
    text: str,
    mode: Mode,
    output_json: bool = False,
) -> None:
    settings = get_settings()
    router = Router()

    with console.status(
        f"[{MODE_COLORS[mode]}]Analyzing with {MODE_LABELS[mode]} mode...[/{MODE_COLORS[mode]}]",
        spinner="dots",
    ):
        result = router.run(text, mode)

    if output_json:
        payload = {
            "mode": result.mode.value,
            "input": result.input_text,
            "output": result.output,
        }
        typer.echo(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    _print_result(mode, result.output)


# ── commands ──────────────────────────────────────────────────────────────────


@app.command(name="analyze", help="Analyze text in the specified mode.", invoke_without_command=True)
def analyze(
    text: Annotated[
        str | None,
        typer.Argument(help="Text to analyze. If omitted, enter interactive mode."),
    ] = None,
    mode: Annotated[
        Mode | None,
        typer.Option("--mode", "-m", help="Operating mode: destroy, reverse, shadow."),
    ] = None,
    output_json: Annotated[
        bool,
        typer.Option("--json", "-j", help="Output raw JSON instead of formatted text."),
    ] = False,
) -> None:
    # ── interactive mode ──────────────────────────────────────────────────────
    if text is None or text.strip() == "":
        # check if we're reading from a pipe
        if not sys.stdin.isatty():
            text = sys.stdin.read().strip()
            if not text:
                console.print("[error]No input provided.[/error]")
                raise typer.Exit(1)
        else:
            _print_header()
            console.print("[label]Enter your idea, argument, or decision:[/label]")
            console.print("[muted](Press Enter twice when done)[/muted]")
            console.print()

            lines: list[str] = []
            try:
                while True:
                    line = input()
                    if line == "" and lines and lines[-1] == "":
                        break
                    lines.append(line)
            except EOFError:
                pass

            text = "\n".join(lines).strip()

            if not text:
                console.print("[error]No input provided.[/error]")
                raise typer.Exit(1)

    # ── mode selection ────────────────────────────────────────────────────────
    if mode is None:
        if sys.stdin.isatty():
            _print_header()
            mode = _print_mode_selection()
        else:
            mode = get_settings().default_mode

    # ── run ───────────────────────────────────────────────────────────────────
    try:
        _run_analysis(text, mode, output_json)
    except ValueError as e:
        console.print(f"[error]Configuration error: {e}[/error]")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[error]Error: {e}[/error]")
        raise typer.Exit(1) from e


@app.command(name="serve", help="Start the ReverseBottom API server.")
def serve(
    host: Annotated[str, typer.Option("--host", help="Host to bind to.")] = "127.0.0.1",
    port: Annotated[int, typer.Option("--port", help="Port to listen on.")] = 8000,
    reload: Annotated[bool, typer.Option("--reload", help="Enable auto-reload (dev only).")] = False,
) -> None:
    import uvicorn

    console.print(f"[dim]Starting server at http://{host}:{port}[/dim]")
    uvicorn.run(
        "reversebottom.api:api_app",
        host=host,
        port=port,
        reload=reload,
    )


@app.command(name="modes", help="List all available modes and their descriptions.")
def list_modes() -> None:
    _print_header()
    for mode in Mode:
        color = MODE_COLORS[mode]
        label = MODE_LABELS[mode]
        desc = MODE_DESCRIPTIONS[mode]
        console.print(f"[{color}]{label}[/{color}]")
        console.print(f"  [dim]{desc}[/dim]")
        console.print()


# ── entry point ───────────────────────────────────────────────────────────────


def main() -> None:
    app()


if __name__ == "__main__":
    main()
