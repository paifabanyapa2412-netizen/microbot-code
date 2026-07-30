import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotSequenceController(Node):
    def __init__(self):
        super().__init__('robot_sequence_controller_node')
        
        # Publisher สำหรับส่งคำสั่งความเร็วไปยัง /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.ticks = 0
        # สร้าง Timer ทำงานทุกๆ 0.1 วินาที (10 ticks = 1 วินาที)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังเชื่อมต่อระบบ... เริ่มรันลำดับการทำงาน')

    def timer_callback(self):
        move_msg = Twist()
        self.ticks += 1

        # 0.0 - 1.0 วินาที (tick 1-10): หน่วงเวลาเริ่มต้นระบบ
        if self.ticks <= 10:
            pass

        # 1.0 - 4.0 วินาที (tick 11-40): 1. เดินหน้า 3 วินาที
        elif self.ticks <= 40:
            move_msg.linear.x = 0.2  # ความเร็วเดินหน้า
            if self.ticks == 11:
                self.get_logger().info('1. เดินหน้า 3 วินาที')

        # 4.0 - 6.0 วินาที (tick 41-60): 2. เลี้ยวซ้าย 2 วินาที (ความเร็ว 1.0)
        elif self.ticks <= 60:
            move_msg.angular.z = 1.0  # เลี้ยวซ้ายความเร็ว 1.0
            if self.ticks == 41:
                self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที (ความเร็ว 1.0)')

        # 6.0 - 7.0 วินาที (tick 61-70): 3. เดินหน้า 1 วินาที
        elif self.ticks <= 70:
            move_msg.linear.x = 0.2
            if self.ticks == 61:
                self.get_logger().info('3. เดินหน้า 1 วินาที')

        # 7.0 - 8.0 วินาที (tick 71-80): 4. หยุดรอ 1 วินาที
        elif self.ticks <= 80:
            # move_msg เป็น 0 ทั้งหมด (หยุดนิ่ง)
            if self.ticks == 71:
                self.get_logger().info('4. หยุดรอ 1 วินาที')

        # 8.0 - 9.0 วินาที (tick 81-90): 5. ถอยหลัง 1 วินาที
        elif self.ticks <= 90:
            move_msg.linear.x = -0.2  # ความเร็วถอยหลัง
            if self.ticks == 81:
                self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # 9.0 - 11.0 วินาที (tick 91-110): 6. เลี้ยว 2 วินาที (ความเร็ว 1.0)
        elif self.ticks <= 110:
            move_msg.angular.z = -1.0  # เลี้ยวขวาความเร็ว 1.0 (ถ้าต้องการเลี้ยวซ้ายให้เปลี่ยนเป็น 1.0)
            if self.ticks == 91:
                self.get_logger().info('6. เลี้ยว 2 วินาที (ความเร็ว 1.0)')

        # 11.0 - 14.0 วินาที (tick 111-140): 7. เดินตรง 3 วินาที
        elif self.ticks <= 140:
            move_msg.linear.x = 0.2
            if self.ticks == 111:
                self.get_logger().info('7. เดินตรง 3 วินาที')

        # หลังจาก 14.0 วินาทีขึ้นไป: หยุดหุ่นยนต์และจบโปรแกรม
        else:
            self.get_logger().info('ทำงานครบทุกขั้นตอน หยุดหุ่นยนต์และปิดโปรแกรม')
            raise SystemExit

        # ส่งสัญญาณควบคุมไปที่ล้อ
        self.publisher_.publish(move_msg)

def main(args=None):
    rclpy.init(args=args)
    node = RobotSequenceController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อจบโปรแกรมหรือกด Ctrl+C ให้ส่งคำสั่งหยุดหุ่นยนต์ทันที
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()