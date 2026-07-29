import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class FullTaskController(Node):
    def __init__(self):
        super().__init__('full_task_controller_node')
        
        # 1. Publisher สำหรับคุมล้อหุ่นยนต์
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 2. Publisher สำหรับคุม Servo S2
        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)
        
        # ตั้งค่าองศาเซอร์โว
        self.CLOSE_ANGLE = 0
        self.OPEN_ANGLE = 80
        
        # ตัวแปรนับเวลา (ทุกๆ 0.1 วินาที)
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('เริ่มทำงานตามลำดับขั้นตอน...')

    def timer_callback(self):
        move_msg = Twist()
        servo_msg = Int32()
        servo_msg.data = self.CLOSE_ANGLE  # ค่าเริ่มต้นเซอร์โวปิดอยู่
        
        self.ticks += 1

        # 0.0 - 1.0 วินาที (tick 1-10): หน่วงเวลาเริ่มต้น
        if self.ticks <= 10:
            pass

        # 1.0 - 4.0 วินาที (tick 11-40): เดินหน้า 3 วินาที
        elif self.ticks <= 40:
            move_msg.linear.x = 0.2
            if self.ticks == 11:
                self.get_logger().info('1. เดินหน้า 3 วินาที')

        # 4.0 - 5.0 วินาที (tick 41-50): เลี้ยวซ้าย 1 วินาที (สมมติใช้เวลาหมุน 1 วินาที)
        elif self.ticks <= 50:
            move_msg.angular.z = 0.5
            if self.ticks == 41:
                self.get_logger().info('2. เลี้ยวซ้าย')

        # 5.0 - 6.0 วินาที (tick 51-60): เดินหน้า 1 วินาที
        elif self.ticks <= 60:
            move_msg.linear.x = 0.2
            if self.ticks == 51:
                self.get_logger().info('3. เดินหน้า 1 วินาที')

        # 6.0 - 7.0 วินาที (tick 61-70): ปล่อยลูกบาศก์ (เปิดไป 80 องศา ค้างไว้ 1 วินาที)
        elif self.ticks <= 65:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 61:
                self.get_logger().info('4. ปล่อยลูกบาศก์ (เปิด servo)')

        elif self.ticks <= 70:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 66:
                self.get_logger().info('4. ปล่อยลูกบาศก์ (ปิด servo)')        
                
        # 7.0 - 8.0 วินาที (tick 71-80): ถอยหลัง 1 วินาที (เซอร์โวจะกลับไปที่ 0 อัตโนมัติ)
        elif self.ticks <= 80:
            move_msg.linear.x = -0.2
            if self.ticks == 71:
                self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # 8.0 - 9.0 วินาที (tick 81-90): เลี้ยวขวา 1 วินาที
        elif self.ticks <= 90:
            move_msg.angular.z = -0.5
            if self.ticks == 81:
                self.get_logger().info('6. เลี้ยวขวา')

        # 9.0 - 10.0 วินาที (tick 91-100): ตรง 1 วินาที
        elif self.ticks <= 100:
            move_msg.linear.x = 0.2
            if self.ticks == 91:
                self.get_logger().info('7. เดินตรง 1 วินาที')

        # หลังจาก 10 วินาทีขึ้นไป: หยุดหุ่นยนต์และจบโปรแกรม
        else:
            self.get_logger().info('8. ทำงานครบทุกขั้นตอน หยุดหุ่นยนต์')
            raise SystemExit

        # ส่งสัญญาณออกไปทั้งล้อและเซอร์โว
        self.cmd_vel_pub.publish(move_msg)
        self.servo_pub.publish(servo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = FullTaskController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อจบโปรแกรม สั่งหยุดล้อและรีเซ็ตเซอร์โวกลับที่ 0
        stop_move = Twist()
        stop_servo = Int32()
        stop_servo.data = 0
        
        node.cmd_vel_pub.publish(stop_move)
        node.servo_pub.publish(stop_servo)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()