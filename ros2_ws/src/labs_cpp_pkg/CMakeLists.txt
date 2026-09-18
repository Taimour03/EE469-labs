cmake_minimum_required(VERSION 3.8)
project(labs_cpp_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(example_interfaces REQUIRED)

add_executable(my_talker src/my_talker.cpp)
ament_target_dependencies(my_talker rclcpp example_interfaces)

add_executable(my_listener src/my_listener.cpp)
ament_target_dependencies(my_listener rclcpp example_interfaces)

install(TARGETS
  my_talker
  my_listener
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()