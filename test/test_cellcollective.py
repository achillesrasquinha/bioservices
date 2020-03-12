import pytest

from bioservices import CellCollective, CCAuthenticationError

@pytest.fixture
def cellcollective():
    return CellCollective(verbose=True)

def test_ping(cellcollective):
    cellcollective.ping()

def test_auth(cellcollective):
    cellcollective.auth(
        username="test@cellcollective.org",
        password="test"
    )

    with pytest.raises(CCAuthenticationError):
        cellcollective.auth(
            username="foobar",
            password="foobar"
        )