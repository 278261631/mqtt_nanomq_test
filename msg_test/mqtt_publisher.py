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
            if message_count % 10 == 0:
                random_msg  = '{"procver":"3.17.13","posErr":"2.161999999","cmosNum":"32","mjdrefi":"58849","dec":"8.704000000","mjdreff":"0.00080074074","reproc":"T","seqpnum":"0","versionNum":0,"origin":"NAOC","hr":"0.15","dateEnd":"2025-04-07T19:01:05.687","detnam":"CMOS32","netRate":"196.62","segNum":"53","timesys":"TT","paPnt":"0","softver":"Hea_15Aug2039_V6.22_epwxtdas_11Jul39_v3.4.0","clockapp":"F","checksum":"UANhX1MeU8MeU8Me","caldbver":"x20391113","delflag":0,"q1":"0.372559636","q2":"0.157583639","q3":"0.911895751","q4":"-0.069374710","targId":"01709134053","datasum":"0","var":"98.109999999","utcfinit":"0","timeunit":"s","ra":"181.040999999","obsId":"01709134053","alarmType":0,"dateObs":"2025-04-07T18:55:45.978","raPnt":"181.041","trigtime":"166215596.503","telescop":"EP","decPnt":"8.704000000000001","decObj":"8.704000000000001","x":"643.299999999","srcSignificance":"174.4","y":"696.399999999","raObj":"181.041","instrume":"WXT","object":"01709134053"}'

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