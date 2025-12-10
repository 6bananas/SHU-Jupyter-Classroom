# SHU-Jupyter-Classroom

上海大学人工智能教学实验平台，基于 JupyterHub + nbgitpuller + nbgrader，可实现教师发布实验、学生进入学习的多用户场景。

## 基本介绍

使用 [DockerSpawner](https://github.com/jupyterhub/dockerspawner) 方式支撑多用户场景，即教师、学生一起使用该平台。

首先使用 Docker 容器的方式运行 JupyterHub，容器使用自定义镜像构建。

对于每一个用户，创建其对应的 Docker 容器，该容器也使用自定义镜像构建。

## 声明

**该项目仅供学习参考！**

因为考虑到网上很难搜到部署这样的平台的教程，以及中途遇到的问题的解决方案。此处提供一个完整的可运行的流程，不针对详细部署内容进行过多解释。我相信正在部署的人通过简单阅读文字说明，更多通过阅读这些配置文件的内容就能理解或找到一些解决当下遇到的问题的思路。如有更多疑问，可在 Issue 中提问。有很多踩过的坑和解决方案都没有放上来，或许未来的解答能给你提供一些思路。

## 部署及使用

详见相关文档。

## License

[MIT](https://github.com/6bananas/SHU-Jupyter-Classroom/blob/main/LICENSE)

## 致谢

- [nbgitpuller](https://github.com/jupyterhub/nbgitpuller)
- [nbgrader](https://github.com/jupyter/nbgrader)

JupyterHub 集成 nbgitpuller 和 nbgrader，实现 Notebook 课程材料教师发布、学生学习的多用户场景