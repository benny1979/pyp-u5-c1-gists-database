from .models import Gist

def search_gists(db_connection, **kwargs):
    conn = db_connection
    cursor = conn.cursor()
    query = build_query(**kwargs)
    results = cursor.execute(query, kwargs)
    for result in results: 
        yield Gist(result) 

def build_query(**kwargs):
    query = "SELECT * FROM gists"
    if not kwargs:
        return """{};""".format(query)
    query_terms = []
    operator_dict = {'gt': '>', 'gte': '>=', 'lt':'<', 'lte': '<='}
    for kwarg_k, kwarg_v in kwargs.items():
        if '__' in kwarg_k:
            search_term, operator = kwarg_k.split('__')
            query_terms.append('datetime({}) {} datetime(\'{}\')'.format(search_term, operator_dict[operator], kwarg_v))
        else:
            query_terms.append('{} = :{}'.format(kwarg_k, kwarg_k))
    if len(query_terms) > 1:
        query_terms = ' AND '.join(query_terms)
    else:
        query_terms  = query_terms[0]
    return """{} WHERE ({});""".format(query, query_terms)
