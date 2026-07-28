import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller_node')
        
        # สร้าง Publisher ส่งข้อมูลไปยัง /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # กำหนดตัวแปรนับเวลาและสถานะ
        self.timer_period = 0.1  # ทำงานทุกๆ 0.1 วินาที
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.ticks = 0  # ตัวนับรอบเวลา (10 ticks = 1 วินาที)

    def timer_callback(self):
        msg = Twist()
        self.ticks += 1

        # 1. ช่วง 0 - 3 วินาที (tick 1-30): เดินหน้า
        if self.ticks <= 30:
            msg.linear.x = 0.2
            msg.angular.z = 0.0
            self.get_logger().info('กำลังเดินหน้า...')

        # 2. ช่วง 3 - 6 วินาที (tick 31-60): ถอยหลัง
        elif self.ticks <= 60:
            msg.linear.x = -0.2
            msg.angular.z = 0.0
            self.get_logger().info('กำลังถอยหลัง...')

        # 3. ช่วง 6 - 8 วินาที (tick 61-80): หมุนเลี้ยวซ้ายอยู่กับที่
        elif self.ticks <= 80:
            msg.linear.x = 0.0
            msg.angular.z = 1.0   # ค่าเป็นบวก = เลี้ยวซ้าย
            self.get_logger().info('กำลังเลี้ยวซ้าย...')

        # 4. ช่วง 8 - 10 วินาที (tick 81-100): หมุนเลี้ยวขวาอยู่กับที่
        elif self.ticks <= 100:
            msg.linear.x = 0.0
            msg.angular.z = -1.0  # ค่าเป็นลบ = เลี้ยวขวา
            self.get_logger().info('กำลังเลี้ยวขวา...')

        # 5. หลังจาก 10 วินาทีขึ้นไป: สั่งหยุดหุ่นยนต์
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.get_logger().info('หุ่นยนต์หยุดทำงาน')

        # ส่งคำสั่งไปยังหุ่นยนต์
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        # เมื่อกด Ctrl+C ให้สั่งหยุดหุ่นยนต์ก่อนปิด
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()