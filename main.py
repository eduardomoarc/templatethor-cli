import os
import shutil
import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, Undefined
import questionary
from rich.console import Console

console = Console()

BASE_DIR = Path(__file__).parent.resolve()
PROJECTS_DIR = BASE_DIR / "projects"
OUTPUT_DIR = BASE_DIR / "output"


# --- Filtros para Jinja ---
def upper_camel_case(value) -> str:
    text = str(value)
    return "".join(word.capitalize() for word in re.split(r"[\s_-]+", text))


def dots(value) -> str:
    text = str(value)
    return text.replace(" ", ".").replace("_", ".")


# --- Undefined personalizado para dejar variables sin contexto sin cambiar ---
class KeepUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return f"{{{{ {self._undefined_name} }}}}"


def render_project_template(project_path: Path, output_path: Path):
    """
    Renderiza proyecto usando el/los contextos del template.yaml.
    Si es lista, genera múltiples carpetas (una por cada dict).
    Si es dict, genera una sola carpeta.
    """

    template_file = project_path / "template.yaml"
    if not template_file.exists():
        console.print("[yellow]template.yaml not found, no rendering performed[/yellow]")
        return

    with open(template_file, "r", encoding="utf-8") as f:
        contexts = yaml.safe_load(f)

    if not contexts:
        console.print("[yellow]template.yaml empty, no rendering performed[/yellow]")
        return

    if isinstance(contexts, dict):
        contexts = [contexts]
    elif not isinstance(contexts, list):
        console.print("[yellow]template.yaml format not recognized, expected dict or list[/yellow]")
        return

    env = Environment(
        loader=FileSystemLoader(str(project_path)),
        undefined=KeepUndefined,
    )
    env.filters["upper_camel_case"] = upper_camel_case
    env.filters["dots"] = dots

    def render_path(path: Path, context: dict) -> Path:
        parts = [env.from_string(part).render(context) for part in path.relative_to(project_path).parts]
        return output_path.joinpath(*parts)

    # Limpiar output antes de generar
    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    for i, context in enumerate(contexts):
        model_name = context.get("model", f"model_{i}").replace(" ", "_")

        base_output_dir = output_path / model_name
        if base_output_dir.exists():
            shutil.rmtree(base_output_dir)
        base_output_dir.mkdir(parents=True)

        for root, dirs, files in os.walk(project_path):
            for name in dirs + files:
                full_path = Path(root) / name
                rel_path = full_path.relative_to(project_path)

                if rel_path.name == "template.yaml":
                    continue

                rendered_path = render_path(full_path, context)
                # Cambiar base al directorio del modelo actual
                rendered_path = base_output_dir / rendered_path.relative_to(output_path)

                # Reemplazar '*' por '.' solo para archivos
                if full_path.is_file() and "*" in rendered_path.name:
                    rendered_path = rendered_path.with_name(rendered_path.name.replace("*", "."))

                if full_path.is_dir():
                    rendered_path.mkdir(parents=True, exist_ok=True)
                else:
                    if full_path.suffix == ".j2":
                        # Archivo plantilla: renderizar contenido y quitar extensión .j2
                        with open(full_path, "r", encoding="utf-8") as f:
                            template_content = f.read()
                        rendered_content = env.from_string(template_content).render(context)

                        # Quitar extensión .j2 para archivo final
                        rendered_path = rendered_path.with_suffix("")

                        rendered_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(rendered_path, "w", encoding="utf-8") as f:
                            f.write(rendered_content)
                    else:
                        # Archivo normal, copiar tal cual sin render
                        rendered_path.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(full_path, rendered_path)

        console.print(f"[green]Rendered project for model '{model_name}' into folder '{base_output_dir}'[/green]")


def ensure_directories_exist():
    if not PROJECTS_DIR.exists():
        PROJECTS_DIR.mkdir(parents=True)
        console.print(f"[yellow]Created 'projects' folder at {PROJECTS_DIR}[/yellow]")
    if not OUTPUT_DIR.exists():
        OUTPUT_DIR.mkdir(parents=True)
        console.print(f"[yellow]Created 'output' folder at {OUTPUT_DIR}[/yellow]")


def main():
    console.print("🚀 [bold]Project Generator[/bold]")

    ensure_directories_exist()

    projects = [p.name for p in PROJECTS_DIR.iterdir() if p.is_dir()]
    if not projects:
        console.print("[red]No projects found in 'projects/'[/red]")
        return

    selected = questionary.select("Select a project", choices=projects).ask()
    if not selected:
        console.print("[red]No project selected[/red]")
        return

    project_path = PROJECTS_DIR / selected

    render_project_template(project_path, OUTPUT_DIR)


if __name__ == "__main__":
    main()
