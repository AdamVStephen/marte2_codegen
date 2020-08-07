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
        'Test/%s/GAMs'], package = "project"):
    subproject_dirs = [x % package for x in dir_patterns]
    text = ""
    if len(subproject_dirs) >=1 :
        d = subproject_dirs[0]
        text += "\nSPB = %s.x" % d
    if len(subproject_dirs) >=2 :
        for d in subproject_dirs[1:]:
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

def m2_project_ukaea_license(template='https://github.com/AdamVStephen/marte2_cookiecutter_package',
                             project_name = "project",
                             gams_list = ["GAM_Alpha GAM_Beta"]
):
    package_name = project_name.capitalize()
    cookiecutter(
        template,
        no_input=True,
        extra_context = {
            'project_name' : project_name,
            'project_folder' : 'MARTe2-%s' % project_name,
            'package_name' : package_name,
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

def m2_gam_plus_ukaea_license(template='https://github.com/AdamVStephen/marte2_cookiecutter_gam',
                              project = "project",
                              gam="MyGAM"):
    cookiecutter(
        template,
        no_input=True,
        extra_context = {
            'project_name' : project,
            'package_name' : project.capitalize(),
            'gam_name' : gam,
            'author' : 'Adam V Stephen',
            'date' : datetime.utcnow().isoformat(),
            'timestamp' : datetime.utcnow().isoformat(),
            'copyright' : CPP_COPYRIGHT_UKAEA,
            'implementation_details' : CPP_DETAILS_IMPLEMENTATION,
            'interface_details' : CPP_DETAILS_INTERFACE
        }
    )

def build_project(project="project",
                  gams_list=["MyGAM"]):
    # Create the Skeleton Project First
    logging.info("Create a Skeleton project using UKAEA standard license")
    m2_project_ukaea_license(project_name = project, gams_list = gams_list)
    # TODO : consider a class/object to hold together all the assumptions
    project_folder = "MARTe2-%s" % project
    package = project.capitalize()
    # Create Each GAM and then move into the Project Skeleton
    for gam in gams_list:
        logging.info("Create a GAM skeleton locally for %s" % gam)
        m2_gam_plus_ukaea_license(project = project, gam = gam)
        # Relocate the GAM implementation into the project
        source = "%s/Source/%s/GAMs/%s" % (gam,package,gam)
        destination = "%s/Source/%s/GAMs" % (project_folder, package)
        moved = shutil.move(source, destination)
        logging.info("mv %s %s : done" % (source, destination))
        # Relocate the GAM Test implementation into the project
        source = "%s/Test/%s/GAMs/%s" % (gam,package,gam)
        destination = "%s/Test/%s/GAMs" % (project_folder, package)
        moved = shutil.move(source, destination)
        logging.info("mv %s %s : done" % (source, destination))
        # Remove the remainder of the stub GAM sources
        tree = "%s" % gam
        shutil.rmtree(tree)
        logging.info("Deleted remaining %s tree" % gam)
    logging.info("Skeleton created")
