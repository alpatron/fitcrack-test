"""This module is used to perform all the necessary pytest configuration 
and define all the used custom fixtures used for testing Fitcrack.

For detailed information about conftest.py files, see
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-plugins
"""
from __future__ import annotations

from datetime import datetime
from typing import NamedTuple, Tuple, TYPE_CHECKING

import pytest

from page_object.login_page import LoginPage

if TYPE_CHECKING:
    import _pytest.config.argparsing
    import _pytest.config
    import _pytest.fixtures
    from selenium.webdriver.remote.webdriver import WebDriver

    from page_object.dashboard import Dashboard
    from page_object.side_bar import SideBar


class Credentials(NamedTuple):
    """Named tuple for Fitcrack login credentials"""
    user_name : str
    password : str


def pytest_addoption(parser:_pytest.config.argparsing.Parser):
    """Configures pytest to accept custom test-configuration parameters used by the test suite
    (with the exception of parameters handled by other pytest plugins that the test suite uses,
    like `base_url` and `--driver`, which are handled by pytest-selenium).
    
    This is a special function used by pytest.
    Relevant pytest documentation: https://docs.pytest.org/en/6.2.x/reference.html#pytest.hookspec.pytest_addoption
    """

    HELP = 'Fitcrack username and password to be used by tests'
    
    parser.addini('credentials', type='args' ,help=HELP)

    group = parser.getgroup("fitcrack", "fitcrack")
    group.addoption('--credentials',nargs=2,metavar=('username','password'),help=HELP)


def pytest_configure(config:_pytest.config.Config):
    """Handles the processing of custom test-configuration parameters.

    Parameters are first taken from command-line options,
    then pytest configuration files, and finally default values
    are used if parameters aren't input.

    This is a special function used by pytest.
    Relevant pytest documentation: https://docs.pytest.org/en/6.2.x/reference.html#pytest.hookspec.pytest_configure
    """
    config.option.credentials = Credentials(*(
        config.getoption('credentials')
        or config.getini('credentials')
        or ('fitcrack', 'FITCRACK')
    )) #type: ignore


def pytest_report_header(config:_pytest.config.Config, startdir):
    """Configures pytest to display the custom test-configuration parameters that are set
    and will be used for the current test session at the beginning of the test report.

    This is a special function used by pytest.
    Relevant pytest documentation: https://docs.pytest.org/en/6.2.x/reference.html#pytest.hookspec.pytest_report_header
    """
    
    credentials:Credentials = config.getoption('credentials') #type: ignore
    return [
        f'fitcrack username: {credentials.user_name}',
        f'fitcrack password: {credentials.password}'
    ]


@pytest.fixture(scope='session')
def credentials(pytestconfig:_pytest.config.Config) -> Credentials:
    """Fixture that returns the configured login credentials. Login credentials should be valid."""
    return pytestconfig.getoption('credentials') #type: ignore

