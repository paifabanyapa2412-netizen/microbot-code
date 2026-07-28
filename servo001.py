import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64  # ส่งองศาเซอร์โว (สามารถเปลี่ยนชนิดข้อมูลตามบอร์ดที่ใช้รับได้)

class CubeDropper(Node):
    def __init__(self):
        super().__init__('cube_dropper_node')
        
        # สร้าง Publisher ส่งองศาเซอร์โวไปยัง topic /servo_angle
        self.publisher_ = self.create_publisher(Float64, '/servo_angle', 10)
        
        # กำหนดองศาสำหรับการใช้งาน (ปรับเปลี่ยนตามองศาจริงของกลไกได้เลย)
        self.CLOSE_ANGLE = 0.0    # องศาตอนหนีบ/กั้นลูกบาศก์ไว้
        self.OPEN_ANGLE = 90.0   # องศาตอนเปิดปล่อยลูกบาศก์
        
        self.get_logger().info('Node ควบคุมการปล่อยลูกบาศก์พร้อมทำงาน')

    def release_cube(self):
        """ฟังก์ชันสั่งเปิดกลไกเพื่อปล่อยลูกบาศก์"""
        msg = Float64()
        msg.data = self.OPEN_ANGLE
        self.publisher_.publish(msg)
        self.get_logger().info(f'สั่งเปิดเซอร์โวไปที่ {self.OPEN_ANGLE} องศา เพื่อปล่อยลูกบาศก์')

    def reset_servo(self):
        """ฟังก์ชันสั่งปิดกลไกกลับเข้าที่เดิม"""
        msg = Float64()
        msg.data = self.CLOSE_ANGLE
        self.publisher_.publish(msg)
        self.get_logger().info(f'สั่งรีเซ็ตเซอร์โวกลับไปที่ {self.CLOSE_ANGLE} องศา')


def main(args=None):
    rclpy.init(args=args)
    node = CubeDropper()
    
    # ตัวอย่างการสั่งปล่อยลูกบาศก์ทันทีที่รัน Node
    node.release_cube()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # เมื่อกด Ctrl+C ให้สั่งรีเซ็ตองศากลับมาที่เดิม
        node.reset_servo()
        node.get_logger().info('หยุดการทำงาน และรีเซ็ตตำแหน่งเซอร์โวเรียบร้อย')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()