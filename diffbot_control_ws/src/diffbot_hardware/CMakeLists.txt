cmake_minimum_required(VERSION 3.8)
project(diffbot_hardware)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(dynamixel_sdk REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(pluginlib REQUIRED)


add_library(${PROJECT_NAME} SHARED
  src/diffbot_hardware_interface.cpp)

target_include_directories(${PROJECT_NAME} PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>)

ament_target_dependencies(${PROJECT_NAME}
  rclcpp
  dynamixel_sdk
  hardware_interface
  rclcpp_lifecycle
  pluginlib)

pluginlib_export_plugin_description_file(hardware_interface diffbot_hardware_interface_plugin.xml)

install(TARGETS ${PROJECT_NAME}
  LIBRARY DESTINATION lib)

install(DIRECTORY include/
  DESTINATION include)

ament_package()
