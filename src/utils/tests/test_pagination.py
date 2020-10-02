import pytest
from django.conf import settings

from utils import pagination
from utils.errors import CustomApiError


def test_offset_and_limit():
    offset, limit = pagination.get_offset_and_limit(5)
    assert offset == settings.PAGE_SIZE * 4
    assert limit == settings.PAGE_SIZE

    offset, limit = pagination.get_offset_and_limit(1)
    assert offset == 0
    assert limit == settings.PAGE_SIZE


def test_start_and_end():
    start, end = pagination.get_start_and_end(5)
    assert start == settings.PAGE_SIZE * 4
    assert end == (settings.PAGE_SIZE * 4) + settings.PAGE_SIZE

    start, end = pagination.get_start_and_end(1)
    assert start == 0
    assert end == settings.PAGE_SIZE


def test_non_positive_page():
    with pytest.raises(CustomApiError) as ex_info:
        pagination.get_offset_and_limit(-1)
    assert ex_info.value.code == 'invalid-page'

    with pytest.raises(CustomApiError) as ex_info:
        pagination.get_offset_and_limit(0)
    assert ex_info.value.code == 'invalid-page'
