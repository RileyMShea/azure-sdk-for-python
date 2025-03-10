import os
from azure.cosmos import CosmosClient
from azure.cosmos.partition_key import PartitionKey


class CosmosDB:
    def __init__(self):
        URL = os.environ["COSMOS_ENDPOINT"]
        KEY = os.environ["COSMOS_KEY"]
        self.client = CosmosClient(URL, {"masterKey": KEY})
        self.dbName = "pySolarSystem"

    def CreateDatabase(self):
        print("Creating '{0}' database...".format(self.dbName))
        return self.client.create_database(self.dbName)

    def CreateContainer(self, db):
        collectionName = "Planets"
        print("Creating '{0}' collection...".format(collectionName))
        partition_key = PartitionKey(path="/id", kind="Hash")
        return db.create_container(id="Planets", partition_key=partition_key)

    def CreateDocuments(self, container):
        # Cosmos will look for an 'id' field in the items, if the 'id' is not specify Cosmos is going to assing a random key.
        planets = [
            {
                "id": "Earth",
                "HasRings": False,
                "Radius": 3959,
                "Moons": [{"Name": "Moon"}],
            },
            {
                "id": "Mars",
                "HasRings": False,
                "Radius": 2106,
                "Moons": [{"Name": "Phobos"}, {"Name": "Deimos"}],
            },
        ]

        print("Inserting items in the collection...")
        for planet in planets:
            container.create_item(planet)
            print("\t'{0}' created".format(planet["id"]))
        print("\tdone")

    def SimpleQuery(self, container):
        print("Quering the container...")
        items = list(
            container.query_items(
                query="SELECT c.id FROM c", enable_cross_partition_query=True
            )
        )
        print("\tdone: {0}".format(items))

    def DeleteDatabase(self):
        print("Cleaning up the resource...")
        self.client.delete_database(self.dbName)
        print("\tdone")

    def Run(self):
        print()
        print("------------------------")
        print("Cosmos DB")
        print("------------------------")
        print("1) Create a Database")
        print("2) Create a Container in the database")
        print("3) Insert Documents (items) into the Container")
        print("4) Delete Database (Clean up the resource)")
        print()

        # Ensure that the database does not exists
        try:
            self.DeleteDatabase()
        except:
            pass

        try:
            db = self.CreateDatabase()
            container = self.CreateContainer(db=db)
            self.CreateDocuments(container=container)
            self.SimpleQuery(container=container)
        finally:
            # if something goes wrong, the resource should be cleaned anyway
            self.DeleteDatabase()
