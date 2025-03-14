# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import platform
from .version import VERSION

USER_AGENT = "azsdk-python-appconfiguration/{} Python/{} ({})".format(
    VERSION, platform.python_version(), platform.platform()
)