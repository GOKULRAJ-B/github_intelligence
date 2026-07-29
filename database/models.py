from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from database.db import Base


class Repository(Base):

    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True)

    name = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    commits = relationship(
        "Commit",
        back_populates="repository",
        cascade="all, delete-orphan",
    )


class Contributor(Base):

    __tablename__ = "contributors"

    id = Column(Integer, primary_key=True)

    username = Column(
        String(255),
        unique=True,
        nullable=False,
    )

    commits = relationship(
        "Commit",
        back_populates="contributor",
        cascade="all, delete-orphan",
    )


class Commit(Base):

    __tablename__ = "commits"

    id = Column(Integer, primary_key=True)

    commit_sha = Column(
        String(64),
        unique=True,
        nullable=False,
    )

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
    )

    contributor_id = Column(
        Integer,
        ForeignKey("contributors.id"),
    )

    message = Column(String)

    commit_time = Column(DateTime)

    repository = relationship(
        "Repository",
        back_populates="commits",
    )

    contributor = relationship(
        "Contributor",
        back_populates="commits",
    )