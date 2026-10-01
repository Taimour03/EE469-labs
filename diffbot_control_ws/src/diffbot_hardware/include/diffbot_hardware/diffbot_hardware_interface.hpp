#pragma once

#include "hardware_interface/system_interface.hpp"
#include "diffbot_hardware/xl330_driver.hpp"

namespace my_diffbot_hardware {

class DiffbotHardwareInterface : public hardware_interface::SystemInterface
{
public:
    // Lifecycle methods - called during controller_manager state transitions
    hardware_interface::CallbackReturn on_init(
        const hardware_interface::HardwareComponentInterfaceParams & params) override;
    hardware_interface::CallbackReturn
        on_configure(const rclcpp_lifecycle::State & previous_state) override;
    hardware_interface::CallbackReturn
        on_activate(const rclcpp_lifecycle::State & previous_state) override;
    hardware_interface::CallbackReturn
        on_deactivate(const rclcpp_lifecycle::State & previous_state) override;

    // Real-time loop methods - called at controller_manager update rate (50 Hz)
    hardware_interface::return_type
        read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
    hardware_interface::return_type
        write(const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
    std::shared_ptr<XL330Driver> driver_;
    int left_dnmxl_id_;
    int right_dnmxl_id_;
    std::string port_;
    bool initialized_{false};
    double init_left_pos_{0.0};
    double init_right_pos_{0.0};

}; // class DiffbotHardwareInterface

} // namespace my_diffbot_hardware
