#Base user manages

from abc import ABC, abstractmethod


class UserManagerABC(ABC):
    '''Abstract class'''

    @abstractmethod
    def authanticate(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    @abstractmethod
    def refresh_tokens(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    