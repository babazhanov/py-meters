import pymssql
from django.shortcuts import render, redirect


"""
def find_key(dic, key):
    for k, v in dic.items():
        if k == key:
            return v
        elif isinstance(v, dict):
            for result in find_key(key, v):
                return result
"""

def index(request):

    connnection = pymssql.connect('aiis-2', 'reader', '555555', 'KMAESBYT', charset='cp1251')
    cursor = connnection.cursor()
    cursor.execute(
        """SELECT ID_Point, PointName, ID_Parent
          FROM Points
          ORDER BY ID_Point
          """)

    native_tree = {}
    tree = {}

    for row in cursor.fetchall():

        """
        sub_tree = find_key(tree, row[2])
        if sub_tree is None:
            tree[row[0]] = {"name": row[1], "childs": []}
        else:
            sub_tree["childs"].append({"name": row[1], "childs": []})
        """
        
        if row[2] == None:
            native_tree[row[0]] = { "name": row[1], "childs": [] }
        else:
            if native_tree.get(row[2]):
                native_tree[row[2]]["childs"].append(row[1])

    connnection.close()
    
    return render(request, "ensfera/index.html",
                              {"tree": native_tree,
                               "lst": tree,
                               })
