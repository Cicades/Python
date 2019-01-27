#! F:\\study\\python\\learning\\venv\\Scripts\\python.EXE

# 在linux中可以使用‘#！’——SheBang 来直接运行python脚本，而不用再指定python执行器
import cards_tools
while True:
    cards_tools.show_menu()
    action_str = input('请选择希望执行的操作：')
    if action_str in ['1', '2', '3']:
        print('-' * 50)
        if action_str == '1':
            # 新增名片
            print('您选择的操作是添加名片！')
            cards_tools.new_card()
        elif action_str == '2':
            # 显示所有名片
            cards_tools.show_all()
        else:
            # 搜索名片
            cards_tools.search()
    elif action_str == '0':
        print('欢迎再次使用名片管理系统!')
        break
    else:
        print('您的操作有误，请再次输入！')
