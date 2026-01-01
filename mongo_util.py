from pymongo import MongoClient
import os, sys

mocking = os.getenv('MOCKING')

if not mocking:
    uri = "mongodb://localhost:27017/"
    database_name = "academicworld"
    client = MongoClient(uri)
    db = client[database_name]
    publications = db['publications']

def count_publications_by_keyword(kw):
    if mocking: return [('A', 100), ('B', 200), ('C', 300)]
    pipeline = [
        { '$match': { 'keywords.name': kw } },
        { '$project': { '_id': 0, 'year':'$year' }},
        { '$group': { '_id': '$year', 'count': {'$sum':1}}}
        ];
    results = publications.aggregate(pipeline)

    d = {}
    for r in results:
        y = r['_id']
        n = r['count']
        y = int(y)
        d[y] = n

    miny = d and min(d) or 0
    maxy = d and max(d) or 0
    return [(y, d.get(y, 0)) for y in range(miny, maxy+1)]


if __name__ == "__main__":
    print(count_publications_by_keyword('data mining'))

    
