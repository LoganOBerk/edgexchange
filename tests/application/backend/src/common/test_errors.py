import pytest

from common import errors

def test_database_error():
    with pytest.raises(errors.DatabaseError):
        raise errors.DatabaseError()


def test_validation_error():
    with pytest.raises(errors.ValidationError):
        raise errors.ValidationError()


def test_service_error():
    with pytest.raises(errors.ServiceError):
        raise errors.ServiceError()


def test_fetching_error():
    with pytest.raises(errors.FetchingError):
        raise errors.FetchingError()


def test_fetching_error_msg():
    with pytest.raises(errors.FetchingError) as e:
        raise errors.FetchingError(message = "Test")
    
    assert str(e.value) == "Test" and e.value.message == "Test"


def test_fetching_error_ticker():
    with pytest.raises(errors.FetchingError) as e:
        raise errors.FetchingError(ticker = "AAPL")
    
    assert e.value.ticker == "AAPL"


def test_empty_fetching_error():
    with pytest.raises(errors.FetchingError) as e:
        raise errors.FetchingError()

    assert str(e.value) == "None" and e.value.message == None and e.value.ticker == None


def test_full_fetching_error():
    with pytest.raises(errors.FetchingError) as e:
        raise errors.FetchingError(message = "Test", ticker = "AAPL")

    assert str(e.value) == "Test" and e.value.message == "Test" and e.value.ticker == "AAPL"


def test_livecache_error():
    with pytest.raises(errors.LiveCacheError):
        raise errors.LiveCacheError()