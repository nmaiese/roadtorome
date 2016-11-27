from neo4j.v1 import GraphDatabase, basic_auth


def openNeo4j():
    driver = GraphDatabase.driver("bolt://localhost", auth=basic_auth("neo4j", "r04dt0r0m3"), encrypted=True)
    return driver.session()



session = openNeo4j()

for a in graph_list:
    trim = ''.join(e for e in a['key'] if e.isalnum())
    session.run("CREATE ("+trim+":Article {title:'"+a['key'].replace("'", "")+"'})")

session.close()



