#include "rclcpp/rclcpp.hpp"

class MyNode : public rclcpp::Node // Replace MyNode with your chosen name
{
public:
  MyNode() : Node("node_name") // Replace MyNode and node_name with your chosen names
  {
  }

private:
};

int main(int argc, char **argv)
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<MyNode>(); // Replace MyNode with your chosen name
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}