# Processing and Visualistaion

Run: `./script.sh <param1> <param2> <param3>`  

`param1`: original file name  
`param2`: no. of users to process from the original file  
`param3`: no. of timestamps per user to process from the original file 

Example: `./script.sh e1.csv 10 20`will process first 10 users with first 20 timestamps each. 

This will generate two files ready to import to node4j:  
`people.csv` contains node data  
`contact.csv` contains relationship data

Use `import-graph.cypher` to import graph to node4j.

`geo.py` measures the distance between two location points.
