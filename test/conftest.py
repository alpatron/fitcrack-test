from __future__ import annotations

from typing import NamedTuple, TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    import _pytest.config.argparsing
    import _pytest.config


class Credentials(NamedTuple):
    user_name : str
    password : str


def pytest_addoption(parser:_pytest.config.argparsing.Parser):
    HELP = 'Fitcrack username and password to be used by tests'
    
    parser.addini('credentials', type='args' ,help=HELP)

    group = parser.getgroup("fitcrack", "fitcrack")
    group.addoption('--credentials',nargs=2,metavar=('username','password'),help=HELP)


def pytest_configure(config:_pytest.config.Config):
    config.option.credentials = Credentials(*(
        config.getoption('credentials')
        or config.getini('credentials')
        or ('fitcrack', 'FITCRACK')
    )) #type: ignore


def pytest_report_header(config:_pytest.config.Config, startdir):
    credentials:Credentials = config.getoption('credentials') #type: ignore
    return f'fitcrack username: {credentials.user_name}\nfitcrack password: {credentials.password}'


@pytest.fixture(scope='session')
def credentials(config:_pytest.config.Config) -> Credentials:
    return config.getoption('credentials') #type: ignore
