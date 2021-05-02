from abc import abstractmethod


class Cloneable:

    @abstractmethod
    def clone(self):
        pass
