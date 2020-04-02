from http import HTTPStatus

import pytest

from tests.factories import PersonFactory, ConnectionFactory
from connections.models.connection import ConnectionType


@pytest.fixture
def connection_payload():
    return {
        'connection_type': ConnectionType.friend.value,
    }


def test_can_update_connection_type(db, testapp, connection_payload):
    connection = ConnectionFactory.create(connection_type=ConnectionType.father.value)
    db.session.commit()

    res = testapp.patch('/connections/' + str(connection.id), json=connection_payload)

    assert res.status_code == HTTPStatus.OK
    assert res.json['connection_type'] == connection_payload['connection_type']


@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('connection_type', None, 'Field may not be null.',
                 id='missing connection type'),
    pytest.param('connection_type', 'borke', 'Invalid enum member borke',
                 id='invalid connection type')
])
def test_update_connection_type_validations(db, testapp, connection_payload, field, value, error_message):
    connection = ConnectionFactory.create(connection_type=ConnectionType.father)
    db.session.commit()

    connection_payload[field] = value

    res = testapp.patch('/connections/' + str(connection.id), json=connection_payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]


def test_connection_not_found(db, testapp, connection_payload):
    res = testapp.patch('/connections/123', json=connection_payload)

    assert res.status_code == HTTPStatus.NOT_FOUND
