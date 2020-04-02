import pytest
from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_get_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    res = testapp.get('/people/' + str(instance.id) + '/mutual_friends?target_id=' + str(target.id))

    assert res.status_code == HTTPStatus.OK

    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person


def test_get_mutual_friends_correct_data(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person=instance)
    ConnectionFactory.create_batch(5, to_person=target)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person=instance, to_person=f, connection_type='friend')
        ConnectionFactory(from_person=target, to_person=f, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person=instance, to_person=decoy, connection_type='coworker')
    ConnectionFactory(from_person=target, to_person=decoy, connection_type='coworker')

    db.session.commit()

    # call mutual_friends endpoints
    res_a = testapp.get('/people/' + str(instance.id) +
                        '/mutual_friends?target_id=' + str(target.id))
    res_b = testapp.get('/people/' + str(target.id) +
                        '/mutual_friends?target_id=' + str(instance.id))

    assert res_a.status_code == HTTPStatus.OK
    assert res_b.status_code == HTTPStatus.OK

    # confirm that both calls return the same values
    instance_f_ids = [f['id'] for f in res_a.json]
    target_f_ids = [f['id'] for f in res_b.json]

    assert set(instance_f_ids) == set(target_f_ids)
