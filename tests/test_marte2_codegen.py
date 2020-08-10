#!/usr/bin/env python

"""Tests for `marte2_codegen` package."""

import pytest


from marte2_codegen import marte2_codegen
from marte2_codegen.ccm2 import Package

@pytest.fixture
def default_package():
    """Default Package object as fixture for tests."""
    return Package()

class TestDefaultPackage:
    
    def test_root_folder(self, default_package):
        """Check naming assumptions are consistent with design."""
        assert(default_package.root_folder == "MARTe2-package")
        
    def test_package_name_capitalized(self, default_package):
        assert(default_package.package_name_capitalized == "Package")

custom_package_name = "automotive"

@pytest.fixture
def custom_package():
    """Default Package object as fixture for tests."""
    return Package(package_name = custom_package_name)

class TestCustomPackage:
    def test_root_folder(self,custom_package):
        """Check naming assumptions are consistent with design."""
        assert(custom_package.root_folder == "MARTe2-automotive")

    def test_package_name_capitalized(self,custom_package):
        assert(custom_package.package_name_capitalized == "Automotive")

odd_package_name = "rObOticS"

@pytest.fixture
def odd_package():
    """Default Package object as fixture for tests."""
    return Package(package_name = odd_package_name)

class TestOddPackage:
    """
    Note that the decision to canonicalise the provided package argument via
    the capitalize method implies a need to similarly canonicalise the root
    folder.
    """
    def test_root_folder(self,odd_package):
        """Check naming assumptions are consistent with design."""
        assert(odd_package.root_folder == "MARTe2-robotics")

    def test_package_name_capitalized(self, odd_package):
        assert(odd_package.package_name_capitalized == "Robotics")


