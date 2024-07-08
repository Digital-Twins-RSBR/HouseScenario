
from abc import ABC,abstractmethod
class DigitalTwin:
    def __init__(self,ID,ModelID):
        self.ID=ID
        self.ModelID=ModelID
        self.attributes=[]
class DigitalTwinInstanceManager(ABC):
    def __init__(self,db_connection):
        self.connection=db_connection
    @abstractmethod
    def insert_digital_twin(self,digital_twin):
        pass
    @abstractmethod
    def get_digital_twin(self,ID):
        pass
    @abstractmethod
    def update_digital_twin(self,digital_twin):
        pass
    @abstractmethod
    def delete_digital_twin(self,ID):
        pass
    @abstractmethod
    def create_relationship(self,from_id,target_id,relationship_name):
        pass
    @abstractmethod
    def execute_query(self,query):
        pass