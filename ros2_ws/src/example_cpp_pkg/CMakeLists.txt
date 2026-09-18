cmake_minimum_required(VERSION 3.8)
project(example_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)

add_executable(ex_node src/example_node.cpp)
ament_target_dependencies(ex_node rclcpp)

install(TARGETS
  ex_node
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()