"""
Console script for marte2_codegen.

# Generate a MARTe2 skeleton project and populate it.
#
# optional arguments:
#   --project PROJECT       Project folder name
#   --gam GAM1 GAM2         Whitespace separated list of GAM names.
#
# TO BE IMPLEMENTED
#
#   --datasource DS1 DS2    Whitespace separated list of DataSource names.
#   --interface IF1 IF2     Whitespace separated list of Interface names
#
# Some means to distinguish update vs create

"""

import logging
import os
import argparse
import sys

from marte2_codegen.marte2_codegen import codegen
from marte2_codegen.license import LICENSE_UKAEA, LICENSE_CCFE
from marte2_codegen.ccm2 import emit_subprojects
from marte2_codegen.ccm2 import emit_cov_libraries_static
from marte2_codegen.ccm2 import emit_gams_subprojects
from marte2_codegen.ccm2 import emit_gams_libraries_static
from marte2_codegen.ccm2 import emit_gams_test_libraries_static
from marte2_codegen.ccm2 import emit_test_libraries
from marte2_codegen.ccm2 import m2_project_ukaea_license
from marte2_codegen.ccm2 import m2_gam_plus_ukaea_license
from marte2_codegen.ccm2 import build_project

def main():
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT,level=logging.INFO)
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Generate MARTe2 skeleton project.')
    parser.add_argument('--project', type=str, help='MARTe2 project name', default="project")
    # TODO Consider option to have different project name and package name.
    parser.add_argument('--gams', type=str, help='GAM list', default="GAM_X GAM_Y")
    #parser.add_argument('--datasources', type=str, help='Issue number', default=0)
    #parser.add_argument('--interfaces', type=str, help='Use cached html? y/n', default="Y")
    #parser.add_argument('--update', type=str, help='Temporary directory for downloaded files', default='temp')

    args = parser.parse_args()

    logging.info("Cookiecutting a new MARTe skeleton project : %s" % args.project)

    # Convert from convenient whitespace separated list to a list of strings
    gams_list = args.gams.split()
    # Build the project
    #build_project(args.project, gams_list)
    print("Ready to build %s from %s" % (args.project, gams_list))
    build_project(args.project, gams_list)

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
