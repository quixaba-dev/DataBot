from abc import abstractmethod, ABC
from dataclasses import dataclass, field

@dataclass
class ToolCall:
    name: str
    arguments: dict

@dataclass
class ProviderResponse:
    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)


class BaseProvider(ABC):
    @abstractmethod
    async def generate(self, messages: list, tools: list | None = None) -> ProviderResponse:
        pass