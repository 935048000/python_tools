#coding=utf-8

import psycopg2

class pgsql:
    """
    PostgreSQL 连接类。
    """
    def pgconnect(slef,DATABASE,USER,PASSWD,IP,POER):
        global conn
        conn = psycopg2.connect (database=DATABASE, user=USER, password=PASSWD, host=IP, port=POER)
        return 0

    def exesql(self,SQL):
        cur = conn.cursor ()
        cur.execute (SQL)
        rows = cur.fetchall ()

        if len(rows)>1:
            I = "\n"
            for i in rows:
                I = I + "%s\n"%(str(i))
        else:
            I = str(rows)+"\n"
        return I+"\n\n"

    def close(self):
        conn.close ()
        return 0



if __name__ == '__main__':
    print ("local run ....")
    pgsql.pgconnect (DATABASE, USER, PASSWD, IP,POER)
    t = pgsql.exesql ("SELECT * FROM bank_balance_detail_cur")
    print t
    pgsql.close()


