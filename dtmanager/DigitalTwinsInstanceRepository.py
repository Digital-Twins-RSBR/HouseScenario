
from abc import ABC,abstractmethod
from .DigitalTwinModelRepository import DTDLModel,ModelElement
import uuid
class DigitalTwin:
    def __init__(self,ID,ModelID,Name,attributes=None):
        self.ID=ID
        self.Name=Name
        self.ModelID=ModelID
        self.attributes=attributes if attributes else []
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
    def create_from_model(self,model:DTDLModel)->DigitalTwin:

        id=str(uuid.uuid4())
        model_id=model.id
        name=model.name
        attributes=[]
        modelElementObjects=[ModelElement(**element) for element in model.modelElements]
        for element in modelElementObjects:
            att={"Type": element.type,"Name": element.name,"Value": "","Schema": element.schema,"Causal": element.isCausal(),"Characteristics": element.supplementTypes}
            attributes.append(att)
        dt=DigitalTwin(id,model_id,name,attributes)
        self.insert_digital_twin(dt)
        return dt

        
