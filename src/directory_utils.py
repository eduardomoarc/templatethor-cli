from pathlib import Path
from rich.console import Console


class DirectoryManager:
    def __init__(self, console: Console):
        self.console = console
    
    def ensure_directories_exist(self, projects_dir: Path, output_dir: Path):
        self._ensure_directory_exists(projects_dir, "projects")
        self._ensure_directory_exists(output_dir, "output")
    
    def _ensure_directory_exists(self, directory: Path, name: str):
        if not directory.exists():
            directory.mkdir(parents=True)
            self.console.print(f"[yellow]Created '{name}' folder at {directory}[/yellow]")
    
    def get_available_projects(self, projects_dir: Path) -> list[str]:
        return [p.name for p in projects_dir.iterdir() if p.is_dir()]