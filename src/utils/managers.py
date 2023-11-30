from abc import ABC, abstractmethod


class UserManagerABC(ABC):

    @abstractmethod
    def authanticate(self, *args, **kwargs):
        raise NotImplementedError
    
    @abstractmethod
    def refresh_tokens(self, *args, **kwargs):
        raise NotImplementedError