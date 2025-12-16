import paho.mqtt.client as mqtt
import time
import random

# MQTT服务器配置
MQTT_BROKER = "localhost"
MQTT_PORT = 11883
MQTT_USERNAME = "mqtt_user"
MQTT_PASSWORD = "mqtt_pass"
MQTT_TOPIC = "test/topic"

# 连接回调函数
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ 成功连接到MQTT服务器: {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"❌ 连接失败，错误代码: {rc}")

# 发布回调函数
def on_publish(client, userdata, mid):
    print(f"📤 消息发布成功，消息ID: {mid}")

# 发布者主函数
def mqtt_publisher():
    print("🚀 MQTT发布者启动")
    print(f"📡 连接到: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"👤 用户名: {MQTT_USERNAME}")
    print(f"📝 发布主题: {MQTT_TOPIC}")
    print("=" * 50)
    
    # 创建MQTT客户端
    client = mqtt.Client()
    
    # 设置用户名和密码
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # 设置回调函数
    client.on_connect = on_connect
    client.on_publish = on_publish
    
    try:
        # 连接到MQTT服务器
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 启动客户端循环
        client.loop_start()
        
        # 发布测试消息
        print("📢 开始发布测试消息...")
        print("💡 输入'quit'退出，或按Enter键发布随机消息")
        print("-" * 50)
        
        message_count = 0
        while True:
            # 生成随机消息内容
            random_msg = f"测试消息 #{message_count} - 随机数: {random.randint(1, 100)}"
            
            # 发布消息
            result = client.publish(MQTT_TOPIC, random_msg, qos=1)
            
            # 等待确认
            result.wait_for_publish()
            
            print(f"\n📝 已发布:")
            print(f"   主题: {MQTT_TOPIC}")
            print(f"   内容: {random_msg}")
            print(f"   QoS: 1")
            print("-" * 50)
            
            message_count += 1
            
            # 等待3秒再发布下一条消息
            time.sleep(3)
            
    except KeyboardInterrupt:
        print("\n⏸️ 用户中断，停止发布")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        # 停止客户端循环并断开连接
        client.loop_stop()
        client.disconnect()
        print("📴 已断开MQTT连接")

if __name__ == "__main__":
    mqtt_publisher()