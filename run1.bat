@echo off
REM 切换到虚拟环境目录
cd /d "I:\workspace\Sequoia\.venv\Scripts"

REM 激活虚拟环境
call activate

REM 切换到 Python 脚本所在目录
cd /d "I:\workspace\Sequoia\"

REM 执行 Python 脚本
python main.py

@echo off
REM 获取当前日期并格式化为 YYYY-MM-DD
REM 根据实际系统日期格式解析日期。如果系统是 "YYYY-MM-DD"，可以直接用。否则需要调整分隔符和顺序。

REM 使用 wmic 获取格式化日期（确保适配所有系统区域设置）
for /f %%A in ('wmic os get localdatetime ^| find "."') do set datetime=%%A

REM 提取年、月、日
set year=%datetime:~0,4%
set month=%datetime:~4,2%
set day=%datetime:~6,2%

REM 构建目标文件名
set "log_file=combinations_%year%-%month%-%day%.log"

REM 打开结果文件
if exist "%log_file%" (
    start notepad.exe "%log_file%"
) else (
    echo File "%log_file%" not found!
)

REM 退出虚拟环境
deactivate