from pathlib import Path
import questionary
from rich.console import Console

from src.project_renderer import ProjectRenderer
from src.directory_utils import DirectoryManager

console = Console()

BASE_DIR = Path(__file__).parent.resolve()
PROJECTS_DIR = BASE_DIR / "projects"
OUTPUT_DIR = BASE_DIR / "output"


def main():
    console.print("🚀 [bold]Project Generator[/bold]")

    directory_manager = DirectoryManager(console)
    directory_manager.ensure_directories_exist(PROJECTS_DIR, OUTPUT_DIR)

    projects = directory_manager.get_available_projects(PROJECTS_DIR)
    if not projects:
        console.print("[red]No projects found in 'projects/'[/red]")
        return

    selected = questionary.select("Select a project", choices=projects).ask()
    if not selected:
        console.print("[red]No project selected[/red]")
        return

    project_path = PROJECTS_DIR / selected
    
    renderer = ProjectRenderer(console)
    renderer.render_project(project_path, OUTPUT_DIR)


if __name__ == "__main__":
    main()
