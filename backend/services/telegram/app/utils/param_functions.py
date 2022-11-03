# Code from fastapi. See more https://github.com/tiangolo/fastapi
from typing import Optional, Callable, Any


class _depends:
    def __init__(
            self, dependency: Optional[Callable[..., Any]] = None, *, use_cache: bool = True
    ) -> None:
        self.dependency = dependency
        self.use_cache = use_cache

    def __repr__(self) -> str:
        attr = getattr(self.dependency, "__name__", type(self.dependency).__name__)
        cache = "" if self.use_cache else ", use_cache=False"
        return f"{self.__class__.__name__}({attr}{cache})"


def depends(dependency: Optional[Callable[..., Any]] = None, *, use_cache: bool = True) -> Any:
    return _depends(dependency=dependency, use_cache=use_cache)
