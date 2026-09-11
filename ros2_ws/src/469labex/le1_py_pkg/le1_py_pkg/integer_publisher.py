#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from example_interfaces.msg import Int64

class IntegerPublisherNode(LifecycleNode):
    def __init__(self):
        super().__init__("integer_publisher")  # must match MANAGED_NODES
        # any plain instance variables go here — NOT the publisher or timer

    def on_configure(self, previous_state: LifecycleState):
        # create the publisher here (create_lifecycle_publisher, not create_publisher)
        # create the timer here (same call you already have, just moved from __init__)
        # return TransitionCallbackReturn.SUCCESS

    def on_activate(self, previous_state: LifecycleState):
        # same one-liner pattern as my_talker.py's on_activate

    def on_deactivate(self, previous_state: LifecycleState):
        # same one-liner pattern as my_talker.py's on_deactivate

    def on_cleanup(self, previous_state: LifecycleState):
        # destroy the publisher and timer you created in on_configure
        # return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state: LifecycleState):
        # same cleanup as on_cleanup
        # return TransitionCallbackReturn.SUCCESS

    def publish_integer(self):
        # keep your original publish logic here — msg.data = 5, publish, log
        pass

def main(args=None):
    # follow the same structure as my_talker.py's main()
    pass

if __name__ == "__main__":
    main()