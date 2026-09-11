#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from lifecycle_msgs.srv import ChangeState
from lifecycle_msgs.msg import Transition
MANAGED_NODES = ['my_talker']

class LifecycleManager(Node):
    def __init__(self, node_names):
        super().__init__("lifecycle_manager")
        self._node_names = node_names
        self._change_state_clients = {
            name: self.create_client(ChangeState, f'/{name}/change_state')
            for name in node_names
        }

    def change_state(self, node_name, transition_id):
        self._change_state_clients[node_name].wait_for_service()
        client = self._change_state_clients[node_name]
        request = ChangeState.Request()
        request.transition.id = transition_id
        future = client.call_async(request)
        rclpy.spin_until_future_complete(self, future)

    def startup(self):
        self.get_logger().info('Startup: configure then activate in dependency order')
        for name in self._node_names:
            self.change_state(name, Transition.TRANSITION_CONFIGURE)
            self.get_logger().info(f'{name}: Transition to inactive state complete')
        for name in self._node_names:
            self.change_state(name, Transition.TRANSITION_ACTIVATE)
            self.get_logger().info(f'{name}: Transition to active state complete')

def main(args=None):
    rclpy.init(args=args)
    manager = LifecycleManager(MANAGED_NODES)
    manager.startup()
    rclpy.shutdown()

if __name__ == "__main__":
    main()