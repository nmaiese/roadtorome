from neo4j.v1 import GraphDatabase, basic_auth
import re

def openNeo4j():
    '''Open connection to Neo4j DB'''
    driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "r04dt0r0m3"), encrypted=True)
    return driver.session()


def addObjectGraph(obj):
    '''for a single dict create the nodes for all element and the connections between them'''
    session = openNeo4j()
    source = ''.join(e for e in obj['key'] if e.isalnum())
    title = re.sub('[^a-zA-Z0-9 \n\.]', ' ', obj['key'])

    #Add node
    session.run("MERGE (`"+source+"`:Article {t itle:'"+title+"'});")
    for s in obj['target']:
        target = ''.join(e for e in s if e.isalnum())
        ttitle = re.sub('[^a-zA-Z0-9 \n\.]', '', s)
        session.run("MERGE (`" + target + "`:Article {title:'" + ttitle+ "'});")
        session.run("MATCH (a:Article),(b:Article) WHERE a.title = '"+title+"'"
                    "and b.title = '"+ttitle+"' MERGE (a)-[LINK:LINK]->(b);")

    session.close()


