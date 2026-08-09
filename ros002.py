import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32

class FullMissionController(Node):
    def __init__(self):
        super().__init__('full_mission_controller_node')
        
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)
        
        # ตั้งค่ามุมเซอร์โว
        self.CLOSE_ANGLE = 0
        self.OPEN_ANGLE = 80
        
        self.ticks = 0
        self.timer = self.create_timer(0.1, self.timer_callback) # 1 tick = 0.1 วินาที
        self.get_logger().info('กำลังเชื่อมต่อระบบ... เริ่มรันภารกิจ')

    def timer_callback(self):
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

        # 7.0 - 8.0 วินาที: 4. ปล่อยลูกบาศก์ (ครั้งที่ 1)
        elif self.ticks <= 75:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 71:
                self.get_logger().info('4. ปล่อยลูกบาศก์ 1(รอบแรก)!เปิด')

        elif self.ticks <= 80:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 76:
                        self.get_logger().info('4. ปล่อยลูกบาศก์ 1(รอบแรก)!ปิด')

        elif self.ticks <= 85:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 81:
                self.get_logger().info('4. ปล่อยลูกบาศก์ 2(รอบแรก)!เปิด')

        elif self.ticks <= 90:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 86:
                        self.get_logger().info('4. ปล่อยลูกบาศก์ 2(รอบแรก)!ปิด')

        elif self.ticks <= 95:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 91:
                self.get_logger().info('4. ปล่อยลูกบาศก์ 3(รอบแรก)!เปิด')

        elif self.ticks <= 100:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 96:
                        self.get_logger().info('4. ปล่อยลูกบาศก์ 3(รอบแรก)!ปิด')

        elif self.ticks <= 105:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 101:
                self.get_logger().info('4. ปล่อยลูกบาศก์ 4(รอบแรก)!เปิด')

        elif self.ticks <= 110:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 106:
                        self.get_logger().info('4. ปล่อยลูกบาศก์ 4(รอบแรก)!ปิด')

        elif self.ticks <= 120:
            move_msg.linear.x = 0.0
            if self.ticks == 161:
                self.get_logger().info('9. หยุด')

        # 8.0 - 9.0 วินาที: 5. ถอยหลัง 1 วินาที
        elif self.ticks <= 130:
            move_msg.linear.x = -0.2
            if self.ticks == 121:
                self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # 9.0 - 11.0 วินาที: 6. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 150:
            move_msg.angular.z = 0.9
            if self.ticks == 131:
                self.get_logger().info('6. เลี้ยวซ้าย 2 วินาที')

        # 11.0 - 14.0 วินาที: 7. เดินตรง 3 วินาที
        elif self.ticks <= 190:
            move_msg.linear.x = 0.2
            if self.ticks == 151:
                self.get_logger().info('7. เดินตรง 4 วินาที')

        # --- ส่วนที่เพิ่มใหม่ตามคำสั่ง ---

        # 14.0 - 16.0 วินาที: 8. เลี้ยวขวา 2 วินาที
        elif self.ticks <= 210:
            move_msg.angular.z = -0.9
            if self.ticks == 191:
                self.get_logger().info('8. เลี้ยวขวา 2 วินาที')

        # 16.0 - 17.0 วินาที: 9. เดินตรง 1 วินาที
        elif self.ticks <= 230:
            move_msg.linear.x = 0.2
            if self.ticks == 211:
                self.get_logger().info('9. เดินตรง 2 วินาที')

        # 17.0 - 19.0 วินาที: 10. เลี้ยวซ้าย 2 วินาที
        elif self.ticks <= 250:
            move_msg.angular.z = 0.9
            if self.ticks == 231:
                self.get_logger().info('10. เลี้ยวซ้าย 2 วินาที')

        elif self.ticks <= 260:
            move_msg.linear.x = 0.2
            if self.ticks == 251:
                self.get_logger().info('9. เดินตรง 1 วินาที')

        # 19.0 - 20.0 วินาที: 11. ปล่อยลูกบาศก์ (ครั้งที่ 2)
        elif self.ticks <= 265:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 261:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสอง)!')

        elif self.ticks <= 270:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 266:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสอง)!')

        elif self.ticks <= 275:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 271:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสอง)!')
        
        elif self.ticks <= 280:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 276:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสอง)!')

        elif self.ticks <= 285:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 281:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสอง)!')

        elif self.ticks <= 290:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 286:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสอง)!')

        elif self.ticks <= 295:
            servo_msg.data = self.OPEN_ANGLE
            if self.ticks == 291:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสอง)!')
        
        elif self.ticks <= 300:
            servo_msg.data = self.CLOSE_ANGLE
            if self.ticks == 296:
                self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสอง)!')

        elif self.ticks <= 310:
            move_msg.linear.x = 0.0
            if self.ticks == 301:
                self.get_logger().info('9. หยุด')

        elif self.ticks <= 320:
            move_msg.linear.x = -0.2
            if self.ticks == 311:
                self.get_logger().info('5. ถอยหลัง 1 วินาที')

        elif self.ticks <= 340:
            move_msg.angular.z = 0.9
            if self.ticks == 321:
                self.get_logger().info('10. เลี้ยวซ้าย 2 วินาที')

        elif self.ticks <= 360:
            move_msg.linear.x = 0.2
            if self.ticks == 341:
                self.get_logger().info('9. เดินตรง 2 วินาที')

        elif self.ticks <= 370:
            move_msg.angular.z = 0.9
            if self.ticks == 361:
                self.get_logger().info('10. เลี้ยวซ้าย 2 วินาที')

        elif self.ticks <= 420:
            move_msg.linear.x = 0.2
            if self.ticks == 371:
                self.get_logger().info('5. ตรง 5 วินาที')

        # elif self.ticks <= 350:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 321:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 370:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 351:
        #         self.get_logger().info('5. ตรง 2 วินาที')

        # elif self.ticks <= 390:
        #     move_msg.angular.z = 0.9
        #     if self.ticks == 371:
        #         self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที')

        # elif self.ticks <= 420:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 391:
        #         self.get_logger().info('5. ตรง 3 วินาที')

        # elif self.ticks <= 440:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 421:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 450:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 441:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 470:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 451:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 480:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 471:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 485:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 481:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสาม)!')

        # elif self.ticks <= 490:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 486:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสาม)!')

        # elif self.ticks <= 495:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 491:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสาม)!')
        
        # elif self.ticks <= 500:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 496:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสาม)!')

        # elif self.ticks <= 505:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 501:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสาม)!')

        # elif self.ticks <= 510:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 506:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสาม)!')

        # elif self.ticks <= 515:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 511:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสาม)!')
        
        # elif self.ticks <= 520:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 516:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสาม)!')

        # elif self.ticks <= 530:
        #     move_msg.linear.x = 0.0
        #     if self.ticks == 521:
        #         self.get_logger().info('9. หยุด')

        # elif self.ticks <= 540:
        #     move_msg.linear.x = -0.2
        #     if self.ticks == 531:
        #         self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # elif self.ticks <= 560:
        #     move_msg.angular.z = 0.9
        #     if self.ticks == 541:
        #         self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที')

        # elif self.ticks <= 570:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 561:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 590:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 571:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 600:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 591:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 605:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 601:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสี่)!')

        # elif self.ticks <= 610:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 606:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบสี่)!')

        # elif self.ticks <= 615:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 611:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสี่)!')
        
        # elif self.ticks <= 620:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 616:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบสี่)!')

        # elif self.ticks <= 625:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 621:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสี่)!')
        
        # elif self.ticks <= 630:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 626:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบสี่)!')

        # elif self.ticks <= 635:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 631:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสี่)!')
        
        # elif self.ticks <= 640:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 636:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบสี่)!')

        # elif self.ticks <= 650:
        #     move_msg.linear.x = 0.0
        #     if self.ticks == 651:
        #         self.get_logger().info('9. หยุด')

        # elif self.ticks <= 640:
        #     move_msg.linear.x = -0.2
        #     if self.ticks == 651:
        #         self.get_logger().info('5. ถอยหลัง 1 วินาที')
        
        # elif self.ticks <= 660:
        #     move_msg.angular.z = 0.9
        #     if self.ticks == 641:
        #         self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที')

        # elif self.ticks <= 670:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 661:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 690:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 671:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 750:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 691:
        #         self.get_logger().info('5. ตรง 6 วินาที')

        # elif self.ticks <= 770:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 751:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 780:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 771:
        #         self.get_logger().info('5. ตรง 1 วินาที')

        # elif self.ticks <= 785:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 781:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบห้า)!')

        # elif self.ticks <= 790:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 786:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 1(รอบห้า)!')

        # elif self.ticks <= 795:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 791:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบห้า)!')
        
        # elif self.ticks <= 800:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 796:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 2(รอบห้า)!')

        # elif self.ticks <= 805:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 801:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบห้า)!')
        
        # elif self.ticks <= 810:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 806:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 3(รอบห้า)!')
        
        # elif self.ticks <= 815:
        #     servo_msg.data = self.OPEN_ANGLE
        #     if self.ticks == 811:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบห้า)!')
                
        # elif self.ticks <= 820:
        #     servo_msg.data = self.CLOSE_ANGLE
        #     if self.ticks == 816:
        #         self.get_logger().info('11. ปล่อยลูกบาศก์ 4(รอบห้า)!')

        # elif self.ticks <= 830:
        #     move_msg.linear.x = 0.0
        #     if self.ticks == 821:
        #         self.get_logger().info('9. หยุด')
        
        # elif self.ticks <= 840:
        #     move_msg.linear.x = -0.2
        #     if self.ticks == 831:
        #         self.get_logger().info('5. ถอยหลัง 1 วินาที')

        # elif self.ticks <= 860:
        #     move_msg.angular.z = 0.9
        #     if self.ticks == 841:
        #         self.get_logger().info('2. เลี้ยวซ้าย 2 วินาที')

        # elif self.ticks <= 890:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 861:
        #         self.get_logger().info('5. ตรง 3 วินาที')

        # elif self.ticks <= 910:
        #     move_msg.angular.z = -0.9
        #     if self.ticks == 891:
        #         self.get_logger().info('2. เลี้ยวขวา 2 วินาที')

        # elif self.ticks <= 1030:
        #     move_msg.linear.x = 0.2
        #     if self.ticks == 911:
        #         self.get_logger().info('5. ตรง 12 วินาที')

        

    # 20.0 - 21.0 วินาที: สั่งหยุดหุ่นยนต์ย้ำๆ 1 วินาที
        elif self.ticks <= 430:
            move_msg.linear.x = 0.0
            move_msg.angular.z = 0.0
            if self.ticks == 421:
                self.get_logger().info('🛑 กำลังสั่งหยุดหุ่นยนต์...')

        # หลัง 21 วินาที: จบการทำงาน
        else:
            self.get_logger().info('เสร็จสิ้นภารกิจทั้งหมด! ปิดโปรแกรมเรียบร้อย')
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