#!/usr/bin/python3
import subprocess
from operator import itemgetter
from time import strftime
import threading
import re
import requests

hostname = "杭州办公室橙域备线路机器通知"

def send_webhook_alert(message):
    webhook_url = "https://oapi.dingtalk.com/robot/send?access_token=b0deef874b979eeb97d3e374e9c9867cb269d110427e9f590038bef0c4025eca"
    headers = {
        "Content-Type": "application/json"
    }
    payload = {
        "msgtype": "text",
        "text": {
            "content": message
        }
    }
    try:
        response = requests.post(webhook_url, json=payload, headers=headers)
        if response.status_code == 200:
            print("Webhook警报发送成功")
        else:
            print(f"无法发送Webhook警报，状态码: {response.status_code}")
    except Exception as e:
        print(f"发送Webhook警报时出错: {e}")

def ping_host(host):
    print(f"{strftime('%Y-%m-%d %H:%M:%S')} 正在Ping {host}:\n")
    result = []
    timeout_count = 0

    for i in range(10):
        try:
            output = subprocess.check_output(f"ping -c 1 {host}", shell=True, stderr=subprocess.STDOUT)
            lines = output.splitlines()
            line = lines[1].decode()  # 包含ping结果的行
            match = re.search(r'time=(\d+\.?\d*)', line)  # 在行中查找延迟信息
            if match:
                delay = float(match.group(1))
                result.append((i, delay))
                print(f"数据包 {i}，延迟 {delay} 毫秒\n")
            else:
                print(f"数据包 {i}，未找到延迟信息。\n")
        except subprocess.CalledProcessError as e:
            print(f"数据包 {i}，Ping失败。{e.output.decode()}")
            timeout_count += 1
        except Exception as e:
            print(f"Ping过程中出现意外错误: {e}")
            timeout_count += 1

    if timeout_count >= 5:
        send_webhook_alert(f"{hostname}:    {host}的Ping超时 {timeout_count} 次")

    result.sort(key=itemgetter(1), reverse=True)
    top3 = result[:3]

    with open("/opt/shell/ping.txt", "a") as f:
        f.write(f"{strftime('%Y-%m-%d %H:%M:%S')} 正在Ping {host}:\n")
        for i, delay in top3:
            f.write(f"数据包 {i}，延迟 {delay} 毫秒\n")
            if delay > 1000:
                send_webhook_alert(f"{hostname}:    检测到高延迟：{delay} 毫秒，主机：{host}")
        f.write("\n")

def ping_hosts(hosts):
    for host in hosts:
        ping_host(host)
hosts = [
    'api.chandler.bet',
    'api.mapbox.com',
    'www.baidu.com',
    '8.8.8.8'
]

if __name__ == "__main__":
    threading.Thread(target=ping_hosts, args=(hosts,)).start()
