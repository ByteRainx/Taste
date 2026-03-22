"""Rich terminal output for taste reports."""

from __future__ import annotations

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel

from taste.data.models import TasteProfile
from taste.output.markdown import render_markdown


def print_profile(profile: TasteProfile) -> None:
    console = Console()
    md_text = render_markdown(profile)
    console.print()
    console.print(Panel(f"[bold]{profile.author.name}[/bold]", subtitle="Paper is cheap, show me the taste."))
    console.print()
    console.print(Markdown(md_text))
