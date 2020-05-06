from neo4j import GraphDatabase


class GraphDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(
            uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()

    @staticmethod
    def _createPersonNode(tx, uid, infected):
        tx.run(
            "MERGE(p: people {`id`: $uid})"
            "ON CREATE SET p.`infected`=$infected",
            uid=uid, infected=infected)
        return

    @staticmethod
    def _createContactRelationship(tx, uid1, uid2, time, distance):
        tx.run(
            "MATCH (from: people {`id`: $uid1})"
            "MATCH (to: people {`id`: $uid2})"
            "CREATE (from)-[r:contact]->(to)"
            "SET r += {`time` : $time, `distance` : $distance};",
            uid1=uid1, uid2=uid2, time=time, distance=distance)
        return

    def addPerson(self, func):
        def inner(uid, infected):
            with self.driver.session() as session:
                session.write_transaction(
                    self._createPersonNode, uid, infected)
            return func(uid, infected)
        return inner

    def addContact(self, func):
        def inner(uid1, uid2, time, distance):
            with self.driver.session() as session:
                session.write_transaction(
                    self._createContactRelationship, uid1, uid2, time, distance)
            return func(uid1, uid2, time, distance)
        return inner
