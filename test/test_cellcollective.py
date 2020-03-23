import pytest

from bioservices import CellCollective
from bioservices.cellcollective import CCAuthenticationError

@pytest.fixture
def cellcollective():
    return CellCollective(verbose=True)

def keys_exists(dict_, keys, test = all):
    return test(key in dict_ for key in keys)

def test_ping(cellcollective):
    cellcollective.ping()

def test_auth(cellcollective):
    cellcollective.auth(
        username="test@cellcollective.org",
        password="test"
    )
    assert cellcollective.authenticated

    with pytest.raises(CCAuthenticationError):
        cellcollective.auth(
            username="abcdefg",
            password="hikjlmnop"
        )

def test_get_models(cellcollective):
    response = cellcollective.get_models()
    assert len(response)
    assert keys_exists(response[0], ("model", "modelPermissions", "hash", "metadataValueMap"), test = any)