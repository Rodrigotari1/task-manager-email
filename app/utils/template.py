from jinja2 import Environment, FileSystemLoader
import os

# Initialize Jinja2 environment
template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(
    loader=FileSystemLoader(template_dir),
    autoescape=True
)

def render_template(template_name: str, **kwargs) -> str:
    """
    Render a template with the given context.
    
    Args:
        template_name: Name of the template file
        **kwargs: Template context variables
        
    Returns:
        str: Rendered HTML content
    """
    template = env.get_template(template_name)
    return template.render(**kwargs) 