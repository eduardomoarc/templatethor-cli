from pathlib import Path
from typing import List, Dict, Any, Union
import yaml
from rich.console import Console


class TemplateConfig:
    def __init__(self, console: Console):
        self.console = console
    
    def load_contexts(self, template_file: Path) -> List[Dict[str, Any]]:
        if not template_file.exists():
            self.console.print("[yellow]template.yaml not found, no rendering performed[/yellow]")
            return []
        
        with open(template_file, "r", encoding="utf-8") as f:
            contexts = yaml.safe_load(f)
        
        if not contexts:
            self.console.print("[yellow]template.yaml empty, no rendering performed[/yellow]")
            return []
        
        return self._normalize_contexts(contexts)
    
    def _normalize_contexts(self, contexts: Union[Dict[str, Any], List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
        if isinstance(contexts, dict):
            return [contexts]
        elif isinstance(contexts, list):
            return contexts
        else:
            self.console.print("[yellow]template.yaml format not recognized, expected dict or list[/yellow]")
            return []