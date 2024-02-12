from __future__ import annotations
from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from page_object.add_job_page.add_job_page import AddJobPage
    from page_object.job_detail_page import JobDetailPage

HOST_NUMBERS = [
    pytest.param(0,id='first_host'),
    pytest.param(-1,id='last_host'),
]


@pytest.fixture
def job_detail_page(add_job_page:AddJobPage) -> JobDetailPage:
    input_settings = add_job_page.open_input_settings()

    input_settings.goto_attach_new_hash_list().input_hashes_manually(['c0b51c46e4dcde6189e48ec9695fe55efc0ea703'],'sha1')

    attack_settings = add_job_page.open_attack_settings()

    dictionary_settings = attack_settings.choose_dictionary_mode()

    dictionary_settings.select_dictionaries(['darkweb2017-top1000.txt'])

    job_detail_page = add_job_page.create_job()

    if len(job_detail_page.get_available_hosts()) < 2:
        pytest.fail('To run this test, you must have two or more hosts connected.')

    return job_detail_page


def test_selecting_zero_hosts_appears(job_detail_page:JobDetailPage):
    job_detail_page.select_hosts_for_job([])

    assert job_detail_page.get_active_hosts() == []


def test_selecting_all_hosts_appears(job_detail_page:JobDetailPage):
    available_hosts = job_detail_page.get_available_hosts()

    job_detail_page.select_hosts_for_job(available_hosts)

    assert { host.name for host in job_detail_page.get_active_hosts() } == set(available_hosts)


@pytest.mark.parametrize('desired_host_number',HOST_NUMBERS)
def test_selecting_one_host_appears(job_detail_page:JobDetailPage,desired_host_number:int):
    available_hosts = job_detail_page.get_available_hosts()
    desired_host = available_hosts[desired_host_number]

    job_detail_page.select_hosts_for_job([desired_host])

    assert [ host.name for host in job_detail_page.get_active_hosts() ] == [desired_host]

@pytest.mark.parametrize('desired_host_number',HOST_NUMBERS)
def test_progress_will_only_show_selected_host(job_detail_page:JobDetailPage,desired_host_number:int):
    available_hosts = job_detail_page.get_available_hosts()
    desired_host = available_hosts[desired_host_number]

    job_detail_page.select_hosts_for_job([desired_host])

    job_detail_page.start_job()

    job_detail_page.wait_until_job_finished(600)

    for workunit in job_detail_page.get_workunits():
        assert workunit.host == desired_host.rsplit(' (',1)[0]
