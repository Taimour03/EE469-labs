#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::chrono_literals;

class MyTalkerNode : public rclcpp::Node
{
public:
  MyTalkerNode() : Node("my_talker"), counter_(1)
  {
    publisher_ = create_publisher<example_interfaces::msg::String>("my_chatter", 10);
    timer_ = create_wall_timer(1s, [this] { publish_talker(); });
  }

private:
  void publish_talker()
  {
    auto msg = example_interfaces::msg::String();
    msg.data = std::string("Hello world: ") + std::to_string(counter_);
    publisher_->publish(msg);
    RCLCPP_INFO(get_logger(), "Publishing: 'Hello World: %d'", counter_);
    counter_++;
  }
  int counter_;
  rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;

};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MyTalkerNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}