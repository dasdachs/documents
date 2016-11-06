__author__ = 'dasDachs'
"""
This script loads a template and returns a cli program that asks the user to
input all the variables and saves the complied template.
"""
import os
import os.path

from jinja2 import Environment, FileSystemLoader, meta, TemplatesNotFound
import click


def load_env(template_dir='templates'):
    """
    Loads the Environment object and configures the PackageLoader (the
    directory for the templates).

    :param template_dir: a string representing path to the templates directory.
    It defaults to 'templates'. If 'templates' does not exists, it falls back
    to the current directory.
    :return: a jinja2.Environment() object
    """
    if not os.path.isdir(template_dir):
        template_dir = os.getcwd()
    # Create the environment and configure the loader
    env = Environment(loader=FileSystemLoader(template_dir))
    return env

def get_templates(environment, extensions=[], hidden=False):
    """
    Gets the templates and returns a list of enumerated template names (a list
    of tuples).

    :param environment: the Environment object for Jinja2 with a loader
    :param estensions: a list allowed extensions
    :param hidden: a boolean, if set to Ture, the hidden files are included
    :return: list of tuples
    """
    if extensions:
        ext = extensions
    else:
        ext = None
    if not hidden:
        # By defult Environment.get_templates() returns a list with all files
        # So we filter out the hidden files if there are any
        filter_func = lambda x: not x.startswith('.')
    else:
        filter_func = None
    templates = environment.list_templates(
        extensions=ext,
        filter_func=filter_func
    )
    if not templates:
        raise TemplatesNotFound(
            message="No templates found in {}".format(
                environment.loader.searchpath[0]
            )
        )

    return dict(enumerate(templates, start=1))


def get_vars(template_name, environment):
    """
    Gets all the template variables from a template before compiling it.

    The program assumes that the module name is 'documents' and that templates
    are stored in ./templates.

    The code is based on this SO answer:
    http://stackoverflow.com/questions/8260490/how-to-get-list-of-all-variables-in-jinja-2-templates

    :param template_name: the whole name of the template
    :param environment: the Environment object for Jinja2
    :returns: set of variables
    """
    # Get the template source(a str) which is the 1st elm of loader.get_source()
    template_source = environment.loader.get_source(environment, template_name)[0]
    # Parse the template string since 'meta ' can only work with AST
    parsed_content = environment.parse(template_source)
    # Find the variables
    variables = meta.find_undeclared_variables(parsed_content)
    return variables

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
