import rclpy

from rclpy.node import Node

from geometry_msgs.msg import Twist

from std_msgs.msg import Int32



class FullMissionController(Node):

    def __init__(self):

        super().__init__('full_mission_controller_node')

        

        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.servo_pub = self.create_publisher(Int32, '/servo_s2', 10)

        

        # ปรับ/คงค่าเซอร์โวตามเดิม

        self.CLOSE_ANGLE = 0

        self.OPEN_ANGLE = 80

        

        self.ticks = 0

        self.timer = self.create_timer(0.1, self.timer_callback)

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

        elif self.ticks <= 50:

            move_msg.linear.x = 0.2

            if self.ticks == 11:

                self.get_logger().info('1. เดินหน้า 4 วินาที')



        # 4.0 - 6.0 วินาที: 2. เลี้ยวขวา 2 วินาที (ปรับความเร็วเชิงมุมเป็นติดลบ)

        elif self.ticks <= 70:

            move_msg.angular.z = -0.9

            if self.ticks == 51:

                self.get_logger().info('2. เลี้ยวขวา 2 วินาที')



        # 7.0 - 8.0 วินาที: 4. ปล่อยลูกบาศก์ (คงเดิม)

        elif self.ticks <= 75:

            servo_msg.data = self.OPEN_ANGLE

            if self.ticks == 71:

                self.get_logger().info('4. ปล่อยลูกบาศก์!')

        elif self.ticks <= 80:
        
                    servo_msg.data = self.CLOSE_ANGLE
        
                    if self.ticks == 76:
        
                        self.get_logger().info('4. ปล่อยลูกบาศก์!')



        # 9.0 - 11.0 วินาที: 6. เลี้ยวซ้าย 2 วินาที (ปรับความเร็วเชิงมุมเป็นบวก)

        elif self.ticks <= 100:

            move_msg.angular.z = 0.9

            if self.ticks == 81:

                self.get_logger().info('6. เลี้ยวซ้าย 2 วินาที')



        # 11.0 - 14.0 วินาที: 7. เดินตรง 3 วินาที

        elif self.ticks <= 150:

            move_msg.linear.x = 0.2

            if self.ticks == 101:

                self.get_logger().info('7. เดินตรง 5 วินาที')

        elif self.ticks <= 170:
        
                    move_msg.angular.z = -0.9
        
                    if self.ticks == 151:
        
                        self.get_logger().info('8. เลี้ยวขวา 2 วินาที')

        elif self.ticks <= 200:
        
                    move_msg.linear.x = 0.2
        
                    if self.ticks == 171:
        
                        self.get_logger().info('9. เดินตรง 3 วินาที')

        elif self.ticks <= 220:
        
                    move_msg.angular.z = 0.9
        
                    if self.ticks == 201:
        
                        self.get_logger().info('10. เลี้ยวซ้าย 2 วินาที')

    
        elif self.ticks <= 225:

            servo_msg.data = self.OPEN_ANGLE

            if self.ticks == 221:

                self.get_logger().info('12. ปล่อยลูกบาศก์!')

        elif self.ticks <= 230:
        
                    servo_msg.data = self.CLOSE_ANGLE
        
                    if self.ticks == 226:
        
                        self.get_logger().info('13. ปล่อยลูกบาศก์!')

       

        elif self.ticks <= 250:
        
                    move_msg.angular.z = -0.9
        
                    if self.ticks == 231:
        
                        self.get_logger().info('15. เลี้ยวขวา 2 วินาที')

        elif self.ticks <= 260:
        
                    move_msg.linear.x = 0.2
        
                    if self.ticks == 251:
        
                        self.get_logger().info('16. เดินตรง 1 วินาที')

        elif self.ticks <= 280:
                
                    move_msg.angular.z = 0.9
                
                    if self.ticks == 261:
                
                        self.get_logger().info('17. เลี้ยวซ้าย 2 วินาที')

        elif self.ticks <= 300:
                
                            move_msg.linear.x = 0.2
                
                            if self.ticks == 281:
                
                                self.get_logger().info('18. เดินตรง 2 วินาที')

      
        # 14.0 - 15.0 วินาที: สั่งหยุดหุ่นยนต์ย้ำๆ 1 วินาที

        elif self.ticks <= 310:

            move_msg.linear.x = 0.0

            move_msg.angular.z = 0.0

            if self.ticks == 301:

                self.get_logger().info('🛑 กำลังสั่งหยุดหุ่นยนต์...')



        # หลัง 15 วินาที: จบการทำงาน

        else:

            self.get_logger().info('เสร็จสิ้นภารกิจ! ปิดโปรแกรมเรียบร้อย')

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