"""Tool contracts and execution models."""

from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field


class ToolPermission(str, Enum):
    READ = "read"
    WRITE = "write"
    ADMIN = "admin"


class ToolDefinition(BaseModel):
    name: str = Field(..., description="Unique tool name")
    description: str = Field(..., description="What the tool does")
    permission_required: ToolPermission = Field(default=ToolPermission.READ)
    is_write_operation: bool = Field(default=False)
    parameters_schema: dict[str, Any] = Field(default_factory=dict)


class ToolResult(BaseModel):
    tool_name: str
    success: bool
    data: Any = None
    error: Optional[str] = None
    duration_ms: float = 0.0
