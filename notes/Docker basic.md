## Docker basic

### docker 三要素

- 镜像——对程序及其运行环境的封装（不包括kernel），即只读模板
- 容器——使用镜像模板创建的实例，即真实的应用程序
- 仓库——存储镜像的仓库

***

### docker架构

![](./images/docker-archite.png)

***

### docker特点

![](./images/docker-vs-vm.png)

***

### docker仓库镜像源配置

- 阿里云
- 网易云

***

### docker常用命令

- 常规命令
    + `docker version`——版本信息
    + `docker info`——本机`docker`信息
- 镜像命令
  + `docker images`——显示本机的镜像信息
  + `docker search`——从`docker hub`查询`docker`信息
  + `docker pull <imagename:tag=latest>`——从仓库拉取镜像
  + `docker rmi <imagename:tag=latest>`

- 容器命令
    + docker run  [options] <iamgename>

      ![](./images/docker-run.png)

      + `-it`——交互式启动容器
      + `-d`——后台运行容器，但容器会马上退出
      + `-p <host-port>:container-port`——指定容器运行时映射的端口
      + `-v <host-datavolume-path:container-datavolume-path>`——指定宿主机与docker之间映射容器数据卷

    + `docker ps` 查看`docker`正在运行的容器

    + `exit`或`ctrl p+q`——退出当前容器

      * `docker attach <id|name>`——重新进入容器
      * `docker exec -it <id|name> <shell directives...>`——以目标容器的身份执行shell命令

    + `docker start <container-name|id>`

    + `docker restart <container-name|id>`

    + `docker stop <name|id>`

    + `docker kill id|name`

    + `docker rm id|name`

    + `docker top <name|id>`——查看详细容器

    + `docker inspect <id|name>`——查看容器内的详细细节

    + `docker cp <id|name>:<filename> <host-filename>`

    + `docker commit`——提交容器副本使之成为新的镜像模板

***

### docker原理

- `docker`镜像底层
    + `UnionFS`（联合文件系统）
      * `bootfs`——docker镜像最底层，主要包含`bootloadr`(引导加载kernel)和`kernel`
      * `rootfs`——在`bootfs`之上，包含linux中标准目录和文件
- `docker`容器数据卷

  + 容器数据持久化以及容器间的数据共享

