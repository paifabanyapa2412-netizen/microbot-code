import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CubeDropper(Node):
    def __init__(self):
        super().__init__('cube_dropper_node')
        
        # เปลี่ยนชื่อ Topic เป็น /servo_s2 สำหรับช่อง S2
        self.publisher_ = self.create_publisher(Int32, '/servo_s2', 10)
        
        self.CLOSE_ANGLE = 0    # องศาเดิม (ปิด/หนีบ)
        self.OPEN_ANGLE = 80    # องศาปล่อย (เปิด)
        
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังเชื่อมต่อระบบ (servo_s2)... กรุณารอสักครู่')

    def timer_callback(self):
        msg = Int32()
        self.ticks += 1

        # 0.0 - 1.0 วินาที (tick 1-10): หน่วงเวลาให้ Publisher เชื่อมต่อกับบอร์ดสำเร็จก่อน
        if self.ticks <= 10:
            pass 

        # 1.0 - 4.0 วินาที (tick 11-40): สั่งเปิดไปที่ 90 องศา (ค้างไว้ 3 วินาที)
        elif self.ticks <= 15:
            msg.data = self.OPEN_ANGLE
            self.publisher_.publish(msg)
            if self.ticks == 11:
                self.get_logger().info('สั่งเปิด servo_s2 ไปที่ 70 องศา...')

        # 4.0 - 6.0 วินาที (tick 41-60): สั่งหมุนกลับมาที่ 0 องศา
        elif self.ticks <= 20:
            msg.data = self.CLOSE_ANGLE
            self.publisher_.publish(msg)
            if self.ticks == 16:
                self.get_logger().info('ครบ 3 วินาทีแล้ว! สั่ง servo_s2 หมุนกลับไปที่ 0 องศา')

        # ปิด Node อัตโนมัติเมื่อเสร็จสิ้น
        else:
            self.get_logger().info('ทำงานเสร็จสิ้นเรียบร้อย ปิดโปรแกรม...')
            raise SystemExit

def main(args=None):
    rclpy.init(args=args)
    node = CubeDropper()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        stop_msg = Int32()
        stop_msg.data = 0
        node.publisher_.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()