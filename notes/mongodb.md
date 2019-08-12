# mongodb

### 1.基本命令

- 查看当前数据库:`db`
- 产看所有数据库：`show dbs/ show databases`
- 切换数据库：`use <db_name>`
- 删除当前数据库：`db.dropDatabase()`
- 手动创建集合：`db.createCollection(collection_name)`
- 产看当前数据库所有集合:`show collections`
- 删除集合:`db.集合名.drop()`

### 2.数据类型

- 文档id：`Object ID`，用于唯一标识一条文档
> 文档_id可以自己设置，或者由MongoDB设置
- 字符串：`String`
- 布尔值：`Boolean`
- 整数:`Integer`
- 浮点型：`Double`
- 数组：`Arrays`
- 对象（文档）：`Object`
- 空值：`Null`
- 时间戳：`Timestamp`
- 时间/日期：`Data`

### 3.增删查改

- 插入：`db.集合名.insert(document)`

- 保存：`db.集合名.save(document)`,文档_id已经存在则修改，否则添加

- 查询：`db.集合名.find()`

- 更新：`db.集合名.update(<query>, <update>, {multi:<boolean>})`

  ~~~javascript
  db.stu.update({name:'hr'}, {name: 'mnc'}) //将name=‘hr’的文档替换成{name: 'mnc'}
  db.stu.update({name:'hr'}, {$set:{name: 'hys'}}) //将name=‘hr’的文档中'name'字段的值设为‘hys’
  db.stu.update({}, {$set:{gender:0}}, {multi:true}) // 将所有文档的gender设为0
  ~~~

- 删除：`db.集合名.remove(<query>, {justOne: <boolean>})`

### 4.查询

- basic

    - `find(<query>)`
    - `findOne(<query>)`
    - `查询结果集.pretty()`——将查询结果格式化

- 条件查询

    + 比较运算符

      * `$lt`——小于
      * `$gt`——大于
      * `$lte`——小于等于
      * `$gte`——大于等于
      * `$ne`——不等于
      * `db.stu.find({age:{$gte:18}})`——查询年纪大于等于18的学生

    + 逻辑运算

      * and:`db.stu.find({age:{$gt:18}, gender:true})`
      * or:`db.stu.find({$or:[{age:{$gt:18}}, {gender: true}]})`

    + 范围运算符

      * `$in`
      * `$nin`
      * `db.stu.find({age:{$in:[18,28]}})`——查询年纪是18，28的学生

    + 正则查询

      * `db.stu.find({name:/^黄/})`
      * `db.stu.find({name:{$regex:'^黄'}})`

    + 偏移

      * `db.stu.find().skip(5).limit(4)`
      + 自定义查询
      ~~~javascript
      db.stu.find({
          $where:function(){
              return this.age > 30
          }
      }) //查询年龄大于30的学生
      ~~~

    + 投影

      * `db.集合名.find(<query>, {字段名称：1|0})`，1表示显示，0不显示，`_id`默认是显示的

    + 排序

      * `db.stu.find().sort({字段名称:1|-1})`，1表示升序，-1表示降序

    + 排序

      * `db.集合名.find(<query>).count()`
      * `db.集合名.count(<query>)`

    + 去重

      * `db.集合名.distinct('去重字段'，<query>)`

### 5.管道

- `db.集合名.aggregate({管道:{表达式}})`

- 常用管道

  * `$group`:将集合中的文档分组
  * `$match`：过滤数据，输出符合条件的数据
  * `$project`：重整文档结构
  * `$sort`：排序
  * `$limit`：偏移
  * `$skip`：偏移
  * `$unwind`：拆分，解曲

- 常用表达式

  * `$sum`,`$sum:1`表示以一倍计数
  * `$avg`
  * `$min`
  * `$max`
  * `$push`
  * `$first`
  * `$last`

- 具体用法

  * `$group`

  ~~~javascript
  //根据性别对学生集合进行分组，输出{_id:'gender的值'，counter:'每组文档总数的一倍和'}
  db.stu.aggregate({
      $group:{
          _id:'$gender',
          counter:{$sum:1}
      }
  }) 
  //所有学生的总数，以及平均年龄
  db.stu.aggregate({
      $group:{
          _id:null,
          counter:{$sum:1},
          avgAge:{$avg:'$age'}
      }
  }) 
  //统计不同性别的学生姓名
  db.stu.aggregate({
      $group:{
          _id:'$gender',
          name:{$push:'$name'}
      }
  })
  //使用$$ROOT将文档内容加入结果集
  db.stu.aggregate({
      $group:{
          _id:'$gender',
          stus:{$push:'$$ROOT'}
      }
  })
  ~~~

- `$match`——用法和find相似

- `$project`——和投影相似

- `$unwind`

  ~~~javascript
  //统计处每种类型所有英雄的名字
  db.heros.aggregate(
      {$unwind:'$tags'},
      $group:{
          _id:'$tags',
          heros:{$push:'$c_name'}
      }
  )
  ~~~

### 6.索引

- 创建索引
  * `db.集合名.ensureIndex({'字段名':1|-1}, {'unique': <boolean>})`,1表示升序，-1表示降序，true表示唯一索引，false表示不是唯一索引
  * `db.集合名.getIndexes()`，查看所有索引
  * `db.集合名.dropIndex('索引名')`,删除索引

### 7.数据备份和恢复

- `mongodump -h dbhost -d dbname -o dbdirectory`
- `mongorestore -h dbhost -d dbname --dir dbdirectory`






