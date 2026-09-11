#!/usr/bin/env python3
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from example_interfaces.msg import Int64

class CumulativeAdderNode(LifecycleNode):
    def __init__(self):
        super().__init__("cumulative_adder")
        # plain instance variables go here — e.g. wherever you track the running sum
        # NOT the publisher or subscriber

    def on_configure(self, previous_state: LifecycleState):
        # create the publisher here (create_lifecycle_publisher, not create_publisher)
        # create the subscriber here (create_subscription — same call as before, just moved)
        # return TransitionCallbackReturn.SUCCESS

    def on_activate(self, previous_state: LifecycleState):
        # same one-liner pattern as my_talker.py's on_activate

    def on_deactivate(self, previous_state: LifecycleState):
        # same one-liner pattern as my_talker.py's on_deactivate

    def on_cleanup(self, previous_state: LifecycleState):
        # destroy the publisher and subscriber you created in on_configure
        # return TransitionCallbackReturn.SUCCESS

    def on_shutdown(self, previous_state: LifecycleState):
        # same cleanup as on_cleanup
        # return TransitionCallbackReturn.SUCCESS

    def callback_integer(self, msg):
        # keep your original logic here — add to the sum, publish, log
        pass

def main(args=None):
    # follow the same structure as my_talker.py's main()
    pass

if __name__ == "__main__":
    main()