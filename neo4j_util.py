from neo4j import GraphDatabase
import os, sys


mocking = os.getenv('MOCKING')

if not mocking:
    uri = "neo4j://localhost:7687"
    user = os.getenv('NEO4J_USER')
    password = os.getenv('NEO4J_PASSWORD')
    database = "academicworld"

    if not user or not password:
        sys.exit('ERROR: invalid NEO4J_USER or NEO4J_PASSWORD in environment')

    driver = GraphDatabase.driver(uri, auth=(user,password))

def query(q):
    session = driver.session(database=database)
    result = []
    for r in session.run(q):
        result += [r]
    session.close()
    return result

# FACULTY-INTERESTED_IN->KEYWORD
# PUBLICATION-LABEL_BY->KEYWORD
# FACULTY-PUBLISH->PUBLICATION
# FACULTY-AFFLIATION_WITH->INSTITUTION


# KEYWORD(name)
# FACULTY(id,name,photoUrl,position)
# LABEL_BY(score)
# PUBLICATION(id, numCitations, title, venue)

def top10_university_by_krc(kw):
    if mocking: return [(chr(ord('a')+x)*5, 100-x) for x in range(10)]
    q=f"""
    match (i:INSTITUTE)<--(faculty:FACULTY)-->(p:PUBLICATION)-[ll:LABEL_BY]->(k:KEYWORD)
    where k.name = "{kw}"
    with i.name as university, sum(ll.score * p.numCitations) as sum_krc
    return university, sum_krc
    order by sum_krc desc
    limit 10
    """
    results = query(q)
    out = []
    for r in results:
        out += [(r['university'], r['sum_krc'])]
    return out

def top10_paper_by_krc(kw):
    if mocking: return [(chr(ord('a')+x)*5, 100-x) for x in range(10)]
    q=f"""
    match (p:PUBLICATION)-[ll:LABEL_BY]->(k:KEYWORD)
    where k.name = "{kw}"
    with p.title as title, sum(ll.score * p.numCitations) as sum_krc
    return title, sum_krc
    order by sum_krc desc
    limit 10
    """
    results = query(q)
    out = []
    for r in results:
        out += [(r['title'], r['sum_krc'])]
    return out


if __name__ == "__main__":
    print(top10_university_by_krc('machine learning'))
    
