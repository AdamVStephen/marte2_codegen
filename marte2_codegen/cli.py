"""
Console script for marte2_codegen.

# Generate a MARTe2 skeleton package and populate it.
#
# optional arguments:
#   --package PROJECT       Project folder name
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
from marte2_codegen.ccm2 import build_package
from marte2_codegen.ccm2 import build_gams_only

def main():
    FORMAT = '%(message)s'
    #logging.basicConfig(format=FORMAT,level=logging.INFO)
    logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Generate MARTe2 skeleton package.')
    parser.add_argument('--mode', type=str, help='Mode : [full|gamsonly]', default = "full")
    parser.add_argument('--package', type=str, help='MARTe2 package name.  Optional if building only gams.', default="package")
    # TODO Consider option to have different package name and package name.
    parser.add_argument('--gams', type=str, help='GAM list as quoted, whitespace separated list.', default="GAM_X GAM_Y")
    #parser.add_argument('--datasources', type=str, help='Issue number', default=0)
    #parser.add_argument('--interfaces', type=str, help='Use cached html? y/n', default="Y")
    #parser.add_argument('--update', type=str, help='Temporary directory for downloaded files', default='temp')

    args = parser.parse_args()

    logging.info("Cookiecutting a new MARTe skeleton package : %s" % args.package)

    # Convert from convenient whitespace separated list to a list of strings
    gams_list = args.gams.split()
    # Build the package
    #build_package(args.package, gams_list)
    print("Ready to build %s from %s" % (args.package, gams_list))

    if args.mode == "full":
        build_package(package_name = args.package, gams_list = gams_list)
    elif args.mode == "gamsonly":
        build_gams_only(package_name = args.package, gams_list = gams_list)
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
