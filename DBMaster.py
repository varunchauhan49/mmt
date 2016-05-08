import MySQLdb
from DBConfig import mysql as cfg
from flask import current_app
import urlparse
import os

class DBMaster:
    connection = None
    cursor = None

    def __init__(self):
        self.getConnection()
        pass

    def getConnection(self):
        try:
            self.connection = MySQLdb.connect(host=cfg['host'],
                                              user=cfg['user'],
                                              passwd=cfg['passwd'],
                                              db=cfg['db'])
        except Exception as error:
            current_app.logger.error("DB Connection Error")
            current_app.logger.error(str(error.__class__) + ": " + error.message)
            raise Exception("We are experiencing some problems. Please try again after some time")
        self.connection.autocommit(True)
        self.cursor = self.connection.cursor(MySQLdb.cursors.DictCursor)
        return self.connection

    def queryDB(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def closeConnection(self):
        self.cursor.close()

    def autoComplete(self,inputJSON):
        search = inputJSON.get("search", "")

        query = """
            select * from
            (select code as label from mmt
            UNION
            select name as label from mmt
            UNION
            select country as label from mmt) abc
            where label like '%%%s%%'
            LIMIT 10;
            """
        query = query % (search)
        result = self.queryDB(query)
        return result

    def search(self,inputJSON):
        search = inputJSON.get("search", "")
        type = inputJSON.get("type", "")
        sortby = inputJSON.get("sortby", "")
        pageNo = inputJSON.get("page", "")

        if(pageNo):
            page = pageNo*10

        print 'called', search, type, sortby, page

        if (not type and not sortby and not page):
            print 1
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                        """
            query = query % (search, search, search)
        elif (not type and not page):
            print 2
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    sort by '%s'
                        """
            query = query % (search, search, search,sortby)
        elif (not type and not sortby):
            print 3
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    LIMIT 10 OFFSET %s;
                    """
            query = query % (search, search, search,page)
        elif (not page and not sortby):
            print 4
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    and type = '%s';
                        """
            query = query % (search, search, search,type)
        elif (not sortby):
            print 5
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    and type = '%s'
                    LIMIT 10 OFFSET %s;
                        """
            query = query % (search, search, search,type,page)
        elif (not page):
            print 6
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    and type = '%s'
                    sort by '%s'
                        """
            query = query % (search, search, search,type,sortby)
        elif (not type):
            print 7
            query = """select * from mmt
                    where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                    sort by '%s'
                    LIMIT 10 OFFSET %s;
                        """
            query = query % (search, search, search,sortby,page)
        else:
            print 8
            query = """select * from mmt
                where code like '%%%s%%' or name like '%%%s%%' or country like '%%%s%%'
                and type = '%s'
                sort by '%s'
                    """
            query = query % (search, search, search)
        result = self.queryDB(query)
        current_app.logger.info(query)
        return result