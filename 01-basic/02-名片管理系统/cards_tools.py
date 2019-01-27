# 名片管理系统注释

# 名片字典
cards_list = []


def show_menu():

    """显示功能菜单"""
    print('*' * 50)
    print('欢迎使用名片管理系统！')
    print('')
    print('1. 新增名片')
    print('2. 显示全部')
    print('3. 搜索名片')
    print('')
    print('0. 退出系统')
    print('*' * 50)


def new_card():

    """新增名片"""
    print('-' * 50)
    name = input('请输入您的名字:')
    age = input('请输入您的年龄:')
    email = input('请输入您的邮箱:')
    phone = input('请输入您的电话:')
    cards_list.append({'name': name, 'age': age, 'email': email, 'phone': phone})
    print('添加成功！')


def show_all():

    """显示所有名片"""
    print('-' * 50)
    if len(cards_list) == 0:
        print('当前没有任何保存的名片，您可以选择添加！')
        return
    print('姓名', '年龄', '邮箱', '电话', sep='\t' * 2)
    print('=' * 50)
    for item in cards_list:
        print('%s\t\t%s\t\t%s\t\t%s\t\t' % tuple(item.values()))


def search():

    """搜索名片"""
    print('-' * 50)
    name = input('请输入需要搜索的姓名：')
    for item in cards_list:
        if item['name'] == name:
            print('查询结果为：')
            print('%s\t\t%s\t\t%s\t\t%s\t\t' % tuple(item.values()))
            print('=' * 50)
            print('您可以选择进行下一步操作：【1】修改 【2】删除 【0】返回上级菜单')
            next_operation = input('请选择您需要进行的下一步操作：')
            if next_operation == '1':
                # 修改名片
                item['name'] = edit_info(item['name'], '请输入姓名：')
                item['age'] = edit_info(item['age'], '请输入年龄：')
                item['email'] = edit_info(item['email'], '请输入邮箱：')
                item['phone'] = edit_info(item['phone'], '请输入电话：')
                print('修改成功！')
            elif next_operation == '2':
                # 删除名片
                del_info(item)
            else:
                pass
            break
    else:
        print('没有找到对应的名片，您可以进行添加！')


def del_info(item):

    """删除名片"""
    cards_list.remove(item)
    print('删除名片成功！')


def edit_info(old, mesg):

    """修改名片"""
    new_info = input(mesg)
    return new_info if len(new_info.strip()) > 0 else old
