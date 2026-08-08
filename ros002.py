import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from std_msgs.msg import Int32
from apriltag_msgs.msg import AprilTagDetectionArray  # ปรับชื่อตาม package apriltag ที่ใช้
import math
import time

class MissionController(Node):
    def __init__(self):
        super().__init__('mission_controller')
        
        # 1. Publisher: สั่งความเร็วล้อหุ่นยนต์
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        # 2. Publisher: ส่งจำนวนกล่องที่ต้องปล่อยไปยัง micro-ROS (ควบคุม Servo)
        self.servo_pub = self.create_publisher(Int32, '/drop_cubes_cmd', 10)
        
        # 3. Subscriber: รับค่าพิกัดล้อ (Odometry)
        self.odom_sub = self.create_subscription(Odometry, '/odom', self.odom_callback, 10)
        
        # 4. Subscriber: รับค่า AprilTag จากกล้อง
        self.tag_sub = self.create_subscription(
            AprilTagDetectionArray, 
            '/tag_detections', 
            self.tag_callback, 
            10
        )
        
        # ตัวแปรเก็บพิกัดปัจจุบัน
        self.current_x = 0.0
        self.current_y = 0.0
        self.current_yaw = 0.0
        self.detected_tag_id = None

    def odom_callback(self, msg):
        # ดึงพิกัดตำแหน่ง X, Y
        self.current_x = msg.pose.pose.position.x
        self.current_y = msg.pose.pose.position.y
        
        # แปลงค่า Quaternion เป็นมุม Yaw (เรเดียน)
        q = msg.pose.pose.orientation
        siny_cosp = 2 * (q.w * q.z + q.x * q.y)
        cosy_cosp = 1 - 2 * (q.y * q.y + q.z * q.z)
        self.current_yaw = math.atan2(siny_cosp, cosy_cosp)

    def tag_callback(self, msg):
        # ดักจับ Tag ID แรกที่กล้องสแกนเจอ
        if len(msg.detections) > 0:
            self.detected_tag_id = msg.detections[0].id

    # -------------------------------------------------------------
    # ฟังก์ชันการเคลื่อนที่ด้วย Odom
    # -------------------------------------------------------------
    def move_forward(self, distance, speed=0.15):
        """ สั่งเดินหน้าเป็นระยะทางที่กำหนด (หน่วย: เมตร) """
        start_x = self.current_x
        start_y = self.current_y
        
        move_cmd = Twist()
        move_cmd.linear.x = speed
        
        self.get_logger().info(f'กำลังเดินหน้า {distance} เมตร...')
        
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)
            moved = math.sqrt((self.current_x - start_x)**2 + (self.current_y - start_y)**2)
            
            if moved >= distance:
                break
                
            self.cmd_pub.publish(move_cmd)
            
        self.stop_robot()
        self.get_logger().info('เดินหน้าถึงระยะแล้ว!')

    def turn_degrees(self, angle_deg, speed=0.3):
        """ สั่งเลี้ยวหมุนตัวตามมุมที่กำหนด (หน่วย: องศา, +ซ้าย/-ขวา) """
        target_rad = math.radians(angle_deg)
        start_yaw = self.current_yaw
        
        turn_cmd = Twist()
        turn_cmd.angular.z = speed if angle_deg > 0 else -speed
        
        self.get_logger().info(f'กำลังหมุนตัว {angle_deg} องศา...')
        
        while rclpy.ok():
            rclpy.spin_once(self, timeout_sec=0.05)
            diff = self.current_yaw - start_yaw
            
            # ปรับแต่งช่วงมุมให้อยู่ระหว่าง -pi ถึง pi
            diff = math.atan2(math.sin(diff), math.cos(diff))
            
            if abs(diff) >= abs(target_rad):
                break
                
            self.cmd_pub.publish(turn_cmd)
            
        self.stop_robot()
        self.get_logger().info('หมุนตัวเสร็จสิ้น!')

    def stop_robot(self):
        """ สั่งหยุดมอเตอร์ """
        stop_cmd = Twist()
        self.cmd_pub.publish(stop_cmd)
        time.sleep(0.5)

    # -------------------------------------------------------------
    # ฟังก์ชันทำภารกิจอ่าน Tag & ปล่อยกล่อง
    # -------------------------------------------------------------
    def scan_and_drop(self, timeout_sec=3.0):
        """ หยุดรอสแกน AprilTag และสั่งปล่อยกล่อง """
        self.get_logger().info('กำลังสแกน AprilTag...')
        self.detected_tag_id = None
        start_time = time.time()
        
        # วนลูปรออ่านค่า Tag ภายในเวลาที่กำหนด
        while time.sleep(0.1) or (time.time() - start_time < timeout_sec):
            rclpy.spin_once(self, timeout_sec=0.05)
            if self.detected_tag_id is not None:
                break

        if self.detected_tag_id is not None:
            tag_id = self.detected_tag_id
            self.get_logger().info(f'>>> เจอ AprilTag ID: {tag_id} <<<')
            
            # แปลงค่า Tag ID เป็นจำนวนลูกบาศก์ที่ต้องการปล่อย (ปรับแต่งตามกติกา)
            cube_map = {1: 1, 2: 2, 3: 3, 4: 4} # เช่น ID 1 = ปล่อย 1 ลูก
            cubes_to_drop = cube_map.get(tag_id, 1) # ถ้าไม่ตรงเงื่อนไข ปล่อย 1 ลูกเป็นค่าเริ่มต้น
            
            # ส่งคำสั่งไปที่ micro-ROS
            msg = Int32()
            msg.data = cubes_to_drop
            self.servo_pub.publish(msg)
            self.get_logger().info(f'สั่งปล่อยลูกบาศก์จำนวน {cubes_to_drop} ลูก')
            
            # หน่วงเวลารอให้ Servo ทำงานจนเสร็จ
            time.sleep(cubes_to_drop * 1.5) 
        else:
            self.get_logger().warn('ไม่พบ AprilTag ในจุดนี้ (ข้ามการปล่อยกล่อง)')

# -------------------------------------------------------------
# ลำดับการทำงานหลัก (Run Mission Loop)
# -------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    robot = MissionController()
    
    # หน่วงเวลา 2 วินาทีรอระบบพร้อม
    time.sleep(2.0)
    
    try:
        # === ตัวอย่าง ลำดับการวิ่งภารกิจ ===
        
        # 1. เดินหน้าไปจุดที่ 1 (ระยะ 1.0 เมตร)
        robot.move_forward(1.0)
        robot.scan_and_drop() # สแกน Tag + ปล่อยกล่อง
        
        # 2. เลี้ยวซ้าย 90 องศา
        robot.turn_degrees(90)
        
        # 3. เดินหน้าไปจุดที่ 2 (ระยะ 0.8 เมตร)
        robot.move_forward(0.8)
        robot.scan_and_drop() # สแกน Tag + ปล่อยกล่อง
        
        # 4. เลี้ยวซ้าย 90 องศา วิ่งกลับ
        robot.turn_degrees(90)
        robot.move_forward(1.0)
        
        robot.get_logger().info('จบการทำงานภารกิจทั้งหมด!')

    except KeyboardInterrupt:
        robot.stop_robot()

    robot.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()