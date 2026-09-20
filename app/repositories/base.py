"""Async repository protocols. Services depend only on these (ADR-202, NFR-224).

Query objects carry filters, sort and pagination, so services never build
storage-specific queries and a SQL implementation can honour the same contract.
"""

from dataclasses import dataclass, field
from datetime import date
from typing import Protocol
from uuid import UUID

from app.domain.enums import Priority, ProjectStatus, Role, TaskStatus
from app.domain.models import Activity, Progress, Project, Task, User


@dataclass(frozen=True)
class Page[T]:
    items: list[T]
    page: int
    page_size: int
    total: int


@dataclass(frozen=True)
class UserQuery:
    q: str | None = None
    role: Role | None = None
    sort: str = "createdAt"
    descending: bool = False
    page: int = 1
    page_size: int = 20


@dataclass(frozen=True)
class ProjectQuery:
    q: str | None = None
    statuses: list[ProjectStatus] = field(default_factory=list)
    owner_id: UUID | None = None
    sort: str = "createdAt"
    descending: bool = False
    page: int = 1
    page_size: int = 20


@dataclass(frozen=True)
class TaskQuery:
    q: str | None = None
    statuses: list[TaskStatus] = field(default_factory=list)
    priorities: list[Priority] = field(default_factory=list)
    project_ids: list[UUID] = field(default_factory=list)
    assignee_ids: list[UUID] = field(default_factory=list)
    overdue: bool | None = None
    today: date | None = None
    due_before: date | None = None
    due_after: date | None = None
    sort: str = "createdAt"
    descending: bool = False
    page: int = 1
    page_size: int = 20


@dataclass(frozen=True)
class ActivityQuery:
    page: int = 1
    page_size: int = 10


class UserRepository(Protocol):
    async def get(self, user_id: UUID) -> User | None: ...
    async def get_by_email(self, email: str) -> User | None: ...
    async def list(self, query: UserQuery) -> Page[User]: ...
    async def add(self, user: User) -> User: ...
    async def update(self, user: User) -> User: ...
    async def delete(self, user_id: UUID) -> bool: ...
    async def count_leads(self) -> int: ...


class ProjectRepository(Protocol):
    async def get(self, project_id: UUID) -> Project | None: ...
    async def list(self, query: ProjectQuery) -> Page[Project]: ...
    async def add(self, project: Project) -> Project: ...
    async def update(self, project: Project) -> Project: ...
    async def delete(self, project_id: UUID) -> bool: ...
    async def count_by_owner(self, owner_id: UUID) -> int: ...


class TaskRepository(Protocol):
    async def get(self, task_id: UUID) -> Task | None: ...
    async def list(self, query: TaskQuery) -> Page[Task]: ...
    async def add(self, task: Task) -> Task: ...
    async def update(self, task: Task) -> Task: ...
    async def delete(self, task_id: UUID) -> bool: ...
    async def progress_for(self, project_id: UUID) -> Progress: ...
    async def unassign_user(self, user_id: UUID) -> int: ...


class ActivityRepository(Protocol):
    async def add(self, activity: Activity) -> Activity: ...
    async def list(self, query: ActivityQuery) -> Page[Activity]: ...
