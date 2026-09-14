#!/usr/bin/env python3
import random
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from std_msgs.msg import Float64
import signal
import time
_SIGINT_GRACE_PERIOD_SEC = 5.0


class SensorDriverNode(LifecycleNode):
    def __init__(self):
        super().__init__("sensor_driver_node")
        self.finalized = False

    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_configure")
        self.publisher_ = self.create_lifecycle_publisher(Float64, "raw_sensor_data", 10)
        self.timer_ = self.create_timer(0.5, self.publish_sensor_data)
        return TransitionCallbackReturn.SUCCESS

    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_activate")
        return super().on_activate(previous_state)

    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_deactivate")
        return super().on_deactivate(previous_state)

    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_cleanup")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_shutdown")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        self.finalized = True
        return TransitionCallbackReturn.SUCCESS

    def publish_sensor_data(self):
        msg = Float64()
        msg.data = round(random.uniform(0.1, 5.0), 3)
        self.publisher_.publish(msg)
        self.get_logger().info(str(msg.data))


def main(args=None):
    rclpy.init(args=args, signal_handler_options=rclpy.SignalHandlerOptions.NO)
    node = SensorDriverNode()

    sigint_time = None
    def _on_sigint(signum, frame):
        nonlocal sigint_time
        sigint_time = time.monotonic()
    signal.signal(signal.SIGINT, _on_sigint)

    try:
        while rclpy.ok() and not node.finalized:
            rclpy.spin_once(node, timeout_sec=0.2)
            if sigint_time is not None and time.monotonic() - sigint_time > _SIGINT_GRACE_PERIOD_SEC:
                break
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()