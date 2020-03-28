import pymysql
from utils.LogUtil import my_log


class Mysql:
    # 初始化数据，连接数据库，光标对象
    def __init__(self, host, user, password, database, charset="utf8", port=3306):
        self.log = my_log()
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
            )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    # 创建查询，执行方法
    def fetchone(self, sql):
        """
        单个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetchall(self, sql):
        """
        多个查询
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        """
        执行
        :param sql:
        :return:
        """
        try:
            if self.conn and self.cursor:
                self.cursor.execute(sql)
                self.conn.commit()
        except Exception as ex:
            self.conn.rollback()
            self.log.error("Mysql 执行失败")
            self.log.error(ex)
            return False
        return True

    # 关闭对象
    def __del__(self):
        # 关闭光标对象
        if self.cursor is not None:
            self.cursor.close()
        # 关闭连接对象
        if self.conn is not None:
            self.cursor.close()


if __name__ == '__main__':
    mysql = Mysql(host="rm-bp1fgfik7419ay382.mysql.rds.aliyuncs.com",
                  user="ccmall",
                  password="NtSH%(gc43p(9Smo",
                  database="ccm_xds", charset="utf8", port=3306)
    res = mysql.fetchone("select * from ccm_xbs.member where phone = '15573235704'")
    print(res)
