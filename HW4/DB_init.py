"""初始化数据库，用于存储用户信息，包括用户ID、用户名、密码和好友ID"""
import sqlite3


dbConn=sqlite3.connect('userData.db')

CreateSql="""create table if not exists user(
        ID TEXT primary key,
        userName TEXT,
        password TEXT,
        friends_ID TEXT
        )"""
dbConn.execute(CreateSql)

InsertSql="""insert into user
        values(?,?,?,?)
        """
data=(0,'wxx','123456','[]')
dbConn.execute(InsertSql,data)

dbConn.commit()

dbConn.close()