from cornice import Service
import psycopg2.extras

teste = Service(
    name='teste',
    path='/teste'
)

@teste.get()
def get_teste(request):
       

    conn = psycopg2.connect(
        host="172.16.0.253",
        port="5432",
        database="gtrp-teste",
        user="api",
        password="7a95a93a5e"
    )

    cur = conn.cursor(cursor_factory = psycopg2.extras.RealDictCursor)

    cur.execute("select now()")

    #results = json.dumps({"io": cur.fetchall()}, indent=4, sort_keys=True, default=str)

    #print(results)

    return {"io": cur.fetchall()[0]}