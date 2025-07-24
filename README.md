# Templathor Python

A powerful and flexible template-based code generator designed to streamline the creation of repetitive code structures, with built-in support for Odoo module generation.

## 🚀 Features

- **Template-driven generation**: Create reusable project templates with Jinja2 templating engine
- **Interactive CLI**: User-friendly command-line interface with project selection
- **Multi-model support**: Generate multiple models/modules from a single template configuration
- **Flexible field definitions**: Support for various field types (char, float, boolean, many2one, etc.)
- **Built-in filters**: Custom Jinja2 filters for common transformations (underscore, upper_camel_case, dots)
- **Clean architecture**: Modular design with separation of concerns
- **Rich output**: Beautiful console output with colors and formatting

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🛠️ Installation

1. Clone the repository:
```bash
git clone git@github.com:eduardomoarc/templatethor-cli.git
cd templathor-python
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Basic Usage

Run the interactive generator:
```bash
python main.py
```

The application will:
1. Display available project templates
2. Let you select a template to generate
3. Process the template configuration
4. Generate the output files in the `output/` directory

### Project Structure

```
templathor-python/
├── main.py                 # Entry point
├── src/                    # Source code
│   ├── project_renderer.py # Core template rendering logic
│   ├── template_config.py  # YAML configuration handler
│   ├── jinja_filters.py    # Custom Jinja2 filters
│   └── directory_utils.py  # Directory management utilities
├── projects/               # Template definitions
│   └── odoo/              # Odoo module templates
│       ├── template.yaml  # Configuration file
│       └── {{ model|underscore }}/  # Template structure
└── output/                # Generated files
```

### Template Configuration

Templates are defined using YAML configuration files. Example `template.yaml`:

```yaml
- model: account type
  model_description: "Account Type"
  fields:
    - name: name
      description: "Name"
      type: char
    - name: balance
      description: "Balance"
      type: float
    - name: partner_id
      description: "Partner"
      type: many2one
      relation: 'res.partner'

- model: account config
  model_description: "Account Configuration"
  fields:
    - name: name
      description: "Name"
      type: char
    - name: active
      description: "Active"
      type: boolean
```

### Template Files

Template files use Jinja2 syntax with `.j2` extension. Available filters:

- `{{ model|underscore }}` - Converts "account type" to "account_type"
- `{{ model|upper_camel_case }}` - Converts "account type" to "AccountType"
- `{{ model|dots }}` - Converts "account type" to "account.type"

Example template file:
```python
class {{ model|upper_camel_case }}(models.Model):
    _name = '{{ model|dots }}'
    _description = '{{ model_description }}'

    {% for field in fields %}
    {{ field.name }} = fields.{{ field.type|upper_camel_case }}(
        string="{{ field.description }}"
        {% if field.type == 'many2one' %}, comodel_name='{{ field.relation}}'{% endif %}
    )
    {% endfor %}
```

## 🏗️ Architecture

The project follows clean architecture principles:

- **ProjectRenderer**: Core rendering engine that processes templates
- **TemplateConfig**: Handles YAML configuration loading and validation
- **DirectoryManager**: Manages directory operations and project discovery
- **JinjaFilters**: Custom filters for string transformations

## 🔧 Creating Custom Templates

1. Create a new directory under `projects/`
2. Add a `template.yaml` configuration file
3. Create your template structure using Jinja2 syntax
4. Use `.j2` extension for files that need template processing

## 📦 Dependencies

- **rich**: Beautiful terminal formatting and colors
- **questionary**: Interactive command-line prompts
- **jinja2**: Template engine for code generation
- **pyyaml**: YAML configuration file parsing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Examples

### Generated Odoo Module Structure

For a model named "account config", the generator creates:

```
output/
└── account_config/
    ├── __init__.py
    ├── models/
    │   ├── __init__.py
    │   └── account_config.py
    ├── security/
    │   ├── groups.xml
    │   ├── multicompany_rules.xml
    │   └── account_config/
    │       └── ir.model.access.csv
    └── views/
        ├── account_config_menu_item.xml
        └── account_config_view.xml
```

---

*Built with ❤️ for developers who value their time*