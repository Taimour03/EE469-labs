cmake_minimum_required(VERSION 3.8)
project(le4_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(integer_publisher src/integer_publisher.cpp)
ament_target_dependencies(integer_publisher rclcpp example_interfaces)

add_executable(cumulative_adder src/cumulative_adder.cpp)
ament_target_dependencies(cumulative_adder rclcpp example_interfaces)

install(TARGETS
  integer_publisher
  cumulative_adder
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()