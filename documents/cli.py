"""
Here you'll find the cli functions built with Click
"""
import os
import os.path

import click

from .documents import load_env, get_templates, get_vars 


@click.command()
@click.option('--temp_dir', default="templates",
              help="The path to the template directory. Default is ./templates")
@click.option('--extensions', help="Limit the template files.")
@click.option('--template', help="The name of the template.")
def main(temp_dir, extensions, template):
    """
    Get's a list of templates, let's the user choose the template, converts the
    variables into prompts and saves the file or prints the rendered templeta
    to std out.
    """
    env = load_env(template_dir=temp_dir)
    if not template:
        # Get all the templates and return a dict with enumerated 
        # templates names
        ext = extensions if extensions else []
        template_dict = get_templates(env, extensions=ext)
        # Echo the content of the template directory by enumerating 
        # the templates and a simple list join
        temp_list = list()
        for x in template_dict.items():
            num = str(x[0])
            # Remove whitespace, underscores and capitalize words
            temp_name = x[1].strip().replace("_", " ").title()
            temp_string = "{}. {}".format(num, temp_name)
            temp_list.append(temp_string)
        click.echo("\n".join(temp_list))
        # Prompt the user to give the number of the template
        temp_num = click.prompt(
            "Choose a templeta by entering the number of the template.",
            type=int
        )
        # Get the template from the template dictionary
        template = template_dict.get(temp_num)
    # Get the variables
    temp_vars = get_vars(template, env)
    # Crate a dict with variables and let the user input the variables
    vars_to_render = dict()
    for var in temp_vars:
        user_var = click.prompt("{}?".format(var.capitalize()))
        vars_to_render[var] = user_var
    # Get the template
    temp = env.get_template(template)
    # Render the template
    click.echo(temp.render(vars_to_render))

if __name__ == '__main__':
    main()
