import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurnController(Node):
    def __init__(self):
        super().__init__('turn_controller_node')
        
        # Publisher สำหรับสั่งงานล้อหุ่นยนต์ผ่าน /cmd_vel
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.ticks = 0
        # สร้าง Timer ให้ทำงานทุกๆ 0.1 วินาที (10 ticks = 1 วินาที)
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('เริ่มทำงาน: เตรียมทดสอบการเลี้ยวซ้าย-ขวา...')

    def timer_callback(self):
        move_msg = Twist()
        self.ticks += 1

        # 0.0 - 1.0 วินาที (tick 1-10): หน่วงเวลาให้ Publisher เชื่อมต่อสำเร็จ
        if self.ticks <= 10:
            pass

        # 1.0 - 3.0 วินาที (tick 11-30): เลี้ยวซ้าย 2 วินาที (ค่า angular.z เป็นบวก)
        elif self.ticks <= 30:
            move_msg.angular.z = 0.5  # ความเร็วในการหมุนซ้าย
            if self.ticks == 11:
                self.get_logger().info('<<< กำลังเลี้ยวซ้าย...')

        # 3.0 - 4.0 วินาที (tick 31-40): พักหยุดนิ่ง 1 วินาที
        elif self.ticks <= 40:
            move_msg.angular.z = 0.0
            if self.ticks == 31:
                self.get_logger().info('--- หยุดรอ 1 วินาที ---')

        # 4.0 - 6.0 วินาที (tick 41-60): เลี้ยวขวา 2 วินาที (ค่า angular.z เป็นลบ)
        elif self.ticks <= 60:
            move_msg.angular.z = -0.5 # ความเร็วในการหมุนขวา
            if self.ticks == 41:
                self.get_logger().info('>>> กำลังเลี้ยวขวา...')

        # จบการทำงาน หยุดหุ่นยนต์
        else:
            self.get_logger().info('ทดสอบเสร็จสิ้น หยุดหุ่นยนต์และปิดโปรแกรม')
            raise SystemExit

        # ส่งคำสั่งไปยังล้อหุ่นยนต์
        self.publisher_.publish(move_msg)

def main(args=None):
    rclpy.init(args=args)
    node = TurnController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อสั่งจบโปรแกรม ให้ส่งคำสั่งหยุดล้อเพื่อความปลอดภัย
        stop_msg = Twist()
        node.publisher_.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()