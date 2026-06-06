import time

from maa.resource import Resource
from maa.controller import AdbController
from maa.tasker import Tasker
from maa.define import MaaAdbInputMethodEnum

def main():
    print(">>> 正在启动 MAA 引擎...")
    
    # 1. 实例化控制器：连接到你的 BlueStacks 模拟器
    # 蓝叠的端口通常是 5555，如果是其他数字请替换
    adb_path = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
    ctrl = AdbController(
        adb_path,
        "127.0.0.1:5555",
        input_methods=MaaAdbInputMethodEnum.AdbShell,
    )
    
    # 测试连接是否成功
    if not ctrl.post_connection().wait().succeeded:
        print("❌ 连接模拟器失败！请检查 BlueStacks 是否开启了 ADB 并且端口号正确。")
        return
    print("✅ 成功连接 BlueStacks 模拟器！")

    # 2. 实例化资源：加载资源包目录（内含 image/pipeline）
    res = Resource()
    if not res.post_bundle("./assets/resource").wait().succeeded:
        print("❌ 加载资源失败！请检查 assets 文件夹路径是否正确。")
        return
    print("✅ 成功加载图片和 JSON 资源！")

    # 3. 实例化任务执行器：绑定资源和控制器
    tasker = Tasker()
    tasker.bind(res, ctrl)

    print(">>> 开始执行任务...")
    
    # 任务名必须和 pipeline/task.json 里的入口名一致
    job = tasker.post_task("press_icon").wait()
    if job.succeeded:
        print(">>> 任务执行完毕：识别并执行成功。")
    else:
        print(f">>> 任务结束但未成功，status={job.status}, failed={job.failed}")

if __name__ == "__main__":
    main()