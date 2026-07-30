import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class FullMissionController(Node):
    def __init__(self):
        super().__init__('full_mission_controller_node')
        
        # 1. Publisher สำหรับคุมการเคลื่อนที่ของล้อผ่าน /cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 2. Publisher สำหรับคุม Servo S2 ผ่าน /servo_s2
        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)
        
        # ตั้งค่าองศาเซอร์โว
        self.CLOSE_ANGLE = 0
        self.OPEN_ANGLE = 80
        
        self.ticks = 0
        # สร้าง Timer ทำงานทุกๆ 0.1 วินาที (10 ticks = 1 วินาที)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังเชื่อมต่อระบบ... เริ่มรันภารกิจเต็มรูปแบบ!')

    def timer_callback(self):
        move_msg = Twist()
        servo_msg = Int32()
        servo_msg.data = self.CLOSE_ANGLE  # ค่าเริ่มต้นเซอร์โวปิดอยู่ที่ 0 องศา
        
        self.ticks += 1

        # 0.0 - 1.0 วินาที (tick 1-10): หน่วงเวลาเริ่มต้นระบบ
        if self.ticks <= 10:
            pass

        # 1.0 - 4.0 วินาที (tick 11-40): 1. เดินหน้า 3 วินาที
        elif self.ticks <= 40:
            move_msg.linear.x = 0.2
            if self.ticks == 11:
                self.get_logger().info('1. เดินหน้า 3 วินาที')

        # 4.0 - 6.0 วินาที (tick 41-60): 2. เลี้ยวซ้าย 2 วินาที (ความเร็ว 1.0)
        elif self.ticks <= 60:
            move_msg.angular.z = 1.0
            if self.ticks == 41:
                self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที (ความเร็ว 1.0)')

        # 6.0 - 7.0 วินาที (tick 61-70): 3. เดินหน้า 1 วินาที
        elif self.ticks <= 70:
            move_msg.linear.x = 0.2
            if self.ticks == 61:
                self.get_logger().info('3. เดินหน้า 1 วินาที')

        # 7.0 - 8.0 วินาที (tick 71-80): 4. ปล่อยลูกบาศก์ (เปิด servo_s2 ไปที่ 80 องศา ค้างไว้ 1 วินาที)
        elif self.ticks <= 80:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 71:
                self.get_logger().info('4. ปล่อยลูกบาศก์! (เปิด servo_s2 ไปที่ 80 องศา)')

        # 8.0 - 9.0 วินาที (tick 81-90): 5. ถอยหลัง 1 วินาที (servo จะหมุนกลับมาที่ 0 องศาอัตโนมัติ)
        elif self.ticks <= 90:
            move_msg.linear.x = -0.2
            if self.ticks == 81:
                self.get_logger().info('5. ถอยหลัง 1 วินาที ( servo_s2 หมุนกลับมาที่ 0 องศา )')

        # 9.0 - 11.0 วินาที (tick 91-110): 6. เลี้ยว 2 วินาที (ความเร็ว 1.0)
        elif self.ticks <= 110:
            move_msg.angular.z = -1.0  # เลี้ยวขวา (หากต้องการเลี้ยวซ้ายเปลี่ยนเป็น 1.0)
            if self.ticks == 91:
                self.get_logger().info('6. เลี้ยว 2 วินาที (ความเร็ว 1.0)')

        # 11.0 - 14.0 วินาที (tick 111-140): 7. เดินตรง 3 วินาที
        elif self.ticks <= 140:
            move_msg.linear.x = 0.2
            if self.ticks == 111:
                self.get_logger().info('7. เดินตรง 3 วินาที')

        # หลังจาก 14.0 วินาทีขึ้นไป: หยุดหุ่นยนต์และจบโปรแกรม
        else:
            self.get_logger().info('เสร็จสิ้นภารกิจทั้งหมด! หยุดหุ่นยนต์และปิดโปรแกรม')
            raise SystemExit

        # ส่งสัญญาณควบคุมออกไปทั้งการเคลื่อนที่และเซอร์โว
        self.cmd_vel_pub.publish(move_msg)
        self.servo_pub.publish(servo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = FullMissionController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อสั่งจบโปรแกรม ให้ส่งคำสั่งหยุดหุ่นยนต์และรีเซ็ตเซอร์โวกลับที่ 0 ทันที
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