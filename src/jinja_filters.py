import re
from jinja2 import Undefined


def upper_camel_case(value) -> str:
    text = str(value)
    return "".join(word.capitalize() for word in re.split(r"[\s_-]+", text))


def dots(value) -> str:
    text = str(value)
    return text.replace(" ", ".").replace("_", ".")


def underscore(value) -> str:
    text = str(value)
    text = re.sub(r'[\s-]+', '_', text)
    return text.lower()


class KeepUndefined(Undefined):
    def _fail_with_undefined_error(self, *args, **kwargs):
        return f"{{{{ {self._undefined_name} }}}}"
