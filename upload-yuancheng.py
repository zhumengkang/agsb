#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import time
import threading
import signal
from pathlib import Path
import requests
from datetime import datetime

# 配置
TMATE_URL = "https://github.com/zhumengkang/agsb/raw/main/tmate"
UPLOAD_API = "https://file.zmkk.fun/api/upload"
USER_HOME = Path.home()
SSH_INFO_FILE = "ssh.txt"  # 可以自定义文件名

class TmateManager:
    def __init__(self):
        self.tmate_path = USER_HOME / "tmate"
        self.ssh_info_path = USER_HOME / SSH_INFO_FILE
        self.tmate_process = None
        self.session_info = {}
        
    def download_tmate(self):
        """下载tmate文件到用户目录"""
        print("正在下载tmate...")
        try:
            response = requests.get(TMATE_URL, stream=True)
            response.raise_for_status()
            
            with open(self.tmate_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            # 给tmate添加执行权限
            os.chmod(self.tmate_path, 0o755)
            print(f"✓ tmate已下载到: {self.tmate_path}")
            print(f"✓ 已添加执行权限 (chmod 755)")
            
            # 验证文件是否可执行
            if os.access(self.tmate_path, os.X_OK):
                print("✓ 执行权限验证成功")
            else:
                print("✗ 执行权限验证失败")
                return False
            
            return True
            
        except Exception as e:
            print(f"✗ 下载tmate失败: {e}")
            return False
    
    def start_tmate(self):
        """启动tmate并获取会话信息"""
        print("正在启动tmate...")
        try:
            # 启动tmate进程 - 分离模式，后台运行
            self.tmate_process = subprocess.Popen(
                [str(self.tmate_path), "-S", "/tmp/tmate.sock", "new-session", "-d"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True  # 创建新进程组，脱离父进程
            )
            
            # 等待tmate启动
            time.sleep(5)
            
            # 获取会话信息
            self.get_session_info()
            
            # 验证tmate是否在运行
            try:
                result = subprocess.run(
                    [str(self.tmate_path), "-S", "/tmp/tmate.sock", "list-sessions"],
                    capture_output=True, text=True, timeout=5
                )
                if result.returncode == 0:
                    print("✓ Tmate后台进程验证成功")
                    return True
                else:
                    print("✗ Tmate后台进程验证失败")
                    return False
            except Exception as e:
                print(f"✗ 验证tmate进程失败: {e}")
                return False
            
        except Exception as e:
            print(f"✗ 启动tmate失败: {e}")
            return False
    
    def get_session_info(self):
        """获取tmate会话信息"""
        try:
            # 获取只读web会话
            result = subprocess.run(
                [str(self.tmate_path), "-S", "/tmp/tmate.sock", "display", "-p", "#{tmate_web_ro}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.session_info['web_ro'] = result.stdout.strip()
            
            # 获取只读SSH会话
            result = subprocess.run(
                [str(self.tmate_path), "-S", "/tmp/tmate.sock", "display", "-p", "#{tmate_ssh_ro}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.session_info['ssh_ro'] = result.stdout.strip()
            
            # 获取可写web会话
            result = subprocess.run(
                [str(self.tmate_path), "-S", "/tmp/tmate.sock", "display", "-p", "#{tmate_web}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.session_info['web_rw'] = result.stdout.strip()
            
            # 获取可写SSH会话
            result = subprocess.run(
                [str(self.tmate_path), "-S", "/tmp/tmate.sock", "display", "-p", "#{tmate_ssh}"],
                capture_output=True, text=True, timeout=10
            )
            if result.returncode == 0:
                self.session_info['ssh_rw'] = result.stdout.strip()
                
            # 显示会话信息
            if self.session_info:
                print("\n✓ Tmate会话已创建:")
                if 'web_ro' in self.session_info:
                    print(f"  只读Web会话: {self.session_info['web_ro']}")
                if 'ssh_ro' in self.session_info:
                    print(f"  只读SSH会话: {self.session_info['ssh_ro']}")
                if 'web_rw' in self.session_info:
                    print(f"  可写Web会话: {self.session_info['web_rw']}")
                if 'ssh_rw' in self.session_info:
                    print(f"  可写SSH会话: {self.session_info['ssh_rw']}")
            else:
                print("✗ 未能获取到会话信息")
                
        except Exception as e:
            print(f"✗ 获取会话信息失败: {e}")
    
    def save_ssh_info(self):
        """保存SSH信息到文件"""
        try:
            content = f"""Tmate SSH 会话信息
创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            if 'web_ro' in self.session_info:
                content += f"web session read only: {self.session_info['web_ro']}\n"
            if 'ssh_ro' in self.session_info:
                content += f"ssh session read only: {self.session_info['ssh_ro']}\n"
            if 'web_rw' in self.session_info:
                content += f"web session: {self.session_info['web_rw']}\n"
            if 'ssh_rw' in self.session_info:
                content += f"ssh session: {self.session_info['ssh_rw']}\n"
            
            with open(self.ssh_info_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✓ SSH信息已保存到: {self.ssh_info_path}")
            return True
            
        except Exception as e:
            print(f"✗ 保存SSH信息失败: {e}")
            return False
    
    def upload_to_api(self, user_name="testtmate"):
        """上传SSH信息文件到API"""
        try:
            if not self.ssh_info_path.exists():
                print("✗ SSH信息文件不存在")
                return False
            
            print("正在上传SSH信息到API...")
            
            # 读取文件内容
            with open(self.ssh_info_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 创建临时文件用于上传
            file_name = f"{user_name}.txt"
            temp_file = USER_HOME / file_name
            
            with open(temp_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # 上传文件
            with open(temp_file, 'rb') as f:
                files = {'file': (file_name, f)}
                response = requests.post(UPLOAD_API, files=files)
            
            # 删除临时文件
            if temp_file.exists():
                temp_file.unlink()
            
            if response.status_code == 200:
                try:
                    result = response.json()
                    if result.get('success') or result.get('url'):
                        url = result.get('url', '')
                        print(f"✓ 文件上传成功!")
                        print(f"  上传URL: {url}")
                        
                        # 保存URL到文件
                        url_file = USER_HOME / "ssh_upload_url.txt"
                        with open(url_file, 'w') as f:
                            f.write(url)
                        print(f"  URL已保存到: {url_file}")
                        return True
                    else:
                        print(f"✗ API返回错误: {result}")
                        return False
                except Exception as e:
                    print(f"✗ 解析API响应失败: {e}")
                    return False
            else:
                print(f"✗ 上传失败，状态码: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ 上传到API失败: {e}")
            return False
    
    def cleanup(self):
        """清理资源 - 不终止tmate会话"""
        # 注意：这里不清理tmate进程，让它在后台继续运行
        print("✓ Python脚本资源清理完成（tmate会话保持运行）")

def signal_handler(signum, frame):
    """信号处理器"""
    print("\n收到退出信号，正在清理...")
    if hasattr(signal_handler, 'manager'):
        signal_handler.manager.cleanup()
    sys.exit(0)

def main():
    manager = TmateManager()
    
    # 只在主线程中注册信号处理器
    try:
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal_handler.manager = manager  # 保存引用用于信号处理
    except ValueError:
        # 如果不在主线程中（如Streamlit环境），跳过信号处理器注册
        print("⚠ 检测到非主线程环境，跳过信号处理器注册")
    
    try:
        print("=== Tmate SSH 会话管理器 ===")
        
        # 检查并安装依赖
        try:
            import requests
        except ImportError:
            print("检测到未安装requests库，正在安装...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
            import requests
            print("✓ requests库安装成功")
        
        # 1. 下载tmate
        if not manager.download_tmate():
            return False
        
        # 2. 启动tmate
        if not manager.start_tmate():
            return False
        
        # 3. 保存SSH信息
        if not manager.save_ssh_info():
            return False
        
        # 4. 上传到API
        user_name = "testtmate"  # 默认文件名，无需交互
        
        if not manager.upload_to_api(user_name):
            return False
        
        print("\n=== 所有操作完成 ===")
        print("✓ Tmate会话已在后台运行")
        print(f"✓ 会话信息已保存到: {manager.ssh_info_path}")
        print(f"✓ 上传URL已保存到: {USER_HOME}/ssh_upload_url.txt")
        print("\n🎉 脚本执行完成！")
        print("📍 Tmate会话将继续在后台运行，可以直接使用SSH连接")
        print("📍 如需停止tmate会话，请执行: pkill -f tmate")
        print("📍 查看tmate进程状态: ps aux | grep tmate")
        
        return True
            
    except Exception as e:
        print(f"✗ 程序执行出错: {e}")
        return False
    finally:
        manager.cleanup()
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
