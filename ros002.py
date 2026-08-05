import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class FullMissionController(Node):
    def __init__(self):
        super().__init__('full_mission_controller_node')
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)
        
        self.CLOSE_ANGLE = 0
        self.OPEN_ANGLE = 80
        
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังเชื่อมต่อระบบ... เริ่มรันภารกิจ')

    def timer_callback(self):
        move_msg = Twist()
        servo_msg = Int32()
        servo_msg.data = self.CLOSE_ANGLE
        
        self.ticks += 1

        # 0.0 - 1.0 วินาที: หน่วงเวลาเริ่มต้น
        if self.ticks <= 10:
            pass

        # 1.0 - 2.0 วินาที: 0. เดินตรงออกมาจากจุดเริ่มต้น 1 วินาที
        elif self.ticks <= 20:
            move_msg.linear.x = 0.2
            if self.ticks == 11:
                self.get_logger().info('0. เดินตรงออกมาจากจุดเริ่มต้น 1 วินาที')

        # 2.0 - 4.0 วินาที: 1. เลี้ยวขวา 2 วินาที
        elif self.ticks <= 40:
            move_msg.angular.z = -1.0
            if self.ticks == 21:
                self.get_logger().info('1. เลี้ยวขวา 2 วินาที')

        # 4.0 - 7.0 วินาที: 2. เดินตรงไป 3 วินาที
        elif self.ticks <= 70:
            move_msg.linear.x = 0.2
            if self.ticks == 41:
                self.get_logger().info('2. เดินตรงไป 3 วินาที')

        # 7.0 - 8.0 วินาที: 3. ปล่อยลูกบาศก์ 1 วินาที
        elif self.ticks <= 80:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 71:
                self.get_logger().info('3. ปล่อยลูกบาศก์!')

        # 8.0 - 9.0 วินาที: 4. ถอยหลังกลับมา 1 วินาที
        elif self.ticks <= 90:
            move_msg.linear.x = -0.2
            if self.ticks == 81:
                self.get_logger().info('4. ถอยหลังกลับมา 1 วินาที')

        # 9.0 - 11.0 วินาที: 5. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 110:
            move_msg.angular.z = 1.0
            if self.ticks == 91:
                self.get_logger().info('5. เลี้ยวซ้าย 2 วินาที')

        # 11.0 - 14.0 วินาที: 6. เดินตรง 3 วินาที
        elif self.ticks <= 140:
            move_msg.linear.x = 0.2
            if self.ticks == 111:
                self.get_logger().info('6. เดินตรง 3 วินาที')

        # 14.0 - 16.0 วินาที: 7. เลี้ยวขวา 2 วินาที
        elif self.ticks <= 160:
            move_msg.angular.z = -1.0
            if self.ticks == 141:
                self.get_logger().info('7. เลี้ยวขวา 2 วินาที')

        # 16.0 - 19.0 วินาที: 8. เดินตรง 3 วินาที
        elif self.ticks <= 190:
            move_msg.linear.x = 0.2
            if self.ticks == 161:
                self.get_logger().info('8. เดินตรง 3 วินาที')

        # 19.0 - 21.0 วินาที: 9. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 210:
            move_msg.angular.z = 1.0
            if self.ticks == 191:
                self.get_logger().info('9. เลี้ยวซ้าย 2 วินาที')

        # 21.0 - 22.0 วินาที: สั่งหยุดหุ่นยนต์ย้ำ 1 วินาที
        elif self.ticks <= 220:
            move_msg.linear.x = 0.0
            move_msg.angular.z = 0.0
            if self.ticks == 211:
                self.get_logger().info('🛑 กำลังสั่งหยุดหุ่นยนต์...')

        # หลัง 22 วินาที: จบการทำงาน
        else:
            self.get_logger().info('เสร็จสิ้นภารกิจ! ปิดโปรแกรมเรียบร้อย')
            raise SystemExit

        # ส่งสัญญาณควบคุม
        self.cmd_vel_pub.publish(move_msg)
        self.servo_pub.publish(servo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = FullMissionController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อสั่งจบโปรแกรม ส่งคำสั่งหยุดความเร็วเป็น 0 ย้ำอีก 5 ครั้ง
        stop_move = Twist()
        stop_servo = Int32()
        stop_servo.data = 0
        
        for _ in range(5):
            node.cmd_vel_pub.publish(stop_move)
            node.servo_pub.publish(stop_servo)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
