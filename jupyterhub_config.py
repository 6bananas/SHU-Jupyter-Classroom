from jupyterhub.auth import DummyAuthenticator # 登录认证方式
import os

def configure_nbgrader_volume(spawner):
    user = spawner.user
    # nbgrader 插件控制
    student_lab_src = "/export/jupyterhub/config/student_lab_config.json"
    admin_lab_src = "/export/jupyterhub/config/admin_lab_config.json"
    # 容器内的目标路径，这是 JupyterLab 读取前端配置的标准位置
    lab_target_path = "/etc/jupyter/labconfig/page_config.json"
    if user.admin:
        spawner.volumes[admin_lab_src] = lab_target_path
    else:
        spawner.volumes[student_lab_src] = lab_target_path
# 注册 hook 函数
c.Spawner.pre_spawn_hook = configure_nbgrader_volume

# 指定模板路径
c.JupyterHub.template_paths = [os.path.join(os.path.dirname(__file__), 'page_templates')]

# 使用 DummyAuthenticator 允许任意用户名+固定密码登录
# Dummy 方式仅测试用，最终要改为 OAuth/LDAP
c.JupyterHub.authenticator_class = DummyAuthenticator
c.DummyAuthenticator.password = '123456' # 固定密码
c.Authenticator.admin_users = {'root'} # 管理员用户
c.JupyterHub.admin_access = True # 允许管理员访问其他用户的服务器

# 空闲自动清理服务
# 自动关闭闲置的用户 Jupyter 服务器，释放系统资源
c.JupyterHub.services = [
    {
        'name': 'idle-culler',
        'command': ['python3', '-m', 'jupyterhub_idle_culler', '--timeout=3600'],
        'admin': True
    }
]

# 使用 DockerSpawner
c.JupyterHub.spawner_class = 'dockerspawner.DockerSpawner'
c.JupyterHub.hub_ip = '0.0.0.0' # 指定 JupyterHub 核心服务绑定的 IP 地址
c.JupyterHub.hub_connect_ip = 'jupyterhub' # 指定用户容器如何连接回 Hub 服务，主 Hub 启动用户容器后，用户容器需要回连主 Hub

# 使用什么 Docker 镜像启动用户容器
c.DockerSpawner.image = 'single_user'
# 挂载宿主机目录
c.DockerSpawner.volumes = {
    '/export/jupyterhub/data/{username}': '/home/jovyan',
    '/export/jupyterhub/exchange': '/tmp/exchange'
}

# 网络配置
c.DockerSpawner.network_name = 'jupyterhub' # 指定用户容器使用的 Docker 网络名

# 开启 CHOWN_HOME 功能
# 当容器以 root 启动时，它会递归修改 /home/jovyan 的所有者为 NB_UID (1000)
c.DockerSpawner.environment = {
    'CHOWN_HOME': 'yes',
    'CHOWN_HOME_OPTS': '-R',  # 递归修改
    'NB_UID': '1000',         # 明确指定目标用户 ID
    'NB_GID': '100',
}

# 告诉 Docker 必须以 Root 身份启动容器
# 只有 Root 才有权限执行 chown 操作
c.DockerSpawner.extra_create_kwargs = {'user': 'root'}