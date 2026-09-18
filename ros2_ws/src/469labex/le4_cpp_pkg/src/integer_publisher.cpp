#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::chrono_literals;

class IntegerPublisherNode : public rclcpp::Node
{
public:
  IntegerPublisherNode() : Node("integer_publisher")
  {
    publisher_ = create_publisher<example_interfaces::msg::Int64>("integer", 10);
    timer_ = create_wall_timer(2s, [this] { publish_integer(); });
    RCLCPP_INFO(get_logger(), "The integer publisher has started.");
  }

private:
  void publish_integer()
  {
    auto msg = example_interfaces::msg::Int64();
    msg.data = 5;
    publisher_->publish(msg);
  }

  rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
  rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<IntegerPublisherNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}