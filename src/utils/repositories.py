#Base repository

from abc import ABC, abstractmethod


class ABCRepository(ABC):
    '''Abstract class'''

    # @abstractmethod
    def get(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    # @abstractmethod
    def create(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    # @abstractmethod
    def update(self, *args, **kwargs):
        '''Method without realization'''

        raise NotImplementedError
    
    # @abstractmethod
    # def delete(self, *args, **kwargs):
    #     raise NotImplementedError
    