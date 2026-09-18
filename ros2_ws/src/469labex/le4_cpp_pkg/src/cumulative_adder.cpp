#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

class CumulativeAdderNode : public rclcpp::Node
{
public:
  CumulativeAdderNode() : Node("cumulative_adder"), sum_(0)
  {
    subscriber_ = create_subscription<example_interfaces::msg::Int64>(
        "integer", 10,
        [this](example_interfaces::msg::Int64::SharedPtr msg)
        { callback_integer(msg); });
    publisher_ = create_publisher<example_interfaces::msg::Int64>("integer_sum", 10);
    RCLCPP_INFO(get_logger(), "The cumulative adder has started.");
  }

private:
  void callback_integer(const example_interfaces::msg::Int64::SharedPtr msg)
  {
    sum_ += msg->data;
    auto sum_msg = example_interfaces::msg::Int64();
    sum_msg.data = sum_;
    publisher_->publish(sum_msg);
  }

  int64_t sum_;
  rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscriber_;
  rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<CumulativeAdderNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}