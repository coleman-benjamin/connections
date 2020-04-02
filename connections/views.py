from http import HTTPStatus

from flask import Blueprint, abort
from webargs import fields
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection
from connections.schemas import ConnectionSchema, UpdateConnectionTypeSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    people = Person.query.all()
    return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people/<person_id>/mutual_friends', methods=['GET'])
@use_args({'target_id': fields.Integer(required=True)})
def get_mutual_friends(args, person_id):
    people_schema = PersonSchema(many=True)
    personA = Person.query.get(person_id)
    personB = Person.query.get(args['target_id'])

    if not personA or not personB:
        abort(404)

    return people_schema.jsonify(personA.mutual_friends(personB)), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
    connection_schema = ConnectionSchema(many=True)
    connections = Connection.query.all()
    return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
@use_args(UpdateConnectionTypeSchema(), locations=('json',))
def update_connection_type(request, connection_id):
    connection = Connection.query.get(connection_id)
    if not connection:
        abort(404)

    connection.connection_type = request.connection_type
    return UpdateConnectionTypeSchema().jsonify(connection), HTTPStatus.OK
