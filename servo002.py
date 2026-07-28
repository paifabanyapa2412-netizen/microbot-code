import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32  # เปลี่ยนเป็น Int32 ตามมาตรฐานบอร์ดหุ่นยนต์ส่วนใหญ่

class CubeDropper(Node):
    def __init__(self):
        super().__init__('cube_dropper_node')
        
        # 1. สร้าง Publisher (ลองเปลี่ยนชื่อ topic เป็น /servo หรือ /servo_angle ให้ตรงกับบอร์ด)
        self.publisher_ = self.create_publisher(Int32, '/servo', 10)
        
        # 2. กำหนดองศา (ตั้งเป็นจำนวนเต็ม Int32)
        self.CLOSE_ANGLE = 0    # องศาปิด/หนีบ
        self.OPEN_ANGLE = 90    # องศาเปิดปล่อย
        
        # 3. ให้ส่งสัญญาณซ้ำทุกๆ 0.1 วินาทีเพื่อป้องกันสัญญาณหลุด
        self.timer = self.create_timer(0.1, self.timer_callback)
        self.get_logger().info('กำลังสั่งเปิด servo ไปที่ 90 องศา...')

    def timer_callback(self):
        msg = Int32()
        msg.data = self.OPEN_ANGLE
        self.publisher_.publish(msg)

    def reset_servo(self):
        """ฟังก์ชันส่งคำสั่งปิด servo ก่อนปิดโปรแกรม"""
        msg = Int32()
        msg.data = self.CLOSE_ANGLE
        self.publisher_.publish(msg)
        self.get_logger().info('สั่งรีเซ็ต servo กลับไปที่ 0 องศา')

def main(args=None):
    rclpy.init(args=args)
    node = CubeDropper()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        # เมื่อกด Ctrl+C ให้รีเซ็ตตำแหน่ง servo กลับที่เดิม
        node.reset_servo()
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()