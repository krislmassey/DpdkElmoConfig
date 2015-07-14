'''
Download test_cli Python Package
--------------------------------

The test_cli Python package can be downloaded from
:releasezip:`here <http://elmo.adtran.com/doc/api>`.

.. warning:: The test_cli does **not** support Python 3!  Please use Python 2.7.

.. warning:: Currently, this package does **not** support ELMO units with firmware below version, 2.1.0.

Firmware upgrades can be downloaded from: `ELMO Firmware <http://elmo.adtran.com/firmware>`_. Please
use the latest available production version, if possible, especially before reporting bugs.

Bugs and feature requests should be reported to:
`Trevor Bowen <mailto:trevor.bowen@adtran.com?subject=test_cli>`_.

Introduction to test_cli Python Package
---------------------------------------

ELMO test automation is supported via the test_cli package. The test_cli package provides a generic
driver for **any** local, telnet, or ssh CLI process that accepts input commands via STDIN,
preceded by a prompt. Convenience functions are provided for submitting commands and verifying
output based on strict matching, whitespace insensitive matching, case insensitive matching, and
regular expressions.

An ELMO-specific test automation reference driver (:class:`.elmo.ElmoTelnetConnection`) and
connection factory (:func:`.elmo.ElmoConnection`) is included to provide connections to ELMO units.

.. note:: Please use the connection factory (:func:`.elmo.ElmoConnection`) for **all** ELMO connections.

A demonstration of a test program using the driver is included in the :mod:`.demo` module.  Please
examine the `source code <_modules/test_cli/demo.html>`_ of that module for exemplary usage.

The test_cli package consists of the following essential classes and functions for ELMO test
automation:

* :func:`.elmo.ElmoConnection` - Factory function used to create connections with automatically \
defined parsers.
* :class:`.elmo.ElmoPipeConnection` - Connection to local ELMO CLI via Unix pipes, returned by \
:func:`.elmo.ElmoConnection`.
* :class:`.elmo.ElmoTelnetConnection` - Connection to remote ELMO CLI over Telnet, returned by \
:func:`.elmo.ElmoConnection`.
* :class:`.elmo.ElmoSSHConnection` - Connection remote ELMO CLI over SSH, manually created and not \
preferred because of paramiko package dependency.

.. note:: The command output parsers for the ELMO driver are detailed in the `ELMO Parsers`_ section.

The test_cli package also includes the following generic classes, which can be used to drive **any**
CLI process:

* :class:`.pipe.PipeConnection` - Connection to any local CLI process through a Unix Pipe.
* :class:`.telnet.TelnetConnection` - Connection to a remote CLI process through a Telnet session.
* :class:`.ssh.SSHConnection` - Connection to a remote CLI process through a SSH session.

Some additional utilty functions are provided in the :mod:`.utils` module to facilitate parsing and
analysis of output text.

.. warning:: Currently, there are **no** parsers available for any firmware below version, 2.1.0.

Firmware upgrades can be downloaded from: `ELMO Firmware <http://elmo.adtran.com/firmware>`_.

.. note:: The test_cli archive for |release| can be downloaded from \
:releasezip:`here <http://elmo.adtran.com/doc/api>`.
'''
__version__ = '2.2.0'
__author__ = 'Trevor Bowen <trevor.bowen@adtran.com>'
__all__ = [
           'approx_eq',
           'approx_ge',
           'PipeConnection',
           # 'SSHConnection',
           'TelnetConnection',
           'ElmoConnection',
           ]
from test_cli.utils import approx_eq, approx_ge
from test_cli.pipe import PipeConnection
# from .ssh import SSHConnection
from test_cli.telnet import TelnetConnection
from test_cli.elmo import ElmoConnection
