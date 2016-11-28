from neo4j.v1 import GraphDatabase, basic_auth


def openNeo4j():
    '''Open connection to Neo4j DB'''
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "r04dt0r0m3"), encrypted=True)
    return driver.session()


def addObjectGraph(obj):
    '''for a single dict create the nodes for all element and the connections between them'''
    session = openNeo4j()
    source = ''.join(e for e in obj['key'] if e.isalnum())
    #Add node
    session.run("MERGE (`"+source+"`:Article {title:'"+obj['key'].replace("'", "")+"'});")
    for s in obj['target']:
        target = ''.join(e for e in s if e.isalnum())
        session.run("MERGE (`" + target + "`:Article {title:'" + s.replace("'", "") + "'});")
        session.run("MATCH (a:Article),(b:Article) WHERE a.title = '"+obj['key'].replace("'", "")+"'"
                    "and b.title = '"+s.replace("'","")+"' MERGE (a)-[LINK:LINK]->(b);")
    session.close()


