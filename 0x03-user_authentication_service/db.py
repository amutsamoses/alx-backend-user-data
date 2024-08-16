#!/usr/bin/env python3

"""
DB module
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import Session

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
                self.session.add(new_user)
                self.session.commit()
            except Exception as e:
                print("Failed to add user to the database: {e}")
                self._session.rollback()
                raise

            return new_user
