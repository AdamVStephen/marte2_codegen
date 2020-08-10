#!/usr/bin/env python3

import logging
import os
import shutil
import pdb
from datetime import datetime

from cookiecutter.main import cookiecutter

from marte2_codegen.license import LICENSE_UKAEA, LICENSE_CCFE
from marte2_codegen.license import CPP_COPYRIGHT_UKAEA, CPP_DETAILS_IMPLEMENTATION, CPP_DETAILS_INTERFACE

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

# TODO: Expand the linkage list to include <package>/DataSources and <package>/Interfaces
#

def emit_test_libraries(gams = ['ConstantGAM']):
    text = ""
    if len(gams) >= 1:
        g = gams[0]
        text += "LIBRARIES += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (g,g)
    if len(gams) >= 2:
        for g in gams[1:]:
            text += "\nLIBRARIES_STATIC += $(BUILD_DIR)/%s/%s$(LIBEXT)" % (g,g)
    return text


class Package:

    def __init__(self,
                 template='https://github.com/AdamVStephen/marte2_cookiecutter_package',
                 package_name = "package",
                 gams_list = ["GAM_Alpha GAM_Beta"]):
        logging.info("Package ctor")
        self.template = template
        self.package_name = package_name.lower()
        self.gams_list = gams_list
        self.root_folder = 'MARTe2-%s' % self.package_name
        self.package_name_capitalized = package_name.capitalize()
        self.license = LICENSE_UKAEA
        self.timestamp = datetime.utcnow().isoformat()
        self.datasources = "False"
        self.gams = "True"
        self.interfaces = "False"
        self.subprojects = emit_subprojects(package = self.package_name_capitalized)
        self.cov_libraries_static = emit_cov_libraries_static(library_dirs = self.gams_list)
        self.gams_subprojects = emit_gams_subprojects(gams = self.gams_list)
        self.gams_libraries_static = emit_gams_libraries_static(gams = self.gams_list)
        self.gams_test_libraries_static = emit_gams_test_libraries_static(gams = gams_list)
    def cut(self):
        cookiecutter(
            self.template,
            
            no_input=True,
            extra_context = {
                'root_folder' : self.root_folder,
                'package_name' : self.package_name_capitalized,
                'timestamp' : self.timestamp,
                'license' : self.license,
                'datasources' : self.datasources,
                'gams' : self.gams,
                'interfaces' : self.interfaces,
                'subprojects' : self.subprojects,
                'cov_libraries_static' : self.cov_libraries_static,
                'gams_subprojects' : self.gams_subprojects,
                'gams_libraries_static' : self.gams_libraries_static,
                'gams_test_libraries_static' : self.gams_test_libraries_static
            }
        )
        
def m2_package_ukaea_license(template='https://github.com/AdamVStephen/marte2_cookiecutter_package',
                             package_name = "package",
                             gams_list = ["GAM_Alpha GAM_Beta"]
):
    package_name_capitalized = package_name.capitalize()
    root_folder =  'MARTe2-%s' % package_name
    cookiecutter(
        template,
        no_input=True,
        extra_context = {
            'root_folder' :root_folder,
            'package_name' : package_name_capitalized,
            'timestamp' : datetime.utcnow().isoformat(),
            'license' : LICENSE_UKAEA,
            'datasources' : "False",
            'gams' : "True",
            'interfaces' : "False",
            'subprojects' : emit_subprojects(package = package_name),
            'cov_libraries_static' : emit_cov_libraries_static(library_dirs = gams_list),
            'gams_subprojects' : emit_gams_subprojects(gams = gams_list),
            'gams_libraries_static' : emit_gams_libraries_static(gams = gams_list),
            'gams_test_libraries_static' : emit_gams_test_libraries_static(gams = gams_list)
        }
    )
    return root_folder

class GAM:
    def __init__(self,
                 template='https://github.com/AdamVStephen/marte2_cookiecutter_gam',
                 package_name = "package",
                 gam_name = "MyGAM"):
        self.template = template
        self.package_name = package_name
        self.package_name_capitalized = self.package_name.capitalize()
        self.gam_name = gam_name
        self.timestamp = datetime.utcnow().isoformat()
        self.copyright = CPP_COPYRIGHT_UKAEA
        self.implementation_details = CPP_DETAILS_IMPLEMENTATION
        self.interface_details = CPP_DETAILS_INTERFACE
        
    def cut(self):
        logging.debug("GAM.cut()")
        cookiecutter(
            self.template,
            no_input=True,
            extra_context = {
                'package_name' : self.package_name_capitalized,
                'gam_name' : self.gam_name,
                'author' : 'Adam V Stephen',
                'date' : self.timestamp,
                'timestamp' : self.timestamp,
                'copyright' : self.copyright,
                'implementation_details' : self.implementation_details,
                'interface_details' : self.interface_details
            }
    )
        
    
def m2_gam_plus_ukaea_license(template='https://github.com/AdamVStephen/marte2_cookiecutter_gam',
                              package = "package",
                              gam="MyGAM"):
    cookiecutter(
        template,
        no_input=True,
        extra_context = {
            'package_name' : package.capitalize(),
            'gam_name' : gam,
            'author' : 'Adam V Stephen',
            'date' : datetime.utcnow().isoformat(),
            'timestamp' : datetime.utcnow().isoformat(),
            'copyright' : CPP_COPYRIGHT_UKAEA,
            'implementation_details' : CPP_DETAILS_IMPLEMENTATION,
            'interface_details' : CPP_DETAILS_INTERFACE
        }
    )

def build_package_deprecated(package="package",
                  gams_list=["MyGAM"]):
    # Create the Skeleton Project First
    logging.info("Create a Skeleton package using UKAEA standard license")
    root_folder = m2_package_ukaea_license(package_name = package, gams_list = gams_list)
    # TODO : consider a class/object to hold together all the assumptions
    package_folder = "MARTe2-%s" % package
    package = package.capitalize()
    # Create Each GAM and then move into the Project Skeleton
    for gam in gams_list:
        logging.info("Create a GAM skeleton locally for %s" % gam)
        m2_gam_plus_ukaea_license(package = package, gam = gam)
        # Relocate the GAM implementation into the package
        source = "%s/Source/%s/GAMs/%s" % (gam,package,gam)
        destination = "%s/Source/%s/GAMs" % (root_folder, package)
        moved = shutil.move(source, destination)
        logging.info("mv %s %s : done" % (source, destination))
        # Relocate the GAM Test implementation into the package
        source = "%s/Test/%s/GAMs/%s" % (gam,package,gam)
        destination = "%s/Test/%s/GAMs" % (root_folder, package)
        moved = shutil.move(source, destination)
        logging.info("mv %s %s : done" % (source, destination))
        # Remove the remainder of the stub GAM sources
        tree = "%s" % gam
        shutil.rmtree(tree)
        logging.info("Deleted remaining %s tree" % gam)
    logging.info("Skeleton created")

def build_package(package_name="package",
                  gams_list=["MyGAM"]):
    # Create the Skeleton Project First
    logging.info("Create a Skeleton package using UKAEA standard license")
    logging.debug("3.141")
    package = Package(package_name = package_name, gams_list = gams_list)
    if True:
        logging.info("Work In Progress")
        package.cut()
        logging.info("Package has been cut")
        for gam_name in gams_list:
            logging.info("Create a GAM skeleton locally for %s" % gam_name)
            gam = GAM(package_name = package.package_name, gam_name = gam_name)
            logging.info("GAM object created")
            gam.cut()
            logging.info("GAM object cut()")
            # Relocate the GAM implementation into the package
            g = gam.gam_name
            p = package.package_name_capitalized
            r = package.root_folder
            source = "%s/Source/%s/GAMs/%s" % (g,p,g)
            destination = "%s/Source/%s/GAMs" % (r,p)
            moved = shutil.move(source, destination)
            logging.info("mv %s %s : done" % (source, destination))
            # Relocate the GAM Test implementation into the package
            source = "%s/Test/%s/GAMs/%s" % (g,p,g)
            destination = "%s/Test/%s/GAMs" % (r, p)
            moved = shutil.move(source, destination)
            logging.info("mv %s %s : done" % (source, destination))
            # Remove the remainder of the stub GAM sources
            tree = "%s" % g
            shutil.rmtree(tree)
            logging.info("Deleted remaining %s tree" % tree)
        return
    logging.info("Skeleton complete")

def build_gams_only(package_name = "package", gams_list=["MyGAM"]):
    for gam_name in gams_list:
        logging.info("Create a GAM skeleton locally for %s" % gam_name)
        gam = GAM(package_name = package_name, gam_name = gam_name)
        logging.info("GAM object created")
        gam.cut()
        logging.info("GAM object cut()")
    logging.info("build_gams_only : finished")
