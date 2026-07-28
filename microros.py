import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class MoveForward(Node):
    def __init__(self):
        super().__init__('move_forward_node')
        # สร้าง Publisher ส่งข้อมูลไปยัง topic /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # ตั้งเวลาให้ฟังก์ชัน timer_callback ทำงานทุกๆ 0.1 วินาที
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังสั่งให้หุ่นยนต์เดินหน้า...')

    def timer_callback(self):
        msg = Twist()
        # กำหนดความเร็วแนวตรง (Linear X) = 0.2 เมตร/วินาที (ปรับเพิ่ม/ลดได้)
        msg.linear.x = 0.2
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        
        # ไม่ให้หมุนตัว (Angular Z = 0)
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = 0.0

        # ส่งคำสั่งไปยังหุ่นยนต์
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MoveForward()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # เมื่อกด Ctrl+C ให้ส่งคำสั่งหยุดหุ่นยนต์
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.get_logger().info('หยุดหุ่นยนต์เรียบร้อยแล้ว')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
    