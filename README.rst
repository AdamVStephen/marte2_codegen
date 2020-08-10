=====================
MARTe2 Code Generator
=====================

MARTe2 code generation tools, mostly in python.

Initial version is not very sophisticated and relies on substituting new project metadata substitutions
into pre-released cookiecutter templates, which are themselves maintained as independent github projects.

Saves a little repetitive search/replace or in line bash preparation when starting work on a new MARTe2
set of related gams (which I describe as a package).

Inspired by and based on the structure of MARTe2-components.

Installation
------------
On any reasonable Linux distribution that has python3 and suitable command line access to github
and using standard practise as regards whether you install to the system locations with sudo (not recommended)
or with a virtualenv (best practice) or using --user to make per user local installs.

1. git clone https://github.com/AdamVStephen/marte2_codegen
2. cd marte2_codegen 
3. Install the dependencies with "pip install -r requirements_dev.txt --user"
4. Install the package with "python setup.py install --user"
5. Depending on your python/virtualenv preference, add the appropriate path/to/your/bin to your PATH

e.g. Using a system python3, the front end command line script marte2_codegen will be installed to $HOME/.local/bin

Usual caveats regarding package dependency hell apply.  Hence recommended use of virtualenv where you can tune the
dependencies without breaking already working python stuff.  Plan B : let's repeat this in Julia which allegedly
has a better package management system.

Usage
-----
marte2_codegen --package package_name --gams "GAM_A GAM_B GAM_C" [--mode [full|gamsonly]]

This will create a new directory named MARTe2-<package_name> and populate it for building GAMs, and create as many 
GAM subfolders as you provide listed named GAMs prepopulated with a template taken from the MARTe2-components/ConstantGAM.

The GAM names must be a double quoted whitespace separated list, but they can use any name ("GAM" prefix is not mandatory, nor recommended).

e.g. marte2_codegen --package plasma --gams "PlasmaCurrent MhdAmplitude DisruptionDetector"

Subject to having a working MARTe2 build setup, this package will locally build fully.

Dependencies
------------

The python dependencies are defined in the requirements_dev.txt file

The templates from which the project and the GAM files are derived are maintained independently at

1. https://github.com/AdamVStephen/marte2_cookiecutter_package
2. https://github.com/AdamVStephen/marte2_cookiecutter_gam


Features
--------

* Generate a MARTe2 package tree with boilerplate space for GAMs

Todo
----

* Add support for DataSources and Interfaces
* Expand range of GAM templates
* Integrate existing MARTe2 cfg python parser/generators from other authors
* Write some code generation using the built in MARTe2 components, possibly wrap in cli/python

Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
