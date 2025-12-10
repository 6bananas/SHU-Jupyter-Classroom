import requests
import time
from urllib.parse import urlparse, parse_qs

# 本机
#API_TOKEN = "f8dc43ff65034adfab974ba610016720"
# 实验室
API_TOKEN = "f7bfb1a0069a443f9a250ea57282e8ac"
TARGET_USER = "root"
LINK_FILE = "link.txt"

def clean_target_path(path_str):
    """
    将绝对路径清洗为相对路径
    """
    if not path_str:
        return None
    # 移除 /home/jovyan/ 前缀
    cleaned = path_str.replace("/home/jovyan/", "")
    return cleaned

def run_pull():
    """
    直接访问 nbgitpuller 后端 api
    """
    headers = {
        "Authorization": f"token {API_TOKEN}",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) PythonAutoPull"
    }
    try:
        with open(LINK_FILE, "r", encoding="utf-8") as f:
            links = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"错误：找不到文件 {LINK_FILE}")
        return
    print(f"开始处理 {len(links)} 个任务...\n")
    for i, original_url in enumerate(links, 1):
        try:
            parsed = urlparse(original_url)
            query_params = parse_qs(parsed.query)
            params = {k: v[0] for k, v in query_params.items()}
            # 获取并清洗路径
            raw_path = params.get('targetPath', '') or params.get('targetpath', '')
            if raw_path:
                fixed_path = clean_target_path(raw_path)
                # 同时发送多种参数名，无论服务器想要驼峰还是全小写都发给它
                # 这样做是兼容 nbgitpuller 不同版本的后端 api 变化
                params['targetPath'] = fixed_path
                params['targetpath'] = fixed_path
                params['destination'] = fixed_path  # 备用兼容名
                
                print(f"[{i}/{len(links)}] 正在请求...")
                print(f"      -> 目标路径: {fixed_path}")
            else:
                print(f"[{i}/{len(links)}] 警告: 原链接未指定 targetPath")
            # 构建 API 地址
            api_url = f"http://{parsed.netloc}/user/{TARGET_USER}/git-pull/api"
            # 发送请求
            response = requests.get(api_url, headers=headers, params=params, stream=True, timeout=60)
            if response.status_code == 200:
                print("      连接成功，服务器日志:")
                print("      " + "-"*20)
                success_flag = False # 标记是否看到了正确的路径
                for line in response.iter_lines():
                    if line:
                        decoded_line = line.decode('utf-8').strip()
                        if "data:" in decoded_line: 
                            clean_log = decoded_line.replace("data:", "").strip()
                            if clean_log and "keep-alive" not in clean_log:
                                print(f"      [Server] {clean_log}")
                                # 检查日志里是否出现了我们想要的 source 目录
                                if fixed_path in clean_log:
                                    success_flag = True  
                print("      " + "-"*20)
                if success_flag:
                    print("      拉取成功！")
                else:
                    print("      警告：服务器日志显示的路径不包含 source 目录，请手动检查")
            elif response.status_code == 403:
                print("      权限拒绝，请检查 token 是否正确")
            else:
                print(f"      失败： {response.status_code}")
        except Exception as e:
            print(f"      异常: {e}")
        print("=" * 40)
        time.sleep(1)
    print("\n 处理完毕！")

if __name__ == "__main__":
    run_pull()