from graphdb import GraphDB

graph = GraphDB("bolt://localhost:7687", "neo4j", "password")


@graph.addPerson
def node(id, inf):
    print('Added Node')
    return


@graph.addContact
def relation(id1, id2, time, dist):
    print('Added Relationship')
    return


node('1', 'no')
node('2', 'no')
relation('1', '2', 'time', 'distance')
