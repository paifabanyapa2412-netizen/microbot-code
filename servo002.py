import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CubeDropper(Node):
    def __init__(self):
        super().__init__('cube_dropper_node')
        
        # Publisher ส่งข้อมูลไปยัง /servo_s1
        self.publisher_ = self.create_publisher(Int32, '/servo_s1', 10)
        
        self.CLOSE_ANGLE = 0    # องศาเดิม (ปิด/หนีบ)
        self.OPEN_ANGLE = 90    # องศาปล่อย (เปิด)
        
        # ตัวแปรนับเวลา ( timer ทำงานทุกๆ 0.1 วินาที -> 10 ticks = 1 วินาที )
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('เริ่มทำงาน: สั่งเปิด servo_s1 ไปที่ 90 องศา เป็นเวลา 3 วินาที...')

    def timer_callback(self):
        msg = Int32()
        self.ticks += 1

        # ช่วง 0 - 3 วินาทีแรก (tick 1 - 30): เปิดไปที่ 90 องศา
        if self.ticks <= 30:
            msg.data = self.OPEN_ANGLE
            self.publisher_.publish(msg)

        # หลังจาก 3 วินาทีขึ้นไป (tick > 30): หมุนกลับมาที่ 0 องศา
        elif self.ticks <= 60:  # ส่งย้ำคำสั่งกลับที่เดิมอีกประมาณ 3 วินาทีเพื่อให้แน่ใจว่าสนิท
            msg.data = self.CLOSE_ANGLE
            self.publisher_.publish(msg)
            if self.ticks == 31:
                self.get_logger().info('ครบ 3 วินาทีแล้ว! สั่ง servo_s1 หมุนกลับไปที่ 0 องศา')

        # เมื่อเสร็จสิ้นกระบวนการ ให้ปิด Node อัตโนมัติ
        else:
            self.get_logger().info('ทำงานเสร็จสิ้นเรียบร้อย ปิดโปรแกรม...')
            raise SystemExit  # สั่งจบการทำงานของโปรแกรมโดยสมบูรณ์

def main(args=None):
    rclpy.init(args=args)
    node = CubeDropper()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
        # เมื่อจบโปรแกรมหรือกด Ctrl+C ให้ส่งคำสั่งกลับที่เดิมย้ำอีกครั้งเพื่อความปลอดภัย
        stop_msg = Int32()
        stop_msg.data = 0
        node.publisher_.publish(stop_msg)
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()