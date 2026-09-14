#!/usr/bin/env python3
from collections import deque
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from std_msgs.msg import Float64
import signal
import time

_SIGINT_GRACE_PERIOD_SEC = 5.0
WINDOW_LENGTH = 5


class SensorProcessorNode(LifecycleNode):
    def __init__(self):
        super().__init__("sensor_processor_node")
        self.finalized = False
        self.window_ = deque(maxlen=WINDOW_LENGTH)

    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_configure")
        self.publisher_ = self.create_lifecycle_publisher(Float64, "processed_sensor_data", 10)
        self.subscriber_ = self.create_subscription(Float64, "raw_sensor_data", self.callback_raw_data, 10)
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
        self.destroy_subscription(self.subscriber_)
        self.window_.clear()
        return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state: LifecycleState):
        self.get_logger().info(f"Node '{self.get_name()}' is in state '{previous_state.label}', executing on_shutdown")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_subscription(self.subscriber_)
        self.finalized = True
        return TransitionCallbackReturn.SUCCESS

    def callback_raw_data(self, msg):
        self.window_.append(msg.data)
        average = sum(self.window_) / len(self.window_)
        out_msg = Float64()
        out_msg.data = round(average, 3)
        self.publisher_.publish(out_msg)
        self.get_logger().info(str(out_msg.data))


def main(args=None):
    rclpy.init(args=args, signal_handler_options=rclpy.SignalHandlerOptions.NO)
    node = SensorProcessorNode()

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