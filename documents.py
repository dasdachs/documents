__author__ = 'dasDachs'
"""
This script loads a template and returns a cli program that asks the user to
input all the variables and saves the complied template.
"""
from jinja2 import Environment, meta, PackageLoader
# import click


def get_vars(template_name):
    """
    Gets all the template variables from a template before compiling it.

    The program assumes that the module name is 'documents' and that templates
    are stored in ./templates.

    The code is based on this SO answer:
    http://stackoverflow.com/questions/8260490/how-to-get-list-of-all-variables-in-jinja-2-templates

    :param template_name: the whole name of the template
    :returns: set of variables
    """
    # Create the environment and configure the loader
    env = Environment(loader=PackageLoader('documents', 'templates'))
    # Get the template source(a str) which is the 1st elm of loader.get_source()
    template_source = env.loader.get_source(env, template_name)[0]
    # Parse the template string since 'meta ' can only work with AST
    parsed_content = env.parse(template_source)
    # Find the variables
    variables = meta.find_undeclared_variables(parsed_content)
    return varibales
