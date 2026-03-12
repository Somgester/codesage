"""Command-line interface for CodeSage."""

from rich.console import Console

console = Console()


def main() -> None:
    """Entry point for CodeSage CLI."""
    console.print("[bold green]CodeSage[/bold green] - AI Codebase Intelligence System v1.0.0")
    console.print("Use 'codesage --help' for available commands.")


if __name__ == "__main__":
    main()
