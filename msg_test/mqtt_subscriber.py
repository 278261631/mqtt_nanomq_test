import paho.mqtt.client as mqtt
import time

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
        # 订阅主题
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"📋 已订阅主题: {MQTT_TOPIC}")
    else:
        print(f"❌ 连接失败，错误代码: {rc}")

# 消息接收回调函数
def on_message(client, userdata, msg):
    print(f"📥 收到消息:")
    print(f"   主题: {msg.topic}")
    print(f"   内容: {msg.payload.decode()}")
    print(f"   QoS: {msg.qos}")
    print("-" * 50)

# 订阅者主函数
def mqtt_subscriber():
    print("🚀 MQTT订阅者启动")
    print(f"📡 连接到: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"👤 用户名: {MQTT_USERNAME}")
    print(f"📝 订阅主题: {MQTT_TOPIC}")
    print("=" * 50)
    
    # 创建MQTT客户端
    client = mqtt.Client()
    
    # 设置用户名和密码
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # 设置回调函数
    client.on_connect = on_connect
    client.on_message = on_message
    
    try:
        # 连接到MQTT服务器
        client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 开始循环，处理消息
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n⏸️ 用户中断，停止订阅")
    except Exception as e:
        print(f"❌ 发生错误: {e}")
    finally:
        # 断开连接
        client.disconnect()
        print("📴 已断开MQTT连接")

if __name__ == "__main__":
    mqtt_subscriber()