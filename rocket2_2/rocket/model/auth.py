# -*- coding: utf-8 -*-
"""
Auth* related model.
"""
import os
from datetime import datetime
from hashlib import sha256

__all__ = ['User', 'Role', 'Permission']

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession


# This is the association table for the many-to-many relationship between
# roles and permissions.
role_permission_table = Table('role_permission', metadata,
                               Column('role_id', Integer, ForeignKey('role.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
                               Column('permission_id', Integer, ForeignKey('permission.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))


# This is the association table for the many-to-many relationship between
# roles and members - this is, the memberships.
user_role_table = Table('user_role', metadata,
                         Column('user_id', Integer, ForeignKey('user.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True),
                         Column('role_id', Integer, ForeignKey('role.id', onupdate="CASCADE", ondelete="CASCADE"), primary_key=True))


class Role(DeclarativeBase):
    """ Role definition """

    __tablename__ = 'role'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(50), unique=True, nullable=False)
    description = Column(Unicode(255))
    persistant = Column(Boolean, default=True)
    created = Column(DateTime, default=datetime.now)
    users = relation('User', secondary=user_role_table, backref='roles')

    def __repr__(self):
        return '<Role: name=%s>' % repr(self.name)

    def __unicode__(self):
        return self.name


class User(DeclarativeBase):
    """ User definition. """

    __tablename__ = 'user'

    id = Column(Integer, autoincrement=True, primary_key=True)
    username = Column(Unicode(255), unique=True, nullable=False)
    name = Column(Unicode(255))
    email = Column(Unicode(255), unique=True)
    mobile = Column(Unicode(255))
    _password = Column('password', Unicode(128))
    role_id = Column(Integer)
    created = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)
    added_by = Column(Integer, nullable=False)

    def __repr__(self):
        return '<User: name=%s, email=%s, mobile=%s>' % (
            repr(self.username),
            repr(self.email),
            repr(self.mobile),
        )

    def __unicode__(self):
        return self.display_name or self.username

    @property
    def permissions(self):
        """Return a set with all permissions granted to the user."""
        perms = set()
        for g in self.roles:
            perms = perms | set(g.permissions)
        return perms

    @classmethod
    def by_id(cls, id):
        """Return the user object whose id address is ``id``."""
        return DBSession.query(cls).filter_by(id=id).first()

    @classmethod
    def by_email(cls, email):
        """Return the user object whose email address is ``email``."""
        return DBSession.query(cls).filter_by(email=email).first()

    @classmethod
    def by_username(cls, username):
        """Return the user object whose user name is ``username``."""
        return DBSession.query(cls).filter_by(username=username).first()

    @classmethod
    def _hash_password(cls, password):
        salt = sha256()
        salt.update(os.urandom(60))
        salt = salt.hexdigest()

        hash = sha256()
        # Make sure password is a str because we cannot hash unicode objects
        hash.update((password + salt).encode('utf-8'))
        hash = hash.hexdigest()

        password = salt + hash

        return password

    def _set_password(self, password):
        """Hash ``password`` on the fly and store its hashed version."""
        self._password = self._hash_password(password)

    def _get_password(self):
        """Return the hashed version of the password."""
        return self._password

    password = synonym('_password', descriptor=property(_get_password,
                                                        _set_password))

    def validate_password(self, password):
        """
        Check the password against existing credentials.

        : param password: the password that was provided by the user to
            try and authenticate. This is the clear text version that we will
            need to match against the hashed one in the database.
        : type password: unicode object.
        : return: Whether the password is valid.
        : rtype: bool

        """
        hash = sha256()
        hash.update((password + self.password[: 64]).encode('utf-8'))
        return self.password[64: ] == hash.hexdigest()


class Permission(DeclarativeBase):
    """ Permission definition."""

    __tablename__ = 'permission'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(63), unique=True, nullable=False)
    description = Column(Unicode(255))

    roles = relation(Role, secondary=role_permission_table, backref='permissions')

    def __repr__(self):
        return '<Permission: name=%s>' % repr(self.name)

    def __unicode__(self):
        return self.name

class SessionKey(DeclarativeBase):
    __tablename__='tbl_sessionkey'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(255), nullable=False)

class SessionValue(DeclarativeBase):
    __tablename__='tbl_sessionvalue'
    id = Column(Integer, autoincrement=True, primary_key=True)
    key_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    value = Column(Unicode(255), nullable=False)

class PasswordHistory(DeclarativeBase):
    __tablename__='tbl_passwordhistory'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    password = Column(Unicode(128), nullable=False)
    added_by = Column(Integer, nullable=False)
    added = Column(DateTime, default=datetime.now)

class UserGuid(DeclarativeBase):
    __tablename__='tbl_userguid'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, nullable=False)
    guid = Column(Unicode(32), nullable=False)
    expires = Column(DateTime, nullable=False)

    @classmethod
    def by_guid(cls, guid):
        return DBSession.query(cls).filter_by(guid=guid).first()
