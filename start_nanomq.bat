@echo off
echo Starting NanoMQ MQTT Broker...
echo Configuration: Port 11883, Username: mqtt_user, Password: mqtt_pass
echo.

:: 检查端口是否被占用
netstat -an | findstr "11883" >nul
if %ERRORLEVEL% == 0 (
    echo Warning: Port 11883 is already in use.
    echo Trying to stop existing NanoMQ process...
    taskkill /F /IM nanomq.exe >nul 2>&1
    echo.
)

:: 启动NanoMQ服务器
D:\mqtt_nanomq\ser_0.19.5\bin\nanomq.exe start --conf D:\mqtt_run\nanomq_default_copy.conf

:: 检查启动结果
if %ERRORLEVEL% == 0 (
    echo.
    echo NanoMQ Broker started successfully!
    echo Listening on port 11883
    echo.
    echo To stop the broker, run: nanomq.exe stop
) else (
    echo.
    echo Failed to start NanoMQ Broker. Please check the logs.
)

echo.
echo Press any key to exit...
pause >nul