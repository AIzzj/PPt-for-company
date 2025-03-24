@echo off
echo 正在设置AI驱动的企业PPT模板系统环境...

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python未安装，请安装Python 3.9或更高版本
    exit /b 1
)

:: 创建虚拟环境
if not exist .venv (
    echo 创建虚拟环境...
    python -m venv .venv
)

:: 激活虚拟环境并安装依赖
echo 安装依赖...
call .venv\Scripts\activate
pip install -r requirements.txt

:: 创建必要的目录
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist templates mkdir templates

echo 环境设置完成！
echo 启动系统请运行: npm run combined 