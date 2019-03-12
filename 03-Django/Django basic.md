# Django basic

***

## 1. 常用命令

- 项目创建——`django-admin startproject <项目名>`
- 应用创建——`python manage.py startapp <应用名>`
- 开启服务器——`python manage.py runserver`
- 根据models生成迁移文件——`python manage.py makemigrations`
- 执行迁移文件——`python manage.py migrate`(生成数据表，表名为`<应用名>_<模型类名小写>`)
- 进入项目的shell环境——`python manage.py shell`
- 创建超级管理员——`python manage.py createsuperuser`

