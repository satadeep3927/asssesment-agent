from jinja2 import Environment, FileSystemLoader


class PromptManager:
    def __init__(self, prompts_dir: str = "prompts"):
        """
        Initialize the prompt manager with Jinja2 templates.

        :param prompts_dir: Directory containing prompt templates
        """
        self.prompts_dir = prompts_dir
        self.env = Environment(loader=FileSystemLoader(prompts_dir))

    def render_prompt(self, prompt_name: str, var: dict = dict) -> str:
        """
        Render a prompt with variables.

        :param prompt_name: Name of the prompt to render
        :param kwargs: Additional template variables
        :return: Rendered prompt text
        """
        template = self.env.get_template(f"{prompt_name}.j2")

        return template.render(var)
