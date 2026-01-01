import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling
import os, sys
from random import random
import pandas as pd




mocking = os.getenv('MOCKING')
if not mocking:
    # Create a connection pool
    dbconfig = {
        "database": "academicworld",
        "user":     os.getenv('MYSQL_USER'),
        "password": os.getenv('MYSQL_PASSWORD'),
        "host":     "127.0.0.1"
    }

    if not dbconfig['user']:
        sys.exit('ERROR: invalid MYSQL_USER in environment')

    if not dbconfig['password']: del dbconfig['password']

    cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      **dbconfig)


def query(sql, params=None, commit=False):
    cnx = cnxpool.get_connection()
    #
    #  Use prepared statement!
    #
    cursor = cnx.cursor(prepared=True)
    cursor.execute(sql, params or ())
    result = cursor.fetchall()
    rowcount = cursor.rowcount
    if commit: cnx.commit()
    cursor.close()
    cnx.close()
    return result, rowcount


def table_exists(tname):
    sql = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = %s";
    results, rowcount = query(sql, (tname,) )
    count = results[0][0]
    return count > 0

def view_exists(vname):
    sql = "SELECT COUNT(*) FROM information_schema.views WHERE table_name = %s";
    results, rowcount = query(sql, (vname,) )
    count = results[0][0]
    return count > 0

def count_faculties():
    if mocking: return 100
    sql = "select count(*) from faculty";
    results, rowcount = query(sql)
    return (results[0])[0]

def count_universities():
    if mocking: return 200
    sql = "select count(*) from university";
    results, rowcount = query(sql)
    return (results[0])[0]

def count_keywords():
    if mocking: return 300
    sql = "select count(*) from keyword";
    results, rowcount = query(sql)
    return (results[0])[0]

def count_publications():
    if mocking: return 400
    sql = "select count(*) from publication";
    results, rowcount = query(sql)
    return (results[0])[0]

def count_publications_by_keyword(kw):
    if mocking: return [(2000+x, 100+x) for x in range(10)]
    sql = '''
    select p.year, count(*)
      from publication p
           join Publication_Keyword pk on p.id = pk.publication_id
           join keyword k on k.id = pk.keyword_id
     where k.name = %s
     group by p.year'''
    results, rowcount = query(sql, (kw,) )

    d = {}
    for r in results:
        y, n = r
        y = int(y)
        d[y] = n
        
    miny = d and min(d) or 0
    maxy = d and max(d) or 0
    return [(y, d.get(y, 0)) for y in range(miny, maxy+1)]
    
def top10_professor_by_krc(kw):
    if mocking: return [(chr(ord('a')+x)*5, 100-x) for x in range(10)]
    sql = '''
    select fname as name, sum(S*C) as KRC
    from (
       select f.name as fname, p.title,
             kw.name as kname, pk.score as S, p.num_citations as C
         from faculty f
              join faculty_publication fp on f.id = fp.faculty_id
              join publication p on p.id = fp.publication_id
              join Publication_Keyword pk on pk.publication_id = p.id
              join keyword kw on kw.id = pk.keyword_id
        where kw.name = %s) foo
    group by fname
    order by KRC desc
    limit 10'''
    
    results, rowcount = query(sql, (kw,) )
    return [(r[0], r[1]) for r in results]

def kw_search(kw):
    if mocking: return [f'paper{x}' for x in range(10)]
    sql = '''
    select kw.name as kname from keyword kw where kw.name like %s
    order by kw.name
    limit 40'''
    results, rowcount = query(sql, (f'%{kw}%',) )
    return [r[0] for r in results]


def create_reading_list_table():
    if mocking: return;
    if table_exists('reading_list'): return
    query('create table reading_list(item text, summary text, unique key (item(255)))')


def rlist_get():
    if mocking:
        data= [f'paper{x}' for x in range(50)]
        data = ['"A Relational Model of Data for Large Shared Data Banks." by Edgar F. Codd'] + data
        return data
    results, rowcount = query('select item from reading_list order by item')
    return [r[0] for r in results]

def rlist_del(item1, item2 = ''):
    if mocking: return
    sql = "delete from reading_list where item = %s or item = %s"
    query(sql, (item1, item2), True)

def rlist_add(item):
    if mocking: return
    if not item: return
    sql = "insert ignore into reading_list (item) values (%s)"
    results, rowcount = query(sql, (item,), True)

def rlist_summary_get(item):
    if mocking: return f"# Summary of {item}"
    sql = "select summary from reading_list where item = %s"
    results, rowcount = query(sql, (item,))
    return rowcount and results[0][0] or None

def rlist_summary_set(item, summary):
    if mocking: return
    sql = "update reading_list set summary = %s where item = %s"
    query(sql, (summary, item), True)

def create_top5kw_per_year():
    if mocking: return
    if table_exists('top5kwperyear'): return
    sql = '''
    create view rank_keyword as
    with base as (
        select k.name as keyword, p.year as year, count(*) as npub,
           ROW_NUMBER() over (PARTITION BY year order by count(*) desc) as rnk	
        from keyword k 
             join Publication_Keyword pk on k.id = pk.keyword_id 
             join publication p on p.id = pk.publication_id
	group by keyword, year
    )
    select *
    from base
    '''
    query(sql)
    
    sql = '''
    create table top5kwperyear as
    select * from rank_keyword where rnk <= 5
    '''
    query(sql)


def top5kw_per_year():
    if mocking:
        return [(2000+x, f'keyword{y}', int(1000*random()))
                for y in range(5) for x in range(20)]

    sql = 'select year, keyword, npub from top5kwperyear'
    results, rowcount = query(sql)
    return [(r[0], r[1], r[2]) for r in results]

def get_publication(title):
    sql = '''
    select distinct f.name, p.title
      from faculty f
           join faculty_publication fp on f.id = fp.faculty_id
           join publication p on p.id = fp.publication_id
    where p.title = %s
    order by f.name
    '''
    results, rowcount = query(sql, (title,) )
    authors = []
    title = None
    for r in results:
        authors += [r[0]]
        title = r[1]

    if not authors or not title:
        return None

    return f'"{title}" by {", ".join(authors)}'

def get_all_keywords():
    # Define SQL query to get all keywords
    sql = '''
    SELECT DISTINCT name
    FROM keyword
    '''
    
    # Execute the query
    results, rowcount = query(sql)
    
    # Return the keywords as a list
    return [r[0] for r in results]


def get_faculty_options(keyword):
    sql = '''
    SELECT DISTINCT f.name
    FROM faculty f
    JOIN faculty_publication fp ON f.id = fp.faculty_id
    JOIN publication p ON p.id = fp.publication_id
    JOIN Publication_Keyword pk ON pk.publication_id = p.id
    JOIN keyword kw ON kw.id = pk.keyword_id
    WHERE kw.name = %s
    '''
    
    results, rowcount = query(sql, (keyword,))
    return [r[0] for r in results]


def get_faculty_image_url(faculty_name):
    # SQL to get the image URL or base64 string from the database
    sql = '''
    SELECT image_url  # or base64_image
    FROM faculty
    WHERE name = %s
    '''
    
    results, rowcount = query(sql, (faculty_name,))
    
    if results:
        return results[0][0]  # Assuming the image URL is in the first column of the result
    return ''

def get_university_image_url(university_name):
    sql = '''
    SELECT photo_url
    FROM university
    WHERE name = %s
    LIMIT 1
    '''

    results, rowcount = query(sql, (university_name,))
    if rowcount == 0: return ''
    return results[0][0]

def get_faculty_details(selected_faculty):
    sql = '''
    SELECT f.name,
           f.position,
           f.phone,
           COALESCE(u.name, 'Unknown University') AS University,
           f.email,
           f.photo_url
    FROM faculty f
    LEFT JOIN university u ON f.university_id = u.id
    WHERE f.name = %s
    LIMIT 1
    '''
    results, rowcount = query(sql, (selected_faculty,) )
    if rowcount == 0: return None

    r = results[0]
    return {'FacultyName': r[0],
                'Position': r[1],
                'Phone': r[2],
                'University': r[3],
                'Email': r[4],
                'PictureURL': r[5]}

def get_top_papers_by_keyword_and_year(keyword, start_year, end_year):
    sql = '''
        SELECT p.title AS title, a.name AS author, u.name AS school, pk.score, p.year
        FROM publication p
        JOIN Publication_Keyword pk ON p.id = pk.publication_id
        JOIN keyword k ON pk.keyword_id = k.id
        JOIN faculty_publication fp ON p.id = fp.publication_id
        JOIN faculty a ON fp.faculty_id = a.id
        JOIN university u ON a.university_id = u.id
        WHERE k.name = %s
        AND CAST(p.year AS UNSIGNED) BETWEEN %s AND %s
        ORDER BY pk.score DESC
        LIMIT 15
    '''

    results, rowcount = query(sql, (keyword, start_year, end_year))
    return pd.DataFrame(results, columns=["title", "author", "school", "score", "year"])


###################################################
#  Create the dependency tables and views
create_reading_list_table()
create_top5kw_per_year()


if __name__ == "__main__":
    print(count_faculties())
    print(count_universities())
    print(count_keywords())
    print(count_publications())
    #print(count_publications_by_keyword('data mining'))
    print(top10_professor_by_krc('machine learning'))
    print(kw_search('data'))
