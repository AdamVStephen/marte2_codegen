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
import getpass
import logging
import os
import argparse
import sys

from marte2_codegen.marte2_codegen import codegen

from marte2_codegen.license import LICENSE_UKAEA, LICENSE_CCFE
from marte2_codegen.license import CPP_LICENSE_COPYRIGHT_UKAEA_EUPL_2022

from marte2_codegen.ccm2 import emit_subprojects
from marte2_codegen.ccm2 import emit_cov_libraries_static

from marte2_codegen.ccm2 import emit_gams_subprojects
from marte2_codegen.ccm2 import emit_gams_libraries_static
from marte2_codegen.ccm2 import emit_gams_test_libraries_static

from marte2_codegen.ccm2 import emit_datasources_subprojects
from marte2_codegen.ccm2 import emit_datasources_libraries_static
from marte2_codegen.ccm2 import emit_datasources_test_libraries_static

from marte2_codegen.ccm2 import emit_test_libraries
from marte2_codegen.ccm2 import build_package
from marte2_codegen.ccm2 import build_gams_only
from marte2_codegen.ccm2 import build_datasources_only

def main():
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT,level=logging.INFO)
    #logging.basicConfig(format=FORMAT, level=logging.DEBUG)

    parser = argparse.ArgumentParser(description='Generate MARTe2 skeleton package.')
    parser.add_argument('--mode', type=str, help='Mode : [full|gamsonly|dsonly]', default = "full")
    parser.add_argument('--package', type=str, help='MARTe2 package name.  Required.', required=True)
    parser.add_argument('--gams', type=str, help='GAM list as quoted, whitespace separated list.', default="GAM_X GAM_Y")
    parser.add_argument('--author', type=str, help='Author', default=getpass.getuser())
    parser.add_argument('--datasources', type=str, help='Datasource list, whitespace separated list.', default="DS_1 DS_2")
    #parser.add_argument('--interfaces', type=str, help='Use cached html? y/n', default="Y")
    #parser.add_argument('--update', type=str, help='Temporary directory for downloaded files', default='temp')

    args = parser.parse_args()

    logging.info("Cookiecutting a new MARTe package : MARTe2-{0}".format(args.package))

    gams_list = args.gams.split()
    datasources_list = args.datasources.split()

    if args.mode == "full":
        build_package(package_name = args.package, gams_list = gams_list, author=args.author)
        logging.info("To build : cd MARTe2-{0} && make -f Makefile.linux".format(args.package))
    elif args.mode == "gamsonly":
        build_gams_only(package_name = args.package, gams_list = gams_list, author=args.author)
    elif args.mode == "datasourcesonly":
        build_datasources_only(package_name = args.package, datasources_list = datasources_list, author=args.author)
        logging.info("To build : cd MARTe2-{0} && make -f Makefile.linux".format(args.package))
    elif args.mode == "gamsonly":
        build_gams_only(package_name = args.package, gams_list = gams_list)
        logging.info("To build : cd MARTe2-{0} && make -f Makefile.linux".format(args.package))
    elif args.mode == "dsonly":
        build_gams_only(package_name = args.package, datasources_list = datasources_list)
        logging.info("To build : cd MARTe2-{0} && make -f Makefile.linux".format(args.package))
    else:
        parser.print_help()

if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
