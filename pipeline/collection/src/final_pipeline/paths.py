from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectPaths:
    """Centralise path computations for the FINAL pipeline."""

    root: Path

    @property
    def config_dir(self) -> Path:
        return self.root / "config"

    @property
    def data_dir(self) -> Path:
        return self.root / "data"

    @property
    def src_dir(self) -> Path:
        return self.root / "src"

    @property
    def output_raw_dir(self) -> Path:
        return self.data_dir / "raw"

    @property
    def output_interim_dir(self) -> Path:
        return self.data_dir / "interim"

    @property
    def output_processed_dir(self) -> Path:
        return self.data_dir / "processed"

    @classmethod
    def discover(cls) -> "ProjectPaths":
        """Discover project root based on this file location."""
        current = Path(__file__).resolve()
        root = current.parent.parent.parent
        return cls(root)

    def resolve_config(self, relative: str) -> Path:
        return (self.config_dir / relative).resolve()

    def resolve_repo_path(self, relative: str) -> Path:
        """Resolve a path relative to the repository parent (one level above FINAL)."""
        repo_root = self.root.parent
        return (repo_root / relative).resolve()

