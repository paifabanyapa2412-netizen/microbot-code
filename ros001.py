#!/usr/bin/env python3
# encoding: utf-8

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32, String
import time

class FullMissionController(Node):
    def __init__(self):
        super().__init__('full_mission_controller_node')
        
        # Publisher ควบคุมล้อและเซอร์โว
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)
        
        # Subscriber รับค่า AprilTag ID จากกล้อง (Topic: /tag_id)
        self.tag_sub = self.create_subscription(
            String,
            '/tag_id',
            self.tag_callback,
            10
        )
        
        # ตั้งค่ามุมเซอร์โว
        self.CLOSE_ANGLE = 0
        self.OPEN_ANGLE = 80
        
        # ตัวแปรเก็บค่า AprilTag ที่สแกนได้
        self.latest_tag_id = None
        self.is_dropping = False  # สถานะกำลังปล่อยลูกบาศก์
        
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback) # 1 tick = 0.1 วินาที
        self.get_logger().info('กำลังเชื่อมต่อระบบ... เริ่มรันภารกิจสแกน AprilTag')

    def tag_callback(self, msg):
        """ อัปเดตค่า AprilTag ล่าสุดที่กล้องมองเห็น """
        if msg.data:
            try:
                self.latest_tag_id = int(msg.data)
            except ValueError:
                pass

    def drop_cubes_by_tag(self):
        """ ฟังก์ชันหยุดหุ่นยนต์แล้วปล่อยลูกบาศก์ตามจำนวนที่อ่านได้จาก AprilTag (0-4) """
        self.is_dropping = True
        
        # สั่งหยุดหุ่นยนต์
        stop_msg = Twist()
        self.cmd_vel_pub.publish(stop_msg)
        
        self.get_logger().info('🔍 กำลังตรวจสอบค่า AprilTag บริเวณทางเข้า...')
        time.sleep(1.0) # รอสแกน
        
        tag_val = self.latest_tag_id
        if tag_val is not None and 0 <= tag_val <= 4:
            self.get_logger().info(f'>>> ตรวจพบ AprilTag ID: {tag_val} <<<')
            if tag_val == 0:
                self.get_logger().info(' Tag = 0 : ไม่ต้องปล่อยลูกบาศก์')
            else:
                self.get_logger().info(f'📦 สั่งปล่อยลูกบาศก์ {tag_val} ชิ้น...')
                for i in range(tag_val):
                    servo_msg = Int32()
                    # เปิด Servo
                    servo_msg.data = self.OPEN_ANGLE
                    self.servo_pub.publish(servo_msg)
                    time.sleep(0.8)
                    
                    # ปิด Servo
                    servo_msg.data = self.CLOSE_ANGLE
                    self.servo_pub.publish(servo_msg)
                    time.sleep(0.8)
        else:
            self.get_logger().warn('⚠️ ไม่พบ AprilTag (หรือค่านอกเหนือ 0-4) : ข้ามการปล่อยสิ่งของ')

        # คืนค่าปิด Servo
        servo_msg = Int32()
        servo_msg.data = self.CLOSE_ANGLE
        self.servo_pub.publish(servo_msg)
        
        self.latest_tag_id = None # รีเซ็ตค่า Tag
        self.is_dropping = False

    def timer_callback(self):
        # ถ้าอยู่ในขั้นตอนการปล่อยลูกบาศก์ ให้ข้ามการสั่งเดินใน Timer
        if self.is_dropping:
            return

        move_msg = Twist()
        servo_msg = Int32()
        servo_msg.data = self.CLOSE_ANGLE
        
        self.ticks += 1

        # 0.0 - 1.0 วินาที: หน่วงเวลาเริ่มต้น
        if self.ticks <= 10:
            pass

        # 1.0 - 4.0 วินาที: 1. เดินหน้า 3 วินาที
        elif self.ticks <= 40:
            move_msg.linear.x = 0.2
            if self.ticks == 11:
                self.get_logger().info('1. เดินหน้า 3 วินาที')

        # 4.0 - 6.0 วินาที: 2. เลี้ยวขวา 2 วินาที
        elif self.ticks <= 60:
            move_msg.angular.z = -0.9
            if self.ticks == 41:
                self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # 6.0 - 7.0 วินาที: 3. เดินหน้า 1 วินาที
        elif self.ticks <= 70:
            move_msg.linear.x = 0.2
            if self.ticks == 61:
                self.get_logger().info('3. เดินหน้า 1 วินาที')

        # 7.0 วินาที: 4. หยุดสแกน AprilTag & ปล่อยลูกบาศก์ (รอบที่ 1)
        elif self.ticks == 71:
            self.get_logger().info('4. เข้าสู่จุดปล่อยลูกบาศก์ (รอบแรก)')
            self.drop_cubes_by_tag()

        # 8.0 - 9.0 วินาที: 5. ถอยหลัง 1 วินาที
        elif self.ticks <= 100:
            move_msg.linear.x = -0.2
            if self.ticks == 91:
                self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # 9.0 - 11.0 วินาที: 6. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 120:
            move_msg.angular.z = 0.9
            if self.ticks == 101:
                self.get_logger().info('6. เลี้ยวซ้าย 2 วินาที')

        # 11.0 - 15.0 วินาที: 7. เดินตรง 4 วินาที
        elif self.ticks <= 160:
            move_msg.linear.x = 0.2
            if self.ticks == 121:
                self.get_logger().info('7. เดินตรง 4 วินาที')

        # 15.0 - 17.0 วินาที: 8. เลี้ยวขวา 2 วินาที
        elif self.ticks <= 180:
            move_msg.angular.z = -0.9
            if self.ticks == 161:
                self.get_logger().info('8. เลี้ยวขวา 2 วินาที')

        # 17.0 - 19.0 วินาที: 9. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 200:
            move_msg.angular.z = 0.9
            if self.ticks == 181:
                self.get_logger().info('9. เลี้ยวซ้าย 2 วินาที')

        # 19.0 วินาที: 10. หยุดสแกน AprilTag & ปล่อยลูกบาศก์ (รอบที่ 2)
        elif self.ticks == 201:
            self.get_logger().info('10. เข้าสู่จุดปล่อยลูกบาศก์ (รอบสอง)')
            self.drop_cubes_by_tag()

        # 20.0 - 21.0 วินาที: สั่งหยุดหุ่นยนต์ย้ำๆ 1 วินาที
        elif self.ticks <= 220:
            move_msg.linear.x = 0.0
            move_msg.angular.z = 0.0
            if self.ticks == 206:
                self.get_logger().info('🛑 กำลังสั่งหยุดหุ่นยนต์...')

        # หลังจบภารกิจ: จบการทำงาน
        else:
            self.get_logger().info('เสร็จสิ้นภารกิจทั้งหมด! ปิดโปรแกรมเรียบร้อย')
            raise SystemExit

        # ส่งสัญญาณเคลื่อนที่และเซอร์โว
        self.cmd_vel_pub.publish(move_msg)
        self.servo_pub.publish(servo_msg)

def main(args=None):
    rclpy.init(args=args)
    node = FullMissionController()
    
    try:
        rclpy.spin(node)
    except (KeyboardInterrupt, SystemExit):
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