from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'from_person',
    'to_person',
]

PEOPLE_EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_can_get_connections(db, testapp):
    personA = PersonFactory()
    personB = PersonFactory()

    ConnectionFactory.create_batch(10, from_person=personA, to_person=personB)

    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for connection in res.json:
        for field in EXPECTED_FIELDS:
            assert field in connection
            for p_field in PEOPLE_EXPECTED_FIELDS:
                assert p_field in connection['from_person']
                assert p_field in connection['to_person']
