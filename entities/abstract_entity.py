from abc import ABC, abstractmethod

class AbstractEntity(ABC):

  @abstractmethod
  def prepare(self):
    pass

  @abstractmethod
  def execute(self):
    pass

  @abstractmethod
  def cleanup(self):
    pass
