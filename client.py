from dtmanager.DigitalTwinModelRepository import ModelManager,DTDLSpecification
from dtmanager.DigitalTwinsInstanceRepository import DigitalTwinInstanceManager
from dtmanager.RepositoryNeo4J import DigitalTwinsInstaceManagerNeo4j
import json
# Step 1 - Create Model Manager

parser_endpoint='http://10.255.255.254:53192'

modelRepository=ModelManager(parser_endpoint)

with open("Room.json","r") as file:
    spec_data=json.load(file)

model_1=DTDLSpecification(id="dtmi:housegen:Room;1",specification=spec_data)

modelRepository.parserDTDLModel(model_1)

modelRoom=modelRepository.getDTDLModel("dtmi:housegen:Room;1")

print(modelRoom)