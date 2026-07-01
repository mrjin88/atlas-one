"""Prompt template loader for Atlas ONE."""

from __future__ import annotations

from pathlib import Path


class PromptNotFoundError(FileNotFoundError):
    """Raised when a prompt template file does not exist."""


class PromptVariableError(KeyError):
    """Raised when required template variables are missing."""


class PromptLoader:
    """Loads and renders Markdown prompt templates from the prompts directory.

    Templates use Python ``str.format()`` syntax for variable substitution.
    """

    def __init__(self, prompts_dir: str | Path | None = None) -> None:
        if prompts_dir is None:
            prompts_dir = (
                Path(__file__).resolve().parents[1] / "prompts"
            )
        self._prompts_dir = Path(prompts_dir)

    def load(self, name: str, **variables: str) -> str:
        """Load a prompt template and render it with the given variables.

        Args:
            name: The template filename without extension (e.g. ``research``).
            **variables: Key-value pairs for ``{variable}`` placeholders.

        Returns:
            The rendered prompt text.

        Raises:
            PromptNotFoundError: If the template file does not exist.
            PromptVariableError: If the template contains placeholders
                that were not provided.
        """
        path = self._prompts_dir / f"{name}.md"
        if not path.exists():
            raise PromptNotFoundError(
                f"Prompt template '{name}' not found at: {path}"
            )

        template = path.read_text(encoding="utf-8")

        try:
            return template.format(**variables)
        except KeyError as exc:
            raise PromptVariableError(
                f"Missing template variable: {exc}"
            ) from exc
