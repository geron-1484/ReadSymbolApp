from abc import ABC, abstractmethod
from typing import Optional, Tuple

class CameraBase(ABC):
    @abstractmethod
    def connect(self) -> None:
        pass

    @abstractmethod
    def disconnect(self) -> None:
        pass

    @abstractmethod
    def capture(self) -> Optional[Tuple[bytes, str]]:
        pass

    @abstractmethod
    def is_connected(self) -> bool:
        pass
