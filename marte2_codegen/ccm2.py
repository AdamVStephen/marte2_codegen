#!/usr/bin/env python3

import logging
import os
import shutil
import pdb
from datetime import datetime

from cookiecutter.main import cookiecutter

from marte2_codegen.license import LICENSE_UKAEA
from marte2_codegen.license import LICENSE_CCFE
from marte2_codegen.license import LICENSE_UKAEA_EUPL_11_2022
from marte2_codegen.license import CPP_LICENSE_COPYRIGHT_UKAEA_EUPL_2022
from marte2_codegen.license import CPP_COPYRIGHT_UKAEA
from marte2_codegen.license import CPP_GAM_DETAILS_IMPLEMENTATION
from marte2_codegen.license import CPP_DATASOURCE_DETAILS_IMPLEMENTATION
from marte2_codegen.license import CPP_DETAILS_INTERFACE

def emit_subprojects(dir_patterns = [
        'Source/%s/GAMs',
        'Test/%s/GAMs'], package = "package"):
    subpackage_dirs = [x % package for x in dir_patterns]
    text = ""
    if len(subpackage_dirs) >=1 :
        d = subpackage_dirs[0]
        text += "\nSPB = %s.x" % d
    if len(subpackage_dirs) >=2 :
        for d in subpackage_dirs[1:]:
            text += "\nSPB += %s.x" % d
    # Test must build last
    text += "\nSPB += Test/GTest.x"
    return text

# TODO: Provide a hook to #ifdef condition the append of a library.
#

def emit_cov_libraries_static(library_dirs = ['ConstantGAM']):
    """
    Code generation for the {{cookiecutter.libraries_static}} placeholder found in
    Source/<package>/GAMs/Makefile.cov
    """
    text = ""
    if len(library_dirs) >= 1:
        d = library_dirs[0]
        text += "LIBRARIES_STATIC = %s/cov/%s$(LIBEXT)" % (d,d)
    if len(library_dirs) >= 2:
        for d in library_dirs[1:]:
            text += "\nLIBRARIES_STATIC += %s/cov/%s$(LIBEXT)" % (d,d)
    return text

# TODO: Provide a hook to #ifdef condition the append of a GAM
#

def emit_gams_subprojects(gams = ['ConstantGAM']):
    text = ""
    if len(gams) >= 1:
        g = gams[0]
        text += "SPB = %s.x" % g
    if len(gams) >= 2:
        for g in gams[1:]:
            text += "\nSPB += %s.x" % g
    return text

# TODO: Provide a hook to #ifdef condition the append of a GAM
#

def emit_gams_libraries_static(gams = ['ConstantGAM']):
    text = ""
    if len(gams) >= 1:
        g = gams[0]
        text += "LIBRARIES_STATIC = $(BUILD_DIR)/%s/%s$(LIBEXT)" % (g,g)
    if len(gams) >= 2:
        for g in gams[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (g,g)
    return text

def emit_gams_test_libraries_static(gams = ['ConstantGAM']):
    text = ""
    if len(gams) >= 1:
        g = gams[0]
        text += "LIBRARIES_STATIC += $(BUILD_DIR)/%s/%sTest$(LIBEXT)" % (g,g)
    if len(gams) >= 2:
        for g in gams[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%sTest$(LIBEXT)" % (g,g)
    return text

# TODO: Provide a hook to #ifdef condition the append of a Data Source
#

def emit_datasources_subprojects(datasources = ['ArbDataSource']):
    text = ""
    if len(datasources) >= 1:
        d = datasources[0]
        text += "SPB = %s.x" % d
    if len(datasources) >= 2:
        for d in datasources[1:]:
            text += "\nSPB += %s.x" % d
    return text

# TODO: Provide a hook to #ifdef condition the append of a GAM
#

def emit_datasources_libraries_static(datasources = ['ArbDataSource']):
    text = ""
    if len(datasources) >= 1:
        d = datasources[0]
        text += "LIBRARIES_STATIC = $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    if len(datasources) >= 2:
        for d in datasources[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    return text

def emit_datasources_test_libraries_static(datasources = ['ArbDataSource']):
    text = ""
    if len(datasources) >= 1:
        d = datasources[0]
        text += "LIBRARIES_STATIC += $(BUILD_DIR)/%s/%sTest$(LIBEXT)" % (d,d)
    if len(datasources) >= 2:
        for d in datasources[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%sTest$(LIBEXT)" % (d,d)
    return text

# TODO: Expand the linkage list to include <package>/DataSources and <package>/Interfaces
#

def emit_test_libraries(datasources = ['ArbDataSource']):
    text = ""
    if len(datasources) >= 1:
        d = datasources[0]
        text += "LIBRARIES += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    if len(datasources) >= 2:
        for d in datasources[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    return text


# TODO: Expand the linkage list to include <package>/DataSources and <package>/Interfaces
#

def TODO_emit_test_libraries(datasources = ['ArbDataSource']):
    text = ""
    if len(datasources) >= 1:
        d = datasources[0]
        text += "LIBRARIES += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    if len(datasources) >= 2:
        for d in datasources[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (d,d)
    return text

class Package:

    def __init__(self,
                 template='https://github.com/AdamVStephen/marte2_cookiecutter_package',
                 package_name = "package",
                 gams_list = ["GAM_Alpha GAM_Beta"],
		 datasources_list = ["DataSource_A DataSource_B"],
		 author="Author"):
        logging.debug("Package ctor")
        self.template = template
        self.package_name = package_name.lower()
        self.gams_list = gams_list
        self.datasources_list = datasources_list
        self.author = author
        self.root_folder = 'MARTe2-%s' % self.package_name
        self.package_name_capitalized = package_name.capitalize()
        self.license = LICENSE_UKAEA
        self.timestamp = datetime.utcnow().isoformat()
        self.datasources = "True"
        self.gams = "True"
        self.interfaces = "False"
        self.subprojects = emit_subprojects(package = self.package_name_capitalized)
        self.cov_libraries_static = emit_cov_libraries_static(library_dirs = self.gams_list)
        self.gams_subprojects = emit_gams_subprojects(gams = self.gams_list)
        self.gams_libraries_static = emit_gams_libraries_static(gams = self.gams_list)
        self.gams_test_libraries_static = emit_gams_test_libraries_static(gams = gams_list)
        self.datasources_subprojects = emit_datasources_subprojects(datasources = self.datasources_list)
        self.datasources_libraries_static = emit_datasources_libraries_static(datasources = self.datasources_list)
        self.datasources_test_libraries_static = emit_datasources_test_libraries_static(datasources = datasources_list)

    def cut(self):
        cookiecutter(
            self.template,
            
            no_input=True,
            extra_context = {
                'root_folder' : self.root_folder,
                'package_name' : self.package_name_capitalized,
                'timestamp' : self.timestamp,
                'author' : self.author,
                'license' : self.license,
                'datasources' : self.datasources,
                'gams' : self.gams,
                'interfaces' : self.interfaces,
                'subprojects' : self.subprojects,
                'cov_libraries_static' : self.cov_libraries_static,
                'gams_subprojects' : self.gams_subprojects,
                'gams_libraries_static' : self.gams_libraries_static,
                'gams_test_libraries_static' : self.gams_test_libraries_static,
                'datasources_subprojects' : self.datasources_subprojects,
                'datasources_libraries_static' : self.datasources_libraries_static,
                'datasources_test_libraries_static' : self.datasources_test_libraries_static
            }
        )
        
class GAM:
    def __init__(self,
                 template='https://github.com/AdamVStephen/marte2_cookiecutter_gam',
                 package_name = "package",
                 gam_name = "MyGAM",
		 author="Author"):
        self.template = template
        self.package_name = package_name.lower()
        self.package_name_capitalized = self.package_name.capitalize()
        self.gam_name = gam_name
        self.author = author
        self.timestamp = datetime.utcnow().isoformat()
        self.copyright = CPP_COPYRIGHT_UKAEA
        self.implementation_details = CPP_GAM_DETAILS_IMPLEMENTATION
        self.interface_details = CPP_DETAILS_INTERFACE
        self.gam_include_guard = "{0}_H_".format(package_name.upper())
        
    def cut(self):
        logging.debug("GAM.cut()")
        cookiecutter(
            self.template,
            no_input=True,
            extra_context = {
                'package_name' : self.package_name_capitalized,
                'gam_name' : self.gam_name,
                'author' : self.author,
                'date' : self.timestamp,
                'timestamp' : self.timestamp,
                'copyright' : self.copyright,
                'implementation_details' : self.implementation_details,
                'interface_details' : self.interface_details,
                'gam_include_guard' : self.gam_include_guard
            }
    )

class DataSource:
    def __init__(self,
                 template='https://github.com/AdamVStephen/marte2_cookiecutter_datasource',
                 package_name = "package",
                 datasource_name = "MyDataSource",
		 author="Author"):
        self.template = template
        self.package_name = package_name.lower()
        self.package_name_capitalized = self.package_name.capitalize()
        self.datasource_name = datasource_name
        self.timestamp = datetime.utcnow().isoformat()
        self.author = author
        self.copyright = CPP_LICENSE_COPYRIGHT_UKAEA_EUPL_2022
        self.implementation_details = CPP_DATASOURCE_DETAILS_IMPLEMENTATION
        self.interface_details = CPP_DETAILS_INTERFACE
        self.datasource_include_guard = "{0}_H_".format(package_name.upper())
        
    def cut(self):
        logging.debug("DataSource.cut()")
        cookiecutter(
            self.template,
            no_input=True,
            extra_context = {
                'package_name' : self.package_name_capitalized,
                'datasource_name' : self.datasource_name,
                'author' : self.author,
                'date' : self.timestamp,
                'timestamp' : self.timestamp,
                'copyright' : self.copyright,
                'license' : self.copyright,
                'implementation_details' : self.implementation_details,
                'interface_details' : self.interface_details,
                'datasource_include_guard' : self.datasource_include_guard
            }
    )


def build_package(package_name="package",
                  gams_list=["MyGAM"],
		  datasources_list=["MyDataSource"],
		  author="Author"):
    # Create the Skeleton Project First
    logging.debug("Create a Skeleton package using UKAEA standard license")
    logging.debug("3.141")
    package = Package(package_name = package_name, 
			gams_list = gams_list,
			datasources_list = datasources_list,
			author = author)
    if True:
        package.cut()
        for gam_name in gams_list:
            logging.debug("Create a GAM skeleton locally for %s" % gam_name)
            gam = GAM(package_name = package.package_name, gam_name = gam_name, author = author)
            logging.debug("GAM {0} object created".format(gam_name))
            gam.cut()
            logging.debug("GAM {0} cut()".format(gam_name))
            # Relocate the GAM implementation into the package
            g = gam.gam_name
            p = package.package_name_capitalized
            r = package.root_folder
            source = "%s/Source/%s/GAMs/%s" % (g,p,g)
            destination = "%s/Source/%s/GAMs" % (r,p)
            moved = shutil.move(source, destination)
            logging.debug("mv %s %s : done" % (source, destination))
            # Relocate the GAM Test implementation into the package
            source = "%s/Test/%s/GAMs/%s" % (g,p,g)
            destination = "%s/Test/%s/GAMs" % (r, p)
            moved = shutil.move(source, destination)
            logging.debug("mv %s %s : done" % (source, destination))
            # Remove the remainder of the stub GAM sources
            tree = "%s" % g
            shutil.rmtree(tree)
            logging.debug("Deleted remaining %s tree" % tree)
        for datasource_name in datasources_list:
            logging.debug("Create a DataSource skeleton locally for %s" % datasource_name)
            datasource = DataSource(package_name = package.package_name, datasource_name = datasource_name, author = author)
            logging.debug("DataSource {0} object created".format(datasource_name))
            datasource.cut()
            logging.debug("DataSource {0} cut()".format(datasource_name))
            # Relocate the DataSource implementation into the package
            d = datasource.datasource_name
            p = package.package_name_capitalized
            r = package.root_folder
            source = "%s/Source/%s/DataSources/%s" % (d,p,d)
            destination = "%s/Source/%s/DataSources" % (r,p)
            moved = shutil.move(source, destination)
            logging.debug("mv %s %s : done" % (source, destination))
            # Relocate the GAM Test implementation into the package
            source = "%s/Test/%s/DataSources/%s" % (d,p,d)
            destination = "%s/Test/%s/DataSources" % (r, p)
            moved = shutil.move(source, destination)
            logging.debug("mv %s %s : done" % (source, destination))
            # Remove the remainder of the stub GAM sources
            tree = "%s" % d
            shutil.rmtree(tree)
            logging.debug("Deleted remaining %s tree" % tree)
        return
    logging.debug("Skeleton complete")

def build_gams_only(package_name = "package", gams_list=["MyGAM"], author="Author"):
    for gam_name in gams_list:
        logging.debug("Create a GAM skeleton locally for %s" % gam_name)
        gam = GAM(package_name = package_name, gam_name = gam_name, author=author)
        gam.cut()
    logging.debug("build_gams_only : finished")

def build_datasources_only(package_name = "package", datasources_list=["MyDataSource"], author="Author"):
    for datasource_name in datasources_list:
        logging.debug("Create a DataSource skeleton locally for %s" % datasource_name)
        datasource = DataSource(package_name = package_name, datasource_name = datasource_name, author=author)
        datasource.cut()
    logging.debug("build_datasources_only : finished")

