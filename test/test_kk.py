from kk.kk import RdsStack

def test_get_clusters(rds_stub):
    rds_stub.add_response(
        'head_object',
        expected_params={},
        service_response={},
    )

    result = RdsStack.get_clusters()

    assert result == ...
