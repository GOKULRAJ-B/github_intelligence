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
    pull_requests = relationship(
    "PullRequest",
    back_populates="repository",
    cascade="all, delete-orphan",
    )
    daily_metrics = relationship(
    "DailyMetric",
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
    pull_requests = relationship(
    "PullRequest",
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

class PullRequest(Base):

    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True)

    pr_number = Column(
        Integer,
        nullable=False,
    )

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False,
    )

    contributor_id = Column(
        Integer,
        ForeignKey("contributors.id"),
        nullable=False,
    )

    title = Column(
        String(500),
        nullable=False,
    )

    state = Column(
        String(50),
        nullable=False,
    )

    created_at = Column(DateTime)

    merged_at = Column(DateTime)

    closed_at = Column(DateTime)

    merge_time_minutes = Column(Integer)

    repository = relationship(
        "Repository",
        back_populates="pull_requests",
    )

    contributor = relationship(
        "Contributor",
        back_populates="pull_requests",
    )
class DailyMetric(Base):

    __tablename__ = "daily_metrics"

    id = Column(Integer, primary_key=True)

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False,
    )

    metric_date = Column(
        DateTime,
        nullable=False,
    )

    total_commits = Column(
        Integer,
        default=0,
    )

    merged_prs = Column(
        Integer,
        default=0,
    )

    open_prs = Column(
        Integer,
        default=0,
    )

    avg_merge_time = Column(
        Integer,
        default=0,
    )

    active_contributors = Column(
        Integer,
        default=0,
    )

    repository = relationship(
        "Repository",
        back_populates="daily_metrics",
    )
class FileHotspot(Base):
    __tablename__ = "file_hotspots"

    id = Column(
        Integer,
        primary_key=True,
    )

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False,
    )

    file_path = Column(
        String(500),
        nullable=False,
    )

    commit_count = Column(
        Integer,
        default=0,
    )

class DeveloperRanking(Base):
    __tablename__ = "developer_rankings"

    id = Column(Integer, primary_key=True)

    contributor_id = Column(
        Integer,
        ForeignKey("contributors.id"),
        nullable=False,
    )

    repository_id = Column(
        Integer,
        ForeignKey("repositories.id"),
        nullable=False,
    )

    total_commits = Column(Integer, default=0)

    merged_prs = Column(Integer, default=0)

    score = Column(Integer, default=0)