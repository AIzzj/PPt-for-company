@echo off
echo 正在修复依赖问题...

:: 激活虚拟环境
call .venv\Scripts\activate

:: 卸载现有的numpy和opencv
echo 卸载现有的numpy和opencv...
pip uninstall -y numpy opencv-python

:: 安装兼容版本
echo 安装兼容版本的numpy和opencv...
pip install numpy==1.26.4
pip install opencv-python==4.8.1.78

echo 依赖修复完成！
echo 请重新启动后端服务: npm run backend 