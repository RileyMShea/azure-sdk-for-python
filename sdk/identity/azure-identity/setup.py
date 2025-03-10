#!/usr/bin/env python

# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import re
import os.path
from io import open
from setuptools import find_packages, setup

PACKAGE_NAME = "azure-identity"
PACKAGE_PPRINT_NAME = "Identity"

package_folder_path = PACKAGE_NAME.replace("-", "/")
namespace_name = PACKAGE_NAME.replace("-", ".")

# azure v0.x is not compatible with this package
# azure v0.x used to have a __version__ attribute (newer versions don't)
try:
    import azure

    try:
        ver = azure.__version__
        raise Exception(
            "This package is incompatible with azure=={}. ".format(ver) + 'Uninstall it with "pip uninstall azure".'
        )
    except AttributeError:
        pass
except ImportError:
    pass

with open(os.path.join(package_folder_path, "_version.py"), "r") as fd:
    VERSION = re.search(r'^VERSION\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE).group(1)
if not VERSION:
    raise RuntimeError("Cannot find version information")

with open("README.md", encoding="utf-8") as f:
    README = f.read()
with open("HISTORY.md", encoding="utf-8") as f:
    HISTORY = f.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Microsoft Azure {} Library for Python".format(PACKAGE_PPRINT_NAME),
    long_description=README + "\n\n" + HISTORY,
    long_description_content_type="text/markdown",
    license="MIT License",
    author="Microsoft Corporation",
    author_email="azpysdkhelp@microsoft.com",
    url="https://github.com/Azure/azure-sdk-for-python/tree/master/sdk/identity/azure-identity",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    zip_safe=False,
    packages=find_packages(
        exclude=[
            "tests",
            # Exclude packages that will be covered by PEP420 or nspkg
            "azure",
        ]
    ),
    install_requires=["azure-core<2.0.0,>=1.0.0b2", "cryptography>=2.1.4", "msal~=0.4.1", "six>=1.6"],
    extras_require={
        ":python_version<'3.0'": ["azure-nspkg"],
        ":python_version<'3.3'": ["mock"],
        ":python_version<'3.5'": ["typing"],
    },
)
