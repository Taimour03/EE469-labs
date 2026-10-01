cmake_minimum_required(VERSION 3.8)
project(dnmxl_test)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(dynamixel_sdk REQUIRED)

add_executable(test_servomotors src/test_servomotors.cpp)
target_include_directories(test_servomotors PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)
ament_target_dependencies(test_servomotors rclcpp dynamixel_sdk)

install(TARGETS test_servomotors
  DESTINATION lib/${PROJECT_NAME})

ament_package()
