from enum import StrEnum

from pydantic import BaseModel


class SortOrder(StrEnum):
    ASC = "asc"
    DESC = "desc"


class UserSortField(StrEnum):
    CREATED_AT = "created_at"
    NAME = "name"
    EMAIL = "email"
    ROLE = "role"


class UserSortingParams(BaseModel):
    sort_by: UserSortField = UserSortField.CREATED_AT
    sort_order: SortOrder = SortOrder.DESC