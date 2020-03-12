import pytest
from botocore.stub import Stubber
import botocore.session

from kk.kk import RdsStack

rds = botocore.session.get_session().create_client('rds')


@pytest.fixture(autouse=True)
def rds_stub():
    with Stubber(rds.meta.client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()
