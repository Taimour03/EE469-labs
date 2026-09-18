#include "rclcpp/rclcpp.hpp"

class ExampleNode : public rclcpp::Node
{
public:
  ExampleNode() : Node("ex_test"), counter_(0)
  {
    RCLCPP_INFO(get_logger(), "Hello World");
    timer_ = create_wall_timer(std::chrono::milliseconds(500),
                                [this] { timerCallback(); });
  }
private:
  void timerCallback()
  {
    counter_++;
    RCLCPP_INFO(get_logger(), "Count %d", counter_);
  }
  rclcpp::TimerBase::SharedPtr timer_;
  int counter_;
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<ExampleNode>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}