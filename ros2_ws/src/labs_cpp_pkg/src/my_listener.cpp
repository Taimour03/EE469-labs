#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

class MyListenerNode : public rclcpp::Node
{
public:
  MyListenerNode() : Node("my_listener")
  {
    subscriber_ = create_subscription<example_interfaces::msg::String>(
        "my_chatter", 10,
        [this](example_interfaces::msg::String::SharedPtr msg)
        { callback_my_chatter(msg); });
  }
private:
  void callback_my_chatter(const example_interfaces::msg::String::SharedPtr msg)
  {
    RCLCPP_INFO(get_logger(), "[%s]", msg->data.c_str());
  }

  rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MyListenerNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}