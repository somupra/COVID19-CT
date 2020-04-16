// Create people nodes 
LOAD CSV WITH HEADERS FROM "file:///people.csv" AS row
MERGE (p:people {`id`: row.`id`})
ON CREATE SET p.`infected` = row.`infected`;

// CREATE contact relationships 
LOAD CSV WITH HEADERS FROM "file:///contact.csv" AS row
MATCH (from:people {`id`: row.`id1`})
MATCH (to:people {`id`: row.`id2`})
MERGE (from)-[r:contact]->(to)
SET r += {`time` : row.`time`, `distance` : row.`distance`};
