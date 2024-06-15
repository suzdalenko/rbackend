from django.db import connection
from myapp.myresponse import DiscoJsonResponse


class MyReports:
    
    def report_work(request, action_get):
        cursor = connection.cursor()
        
        sqlQuery = """SELECT visit, email, lang, city
                     FROM person
                     JOIN lastvisit ON person.id = lastvisit.user_id
                  """
        cursor.execute(sqlQuery)
        sqlQueyRes = cursor.fetchall()
        cursor.close()

        array_res = []

        for line in sqlQueyRes:
            array_res.append(str(line[0])+" "+str(line[1])+" "+str(line[2])+" "+str(line[3]))
           

        # print(sqlQueyRes)
        # print({action_get:array_res})

        return DiscoJsonResponse({action_get:array_res})