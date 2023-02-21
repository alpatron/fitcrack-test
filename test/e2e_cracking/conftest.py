"""Common fixture and common test-input dataclass used by end-to-end cracking tests.

For detailed information about conftest.py files, see
https://docs.pytest.org/en/6.2.x/fixture.html#conftest-py-sharing-fixtures-across-multiple-files
"""
from __future__ import annotations
from dataclasses import dataclass, KW_ONLY
from typing import TYPE_CHECKING, List
from datetime import datetime

import pytest
from selenium.webdriver.support.wait import WebDriverWait

if TYPE_CHECKING:
    import _pytest.fixtures
    from selenium.webdriver.remote.webdriver import WebDriver
    from page_object.add_job_page.add_job_page import AddJobPage
    


@dataclass
class GenericE2ECrackingTestInput:
    """A generic dataclass to be inherited from for the use in end-to-end cracking tests.
    Contains hash type and a list of hashes and their expected cracked output since
    all end-to-end cracking tests input hashes at the start and check results at the end.
    And contains the maximum time the test should wait for the cracking result after starting
    the job (in seconds); the default wait time is one hour.
    """
    hash_type:str
    hashes:List[tuple[str,str]]
    _: KW_ONLY
    wait_time:float = 3600


@pytest.fixture
def e2e_cracking_test(selenium:WebDriver,add_job_page:AddJobPage,testdata:GenericE2ECrackingTestInput,request:_pytest.fixtures.FixtureRequest):
    """Fixture for end-to-end cracking tests.
    
    Before the test, it inputs hashes (using the manual mode) and selects the hash type.
    The name of the cracking job is set to indicate the currently run test.
    It then yields control to the test function so that the test can set up the cracking task.
    After the test function ends, the fixture starts the cracking job, waits for the cracking job
    to end, and then checks the output of the cracking task and compares it to the test data.

    This fixture expects Webadmin be on the Add Job page at the beginning and end of the test.

    This fixture requires the test function to use a "testdata" fixture that provides a
    GenericE2ECrackingTestInput or derived object (see concrete test implementations for example.)
    """
    add_job_page.set_job_name(f'Job created by an automatic Fitcrack test -- {request.node.name} -- {datetime.utcnow().isoformat()}')
    
    input_settings = add_job_page.open_input_settings()
    input_settings.select_hash_type_exactly(testdata.hash_type)
    input_settings.input_hashes_manually([x[0] for x in testdata.hashes])
    
    yield
    
    job_detail_page = add_job_page.create_job()
    assert job_detail_page.get_job_state() == 'Ready'
    job_detail_page.start_job()
    WebDriverWait(selenium,testdata.wait_time).until(lambda _: job_detail_page.get_job_state() == 'Finished')
    worked_on_hashes = job_detail_page.get_hashes()
    assert set(worked_on_hashes) == set(testdata.hashes)