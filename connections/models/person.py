from connections.database import CreatedUpdatedMixin, CRUDMixin, db, Model

from connections.models.connection import ConnectionType


class Person(Model, CRUDMixin, CreatedUpdatedMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    email = db.Column(db.String(145), unique=True, nullable=False)

    connections = db.relationship(
        'Connection', foreign_keys='Connection.from_person_id', lazy='dynamic')

    def mutual_friends(self, Person):
        self_friends = self.connections.filter_by(connection_type=ConnectionType.friend)
        other_friends = Person.connections.filter_by(connection_type=ConnectionType.friend)

        mutual_connections = self_friends.union(other_friends)
        result = set(connection.to_person for connection in mutual_connections)

        return result
