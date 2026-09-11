#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from lifecycle_msgs.srv import ChangeState
from lifecycle_msgs.msg import State, Transition
import signal
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

    def shutdown(self):
        self.get_logger().info('Shutdown: reverse dependency order')
        for name in reversed(self._node_names):
            self.change_state(name, Transition.TRANSITION_DEACTIVATE)
            self.get_logger().info(f'{name}: Transition to inactive state complete')
        for name in reversed(self._node_names):
            self.change_state(name, Transition.TRANSITION_CLEANUP)
            self.get_logger().info(f'{name}: Transition to unconfigured state complete')
        for name in reversed(self._node_names):
            self.change_state(name, Transition.TRANSITION_UNCONFIGURED_SHUTDOWN)
            self.get_logger().info(f'{name}: Transition to finalized state complete')

def main(args=None):
    rclpy.init(args=args, signal_handler_options=rclpy.SignalHandlerOptions.NO)
    manager = LifecycleManager(MANAGED_NODES)

    shutdown_requested = False
    def _on_sigint(signum, frame):
        nonlocal shutdown_requested
        shutdown_requested = True
    signal.signal(signal.SIGINT, _on_sigint)

    try:
        manager.startup()
        manager.get_logger().info('Managed nodes active - spinning until shutdown (Ctrl+C)')
        while rclpy.ok() and not shutdown_requested:
            rclpy.spin_once(manager, timeout_sec=0.2)
    except RuntimeError as exc:
        manager.get_logger().error(str(exc))
    finally:
        manager.shutdown()
        manager.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()

if __name__ == "__main__":
    main()