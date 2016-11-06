from setuptools import setup, find_packages

setup(
    # Descriptions
    name='Documents',
    version='0.1',
    author='dasDachs',
    author_email='jani.sumak@gmail.com',
    description="Render document templates with jinja2 syntax.",
    # long_description=""""""
    # url=''
    keywords='cli templates documents',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers, Users',
        'Topic :: Template engine :: Documents',

        # Pick your license as you wish (should match "license" above)
         'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # Package details
    packages=find_packages(exclude=['tests*']),
    
    # Requirements
    install_requires=[
        'Click',
        'Jinja2'
    ],
    entry_points='''
        [console_scripts]
        documents=documents.main:main
    ''',
)
