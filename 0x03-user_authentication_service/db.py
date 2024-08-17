#!/usr/bin/env python3

"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError

from user import Base, User


class DB:
    """
    DB Class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """

        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized the session object
        """

        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()

        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Save the user to the database

        Args:
            email: the user's email address(string)
            hashed_password: the user's hashed password(string)

        Returns:
            The newly created User object
        """

        new_user = User(email=email, hashed_password=hashed_password)
        try:
            self._session.add(new_user)
            self._session.commit()
        except Exception as e:
            print("Failed to add user to the database: {e}")
            self._session.rollback()
            raise

        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
         Finds a user based on keyword arguments.

         Args:
            **kwargs: Arbitrary keyword arguments used for filtering the query.

        Return:
            The first user that matches the filtering criteria.
            or reises an exception

        Raises:
            NoResultFound: no results found matching filter criteria
            InvalidRequestError: when wrong query arguments are passed

            """

        query = self._session.query(User)

        'filter based on the provided arbitrary keyword argument'
        for key, value in kwargs.items():
            'check if the attribute exist in User model'
            if not hasattr(User, key):
                raise InvalidRequestError(f"Invalid Argument passed: {key}")
            query = query.filter(getattr(User, key) == value)

        user = query.one()

        if user is None:
            raise NoResultFount("No user Found")

        return user
