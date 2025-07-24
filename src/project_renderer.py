import os
import shutil
from pathlib import Path
from typing import Dict, Any, List
from jinja2 import Environment, FileSystemLoader
from rich.console import Console

from .jinja_filters import upper_camel_case, dots, underscore, KeepUndefined
from .template_config import TemplateConfig


class ProjectRenderer:
    def __init__(self, console: Console):
        self.console = console
        self.template_config = TemplateConfig(console)

    def render_project(self, project_path: Path, output_path: Path):
        template_file = project_path / "template.yaml"
        contexts = self.template_config.load_contexts(template_file)

        if not contexts:
            return

        env = self._create_jinja_environment(project_path)

        self._clean_output_directory(output_path)

        for i, context in enumerate(contexts):
            model_name = self._get_model_name(context, i)
            self._render_project_files(project_path, output_path, output_path, env, context)
            self.console.print(f"[green]Rendered project for model '{model_name}'[/green]")

    def _create_jinja_environment(self, project_path: Path) -> Environment:
        env = Environment(
            loader=FileSystemLoader(str(project_path)),
            undefined=KeepUndefined,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        env.filters["upper_camel_case"] = upper_camel_case
        env.filters["dots"] = dots
        env.filters["underscore"] = underscore
        return env

    def _clean_output_directory(self, output_path: Path):
        if output_path.exists():
            shutil.rmtree(output_path)
        output_path.mkdir(parents=True)

    def _get_model_name(self, context: Dict[str, Any], index: int) -> str:
        return context.get("model", f"model_{index}").replace(" ", "_")

    def _prepare_model_directory(self, base_output_dir: Path):
        if base_output_dir.exists():
            shutil.rmtree(base_output_dir)
        base_output_dir.mkdir(parents=True)

    def _render_project_files(self, project_path: Path, base_output_dir: Path,
                            output_path: Path, env: Environment, context: Dict[str, Any]):
        for root, dirs, files in os.walk(project_path):
            for name in dirs + files:
                full_path = Path(root) / name

                if self._should_skip_file(full_path, project_path):
                    continue

                rendered_path = self._render_path(full_path, project_path, base_output_dir,
                                                output_path, env, context)

                if full_path.is_dir():
                    rendered_path.mkdir(parents=True, exist_ok=True)
                else:
                    self._process_file(full_path, rendered_path, env, context)

    def _should_skip_file(self, full_path: Path, project_path: Path) -> bool:
        rel_path = full_path.relative_to(project_path)
        return rel_path.name == "template.yaml"

    def _render_path(self, full_path: Path, project_path: Path, base_output_dir: Path,
                     output_path: Path, env: Environment, context: Dict[str, Any]) -> Path:
        parts = [env.from_string(part).render(context)
                 for part in full_path.relative_to(project_path).parts]
        rendered_path = base_output_dir.joinpath(*parts)

        if full_path.is_file() and "*" in rendered_path.name:
            rendered_path = rendered_path.with_name(rendered_path.name.replace("*", "."))

        return rendered_path

    def _process_file(self, full_path: Path, rendered_path: Path,
                     env: Environment, context: Dict[str, Any]):
        if full_path.suffix == ".j2":
            self._render_template_file(full_path, rendered_path, env, context)
        else:
            self._copy_regular_file(full_path, rendered_path)

    def _render_template_file(self, full_path: Path, rendered_path: Path,
                            env: Environment, context: Dict[str, Any]):
        with open(full_path, "r", encoding="utf-8") as f:
            template_content = f.read()

        rendered_content = env.from_string(template_content).render(context)
        rendered_path = rendered_path.with_suffix("")

        rendered_path.parent.mkdir(parents=True, exist_ok=True)
        with open(rendered_path, "w", encoding="utf-8") as f:
            f.write(rendered_content)

    def _copy_regular_file(self, full_path: Path, rendered_path: Path):
        rendered_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(full_path, rendered_path)