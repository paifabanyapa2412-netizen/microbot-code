import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32
import time

def main():
    rclpy.init()
    node = Node('servo_zero_node')
    publisher = node.create_publisher(Int32, '/servo_s2', 10)
    
    msg = Int32()
    msg.data = 0  # ตั้งค่าเป็น 0 องศา
    
    # ส่งสัญญาณซ้ำ 5 ครั้งเพื่อให้แน่ใจว่ามอเตอร์รับคำสั่ง
    for _ in range(5):
        publisher.publish(msg)
        time.sleep(0.1)
        
    node.get_logger().info('ตั้งค่า servo_s2 ไปที่ 0 องศาเรียบร้อย!')
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()