from dtmanager.DigitalTwinModelRepository import ModelManager,DTDLSpecification
from dtmanager.DigitalTwinsInstanceRepository import DigitalTwinInstanceManager
from dtmanager.RepositoryNeo4J import DigitalTwinsInstaceManagerNeo4j,Neo4jConnection
import json
# Step 1 - Create Model Manager

parser_endpoint='http://localhost:5251'

modelRepository=ModelManager(parser_endpoint)

with open("Room.json","r") as file:
    spec_data_room=json.load(file)

model_1=DTDLSpecification(id="dtmi:housegen:Room;1",specification=spec_data_room)

modelRepository.parserDTDLModel(model_1)

with open("House.json") as file:
    spec_data_house=json.load(file)

model_2=DTDLSpecification(id="dtmi:housegen:House;1",specification=spec_data_house)

parsed_model_house=modelRepository.parserDTDLModel(model_2)


with open("LightBulb.json") as file:
    spec_data_lightbulb=json.load(file)

model_3=DTDLSpecification(id="dtmi:housegen:LightBulb;1",specification=spec_data_lightbulb)

modelRepository.parserDTDLModel(model_3)

with open("AirConditioner.json") as file:
    spec_data_airconditioner=json.load(file)

model_4=DTDLSpecification(id="dtmi:housegen:AirConditioner;1",specification=spec_data_airconditioner)

modelRepository.parserDTDLModel(model_4)

#Configurando o instance manager

connection=Neo4jConnection("bolt://localhost:7687","neo4j","burks123")

digitalTwinInstanceManager=DigitalTwinsInstaceManagerNeo4j(connection)


# Criando as instâncias

house_1=digitalTwinInstanceManager.create_from_model(modelRepository.getDTDLModel("dtmi:housegen:House;1"))

room_1=digitalTwinInstanceManager.create_from_model(modelRepository.getDTDLModel("dtmi:housegen:Room;1"))

lightbulb_1=digitalTwinInstanceManager.create_from_model(modelRepository.getDTDLModel("dtmi:housegen:LightBulb;1"))

lightbulb_2=digitalTwinInstanceManager.create_from_model(modelRepository.getDTDLModel("dtmi:housegen:LightBulb;1"))

airconditioner_1=digitalTwinInstanceManager.create_from_model(modelRepository.getDTDLModel("dtmi:housegen:AirConditioner;1"))

#Criando os relacionamentos

digitalTwinInstanceManager.create_relationship(from_id=house_1.ID,target_id=room_1.ID,relationship_name="HAS_ROOM")

digitalTwinInstanceManager.create_relationship(from_id=room_1.ID,target_id=lightbulb_1.ID,relationship_name="HAS_LIGHTBULB")

digitalTwinInstanceManager.create_relationship(from_id=room_1.ID,target_id=lightbulb_2.ID,relationship_name="HAS_LIGHTBULB")

digitalTwinInstanceManager.create_relationship(from_id=room_1.ID,target_id=airconditioner_1.ID,relationship_name="HAS_AIRCONDITIONER")

print("Its All Done!!!")
