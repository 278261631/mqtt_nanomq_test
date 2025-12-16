@echo off
echo Stopping NanoMQ MQTT Broker...
echo.

:: 停止NanoMQ服务器
D:\mqtt_nanomq\ser_0.19.5\bin\nanomq.exe stop

:: 检查停止结果
if %ERRORLEVEL% == 0 (
    echo NanoMQ Broker stopped successfully!
) else (
    echo Failed to stop NanoMQ Broker using command.
    echo Trying to force stop process...
    taskkill /F /IM nanomq.exe >nul 2>&1
    if %ERRORLEVEL% == 0 (
        echo NanoMQ process force stopped successfully!
    ) else (
        echo No NanoMQ process found or failed to stop.
    )
)

echo.
echo Press any key to exit...
pause >nul