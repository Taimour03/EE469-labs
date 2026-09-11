#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from example_interfaces.msg import String

class MyTalkerNode(LifecycleNode):
    def __init__(self):
        super().__init__("my_talker")
        self.get_logger().info("Executing constructor")
        self.counter_ = 0

    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_configure")
        self.publisher_ = self.create_lifecycle_publisher(String, "my_chatter", 10)
        self.timer_ = self.create_timer(0.5, self.publish_talker)
        return TransitionCallbackReturn.SUCCESS

    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_cleanup")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        return TransitionCallbackReturn.SUCCESS

    def publish_talker(self):
        self.counter_ += 1
        msg = String()
        msg.data = "Hello World: " + str(self.counter_)
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = MyTalkerNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        if rclpy.ok():
            node.destroy_node()

if __name__ == "__main__":
    main()