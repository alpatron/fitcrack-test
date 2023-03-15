"""This module is used to perform all the necessary pytest configuration 
and define all the used custom fixtures used for testing Fitcrack.

For detailed information about conftest.py files, see
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
https://docs.pytest.org/en/6.2.x/writing_plugins.html#conftest-py-plugins
"""
from __future__ import annotations
from typing import NamedTuple, Tuple, TYPE_CHECKING
from datetime import datetime
import shutil

import pytest

from page_object.login_page import LoginPage

if TYPE_CHECKING:
    from pathlib import Path
    
    import _pytest.config.argparsing
    import _pytest.config
    import _pytest.fixtures
    from selenium.webdriver.remote.webdriver import WebDriver

    from page_object.dashboard import Dashboard
    from page_object.side_bar import SideBar
    from page_object.add_job_page.add_job_page import AddJobPage


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


@pytest.fixture(scope='session',autouse=True)
def require_base_url(base_url) -> None:
    """Fixture that fixes a problem in pytest-selenium.
    Forces the display of an error message if base_url is not set.
    pytest-selenium would normally cause a cryptic error to occur.
    """
    if not base_url:
        raise pytest.UsageError(
            'base_url is not set; use `pytest --base-url https://example.com` '
            'or set base_url in pytest.ini'
            )


@pytest.fixture(scope='session')
def credentials(pytestconfig:_pytest.config.Config) -> Credentials:
    """Fixture that returns the configured login credentials. Login credentials should be valid."""
    return pytestconfig.getoption('credentials') #type: ignore


@pytest.fixture
def login_page(selenium:WebDriver,base_url:str) -> LoginPage:
    """Fixture that navigates to login page and returns a LoginPage object."""
    login_page = LoginPage(selenium,no_ensure_loaded=True)
    login_page.navigate(base_url)
    login_page.ensure_loaded()
    return login_page


@pytest.fixture
def _start_logged_in(login_page:LoginPage,credentials:Credentials) -> Tuple[SideBar,Dashboard]:
    """You probably want to use the side_bar and dashboard fixtures instead.
    
    Fixture that logs into Fitcrack with the provided default credentials supplied to the test
    session, and returns two values, the SideBar object and the Dashboard object.
    """
    return login_page.login(*credentials)


@pytest.fixture
def side_bar(_start_logged_in:Tuple[SideBar,Dashboard]) -> SideBar:
    """Fixture that logs into Fitcrack and returns a Sidebar object."""
    return _start_logged_in[0]


@pytest.fixture
def dashboard(_start_logged_in:Tuple[SideBar,Dashboard]) -> Dashboard:
    """Fixture that logs into Fitcrack and returns the initial Dashboard object created by the
    initial log in. Beware the object is not useable if you use also use fixtures that navigate
    away from the dashboard.
    """
    return _start_logged_in[1]


@pytest.fixture
def add_job_page(side_bar:SideBar) -> AddJobPage:
    """Fixture that returns an AddJobPage object."""
    add_job_page = side_bar.goto_add_job()
    return add_job_page


@pytest.fixture
def test_file_path(request:_pytest.fixtures.FixtureRequest):
    """Fixture for working with test files in tests.
    This fixture MUST be used with indirect parametrisation.
    The parameter given MUST be of `pathlib.Path` type (or equivalent).
    This fixture yields a `Path` object ready to be used with Selenium for uploading files
    through `<input>` elements.
    The yielded `Path` object is an absolute path to a temporary COPY (!) of the given path.
    The yielded `Path` object has a timestamp appended to the the filename.

    This is useful for testing Webadmin because sometimes filenames cannot be reused;
    appending the timestamp ensures that the filenames are unique for each test.
    """
    test_file_path:Path = request.param.with_stem(f'{request.param.stem}-{datetime.utcnow():%Y%m%d%H%M%S}') # type: ignore
    shutil.copyfile(request.param,test_file_path) # type: ignore 
    yield test_file_path.absolute()
    test_file_path.unlink()

@pytest.fixture
def test_file_text_content(test_file_path):
    with open(test_file_path,'r') as file:
        return file.read()