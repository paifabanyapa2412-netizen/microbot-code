import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class CubeDropper(Node):
    def __init__(self):
        super().__init__('cube_dropper_node')
        
        # แก้ไขชื่อ Topic เป็น /servo_s1 ให้ตรงกับที่บอร์ด Yahboom ใช้งาน
        self.publisher_ = self.create_publisher(Int32, '/servo_s1', 10)
        
        self.CLOSE_ANGLE = 0    # องศาปิด/หนีบ
        self.OPEN_ANGLE = 90    # องศาเปิดปล่อย
        
        # ส่งสัญญาณซ้ำทุกๆ 0.1 วินาที
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังสั่งเปิด servo_s1 ไปที่ 90 องศา...')

    def timer_callback(self):
        msg = Int32()
        msg.data = self.OPEN_ANGLE
        self.publisher_.publish(msg)

    def reset_servo(self):
        msg = Int32()
        msg.data = self.CLOSE_ANGLE
        self.publisher_.publish(msg)
        self.get_logger().info('สั่งรีเซ็ต servo_s1 กลับไปที่ 0 องศา')

def main(args=None):
    rclpy.init(args=args)
    node = CubeDropper()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.reset_servo()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()