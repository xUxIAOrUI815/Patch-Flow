import docker
import os

client = docker.from_env()

def run_in_sandbox(local_dir, command):
    """
    在docker容器中执行command

    :param local_dir: 存放bug代码的目录
    :param command: 运行命令
    """
    container = client.containers.run(
        image="python:3.10-slim",
        command=["/bin/sh", "-c", command],
        volumes={local_dir: {'bind':'/app',"mode": "rw"}},
        working_dir="/app",
        detach=True
    )

    result=container.wait()
    logs=container.logs().decode()
    container.remove()
    return result['StatusCode'], logs


if __name__ == "__main__":
    LOCAL_DIR=r"D:\日常学习\Patch-Flow\tests"       # 此处填测试代码的路径
    COMMAND="pytest -v test_math.py"
    status_code, logs=run_in_sandbox(LOCAL_DIR, COMMAND)

    print("===执行结果===")
    print(f"状态码: {status_code}")
    print(f"日志: \n{logs}")