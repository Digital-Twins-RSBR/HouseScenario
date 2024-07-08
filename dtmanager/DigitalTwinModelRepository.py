import requests
from dataclasses import dataclass,field
from typing import List,Optional

@dataclass
class ModelElement:
    id:int
    type:Optional[str]=None
    name:Optional[str]=None
    schema:Optional[str]=None
    supplementTypes:Optional[List[str]]=None

    def isCausal(self)->bool:
        if self.supplementTypes:
            return "dtmi:dtdl:extension:causal:v1:Causal" in self.supplementTypes
        return False
@dataclass
class ModelRelationship:
    id: int
    name: Optional[str] = None
    target: Optional[str] = None

@dataclass
class DTDLModel:
    id: Optional[str] = None
    name: Optional[str] = None
    modelElements: Optional[List[ModelElement]] = None
    modelRelationships: Optional[List[ModelRelationship]] = None

@dataclass
class DTDLSpecification:
    id: Optional[str] = None
    specification: Optional[dict] = None


class ModelManager:
    def __init__(self,parser_endpoint) -> None:
        self.parser=DTDLParserClient(parser_endpoint)
        self.models:List[DTDLModel]=[]
    def parserDTDLModel(self,specification:DTDLSpecification):
        model=self.parser.parse_specification(specification)
        self.models.append(model)
    def getDTDLModel(self,modelID:str) ->Optional[DTDLModel]:
        for model in self.models:
            if modelID==model.id:
                return model
        return None

class DTDLParserClient:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def get_all_models(self) -> List[DTDLModel]:
        response = requests.get(f"{self.base_url}/api/DTDLModels")
        response.raise_for_status()
        models_data = response.json()
        return [DTDLModel(**model) for model in models_data]

    def get_model_by_id(self, model_id: str) -> DTDLModel:
        response = requests.get(f"{self.base_url}/api/DTDLModels/{model_id}")
        response.raise_for_status()
        model_data = response.json()
        return DTDLModel(**model_data)

    def delete_model_by_id(self, model_id: str) -> None:
        response = requests.delete(f"{self.base_url}/api/DTDLModels/{model_id}")
        response.raise_for_status()

    def parse_specification(self, specification: DTDLSpecification) -> DTDLModel:
        response = requests.post(
            f"{self.base_url}/api/DTDLModels/parse",
            json=specification.__dict__
        )
        response.raise_for_status()
        model_data = response.json()
        return DTDLModel(**model_data)