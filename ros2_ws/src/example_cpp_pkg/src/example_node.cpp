#include "rclcpp/rclcpp.hpp"

class ExampleNode : public rclcpp::Node
{
public:
  ExampleNode() : Node("ex_test"), counter_(0)
  {
    RCLCPP_INFO(get_logger(), "Hello world");
    timer_ = create_wall_timer(std::chrono::seconds(1),
                                [this] { timerCallback(); });
  }
private:
  void timerCallback()
  {
    RCLCPP_INFO(get_logger(), "Count %d", counter_);
    counter_++;
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
  return(0);
}