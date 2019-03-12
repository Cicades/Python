from pymysql import *


class JD(object):

    def __init__(self):
        self.conn = Connect(host='localhost', port=3306, user='root', password='root', database='jing_dong', charset='utf8')
        self.cursor = self.conn.cursor()

    def __del__(self):
        self.conn.close()
        self.cursor.close()

    def execute_select(self, sql):
        """执行sql语句"""
        self.cursor.execute(sql)
        for item in self.cursor.fetchall():
            print(item)

    def get_goods(self):
        """获取商品信息"""
        self.execute_select('select * from goods;')

    def get_cate(self):
        """获取种类信息"""
        self.execute_select('select * from goods_cates;')

    def get_brand(self):
        """获取品牌信息"""
        self.execute_select('select * from goods_brands;')

    def execute_sql(self, cate_name):
        """执行增删改"""
        res = self.cursor.execute('insert into goods_cates (name) values (%s)', [cate_name])  # 防止sql注入,尽量避免自己拼接sql语句
        if res:
            print('执行成功!')
        self.conn.commit()  # 只有提交后,对数据库的操作才会真正生效
        # self.conn.rollback()  可以撤销之前对数据库的操作(尚未提交)
    
    @staticmethod
    def print_menu():
        print('-------JD--------')
        print('1.查询商品信息')
        print('2.查询种类信息')
        print('3.查询品牌信息')
        print('4.插入种类信息')
        print('退出(exit)')

    def run(self):
        """运行函数"""
        while True:
            self.print_menu()
            opt = input('请输入你要执行的操作:')
            if opt == '1':
                # 1. 查询商品信息
                self.get_goods()
            elif opt == '2':
            # 2. 查询种类信息
                self.get_cate()
            elif opt == '3':
            # 3. 查询品牌信息
                self.get_brand()
            elif opt == '4':
                # 4. 插入种类信息
                cate_name = input('请输入要插入的品牌:')
                self.execute_sql(cate_name)
            elif opt == 'exit':
                break
            else:
                print('您进行的操作有误!')


if __name__ == '__main__':
    jd = JD()
    jd.run()

