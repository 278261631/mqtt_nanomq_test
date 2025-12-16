import paho.mqtt.client as mqtt
import time
import random
import threading

# MQTT服务器配置
MQTT_BROKER = "localhost"
MQTT_PORT = 11883
MQTT_USERNAME = "mqtt_user"
MQTT_PASSWORD = "mqtt_pass"
MQTT_TOPIC = "test/topic"

# 订阅者相关变量
subscriber_connected = False
message_received = 0

# 订阅者连接回调函数
def on_subscribe_connect(client, userdata, flags, rc):
    global subscriber_connected
    if rc == 0:
        print(f"✅ 订阅者成功连接到MQTT服务器: {MQTT_BROKER}:{MQTT_PORT}")
        client.subscribe(MQTT_TOPIC, qos=1)
        print(f"📋 订阅者已订阅主题: {MQTT_TOPIC}")
        subscriber_connected = True
    else:
        print(f"❌ 订阅者连接失败，错误代码: {rc}")

# 订阅者消息接收回调函数
def on_subscribe_message(client, userdata, msg):
    global message_received
    message_received += 1
    print(f"📥 订阅者收到消息 #{message_received}:")
    print(f"   主题: {msg.topic}")
    print(f"   内容: {msg.payload.decode()}")
    print(f"   QoS: {msg.qos}")
    print("-" * 60)

# 发布者连接回调函数
def on_publish_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"✅ 发布者成功连接到MQTT服务器: {MQTT_BROKER}:{MQTT_PORT}")
    else:
        print(f"❌ 发布者连接失败，错误代码: {rc}")

# 发布者发布回调函数
def on_publish_message(client, userdata, mid):
    print(f"📤 发布者消息发布成功，消息ID: {mid}")

# 订阅者线程函数
def subscriber_thread():
    # 创建订阅者MQTT客户端
    subscriber_client = mqtt.Client(client_id="subscriber-" + str(random.randint(1000, 9999)))
    
    # 设置用户名和密码
    subscriber_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # 设置回调函数
    subscriber_client.on_connect = on_subscribe_connect
    subscriber_client.on_message = on_subscribe_message
    
    try:
        # 连接到MQTT服务器
        subscriber_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 开始循环
        subscriber_client.loop_forever()
    except Exception as e:
        print(f"❌ 订阅者线程错误: {e}")

# 发布者函数
def publisher():
    # 创建发布者MQTT客户端
    publisher_client = mqtt.Client(client_id="publisher-" + str(random.randint(1000, 9999)))
    
    # 设置用户名和密码
    publisher_client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    
    # 设置回调函数
    publisher_client.on_connect = on_publish_connect
    publisher_client.on_publish = on_publish_message
    
    try:
        # 连接到MQTT服务器
        publisher_client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
        
        # 启动客户端循环
        publisher_client.loop_start()
        
        # 等待订阅者连接
        print("⏳ 等待订阅者连接...")
        timeout = 10
        while not subscriber_connected and timeout > 0:
            time.sleep(1)
            timeout -= 1
        
        if not subscriber_connected:
            print("⚠️  订阅者连接超时，继续发布消息")
        
        # 发布测试消息
        print("\n📢 开始发布测试消息...")
        print("💡 将连续发布5条消息，每条间隔2秒")
        print("-" * 60)
        
        for i in range(1, 6):
            # 生成测试消息内容
            test_msg = f"综合测试消息 #{i} - {time.strftime('%H:%M:%S')}"
            
            # 发布消息
            result = publisher_client.publish(MQTT_TOPIC, test_msg, qos=1)
            
            # 等待确认
            result.wait_for_publish()
            
            print(f"\n📝 发布者已发布消息 #{i}:")
            print(f"   主题: {MQTT_TOPIC}")
            print(f"   内容: {test_msg}")
            print(f"   QoS: 1")
            print("-" * 60)
            
            # 等待2秒
            time.sleep(2)
        
        print("\n🎉 测试完成!")
        print(f"📊 发布消息数: 5")
        print(f"📊 接收消息数: {message_received}")
        print(f"📊 消息成功率: {message_received}/5")
        
        if message_received == 5:
            print("✅ 所有消息均已成功接收!")
        else:
            print("⚠️  部分消息未接收，请检查网络或服务器状态")
        
        # 停止客户端循环
        publisher_client.loop_stop()
        
    except Exception as e:
        print(f"❌ 发布者错误: {e}")
        publisher_client.loop_stop()

# 主函数
def main():
    print("🚀 MQTT综合测试工具")
    print(f"📡 MQTT服务器: {MQTT_BROKER}:{MQTT_PORT}")
    print(f"👤 用户名: {MQTT_USERNAME}")
    print(f"📝 测试主题: {MQTT_TOPIC}")
    print("=" * 60)
    
    # 启动订阅者线程
    sub_thread = threading.Thread(target=subscriber_thread, daemon=True)
    sub_thread.start()
    
    try:
        # 启动发布者
        publisher()
        
    except KeyboardInterrupt:
        print("\n⏸️ 用户中断，测试结束")
    
    print("\n📴 测试工具已退出")

if __name__ == "__main__":
    main()