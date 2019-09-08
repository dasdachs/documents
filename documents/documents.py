import os
import os.path

from jinja2 import Environment, FileSystemLoader, meta, TemplatesNotFound


# Define a list of public 'names' to import to __init__.py
# so we can use this module programtically like this:
#
# >>> from documents import load_env, get_templats
# >>> get_templates(load_env())
# >>> ['template1.md', 'template2.rst', 'template3.html']
__all__ = ['load_env', 'get_templates', 'get_vars']


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
