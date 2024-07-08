from neo4j import GraphDatabase

from .DigitalTwinsInstanceRepository import DigitalTwin,DigitalTwinInstanceManager

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def execute_write(self, query, parameters=None):
        with self._driver.session() as session:
            return session.write_transaction(lambda tx: tx.run(query, parameters).single())

    def execute_read(self, query, parameters=None):
        with self._driver.session() as session:
            return session.read_transaction(lambda tx: tx.run(query, parameters).single())

class DigitalTwinsInstaceManagerNeo4j(DigitalTwinInstanceManager):
    def __init__(self, db_connection):
        super().__init__(db_connection)
    def insert_digital_twin(self,digital_twin):
        query = """
        CREATE (dt:DigitalTwin {ID: $ID, ModelID: $ModelID})
        WITH dt
        UNWIND $attributes AS attr
        CREATE (dt)-[:HAS_ATTRIBUTE]->(a:Attribute {Type: attr.Type, Name: attr.Name,Schema: attr.Schema, Value: attr.Value})
        WITH a, attr
        UNWIND attr.Characteristics AS char
        CREATE (a)-[:HAS_CHARACTERISTIC]->(:Characteristic {Name: char})
        """
        parameters = {
            'ID': digital_twin.ID,
            'ModelID': digital_twin.ModelID,
            'attributes': digital_twin.attributes
        }
        self.connection.execute_write(query, parameters)
    def get_digital_twin(self,ID):
        query = """
        MATCH (dt:DigitalTwin {ID: $ID})
        OPTIONAL MATCH (dt)-[:HAS_ATTRIBUTE]->(attr:Attribute)
        OPTIONAL MATCH (attr)-[:HAS_CHARACTERISTIC]->(char:Characteristic)
        RETURN dt.ID AS ID, dt.ModelID AS ModelID, 
               collect(DISTINCT attr {Type: attr.Type, Name: attr.Name, Schema: attr.Schema, Value: attr.Value, Characteristics: collect(char.Name)}) AS attributes
        """
        parameters = {'ID': ID}
        result = self.connection.execute_read(query, parameters)
        if result:
            attributes = result['attributes']
            for attr in attributes:
                attr['Characteristics'] = attr.get('Characteristics', [])
            return DigitalTwin(ID=result['ID'], ModelID=result['ModelID'], attributes=attributes)
        return None
    def update_digital_twin(self,digital_twin):
        pass
    def delete_digital_twin(self,ID):
        pass
    def create_relationship(self,from_id,target_id,relationship_name):
        query = """
        MATCH (a:DigitalTwin {ID: $from_id}), (b:DigitalTwin {ID: $to_id})
        CREATE (a)-[r:%s]->(b)
        RETURN type(r)
        """ % relationship_name
        parameters = {'from_id': from_id, 'to_id': target_id}
        self.execute_write(query, parameters)
    def execute_query(self,query):
        pass