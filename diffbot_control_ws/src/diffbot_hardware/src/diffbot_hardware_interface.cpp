#include "diffbot_hardware/diffbot_hardware_interface.hpp"
#include "rclcpp/rclcpp.hpp"
#include "pluginlib/class_list_macros.hpp"

namespace my_diffbot_hardware {

hardware_interface::CallbackReturn DiffbotHardwareInterface::on_init(
    const hardware_interface::HardwareComponentInterfaceParams & params)
{
    if (hardware_interface::SystemInterface::on_init(params) !=
        hardware_interface::CallbackReturn::SUCCESS)
    {
        return hardware_interface::CallbackReturn::ERROR;
    }

    port_= info_.hardware_parameters.at("dynamixel_port");
    left_dnmxl_id_= std::stoi(info_.hardware_parameters.at("left_dnmxl_id"));
    right_dnmxl_id_= std::stoi(info_.hardware_parameters.at("right_dnmxl_id"));
    driver_ = std::make_shared<XL330Driver>(port_);
    return hardware_interface::CallbackReturn::SUCCESS;
}
hardware_interface::CallbackReturn DiffbotHardwareInterface::on_configure(
    const rclcpp_lifecycle::State & /*previous_state*/)
{
    try {
        driver_->init();
    } catch (const std::exception & e) {
        RCLCPP_ERROR(get_logger(), "Failed to configure port %s: %s", port_.c_str(), e.what());
        return hardware_interface::CallbackReturn::ERROR;
    }
    return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn DiffbotHardwareInterface::on_activate
    (const rclcpp_lifecycle::State & /*previous_state*/)
{
    driver_->activateVelocityMode(left_dnmxl_id_);
    driver_->activateVelocityMode(right_dnmxl_id_);
    return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::CallbackReturn DiffbotHardwareInterface::on_deactivate
    (const rclcpp_lifecycle::State & /*previous_state*/)
{
    driver_->deactivate(left_dnmxl_id_);
    driver_->deactivate(right_dnmxl_id_);
    return hardware_interface::CallbackReturn::SUCCESS;
}

hardware_interface::return_type DiffbotHardwareInterface::read
    (const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
    double left_vel = driver_->getVelocity(left_dnmxl_id_);
    double right_vel = -1.0 * driver_->getVelocity(right_dnmxl_id_);
    double left_pos = driver_->getPosition(left_dnmxl_id_);
    double right_pos = -1.0 * driver_->getPosition(right_dnmxl_id_);
    if (!initialized_)
    {
        init_left_pos_ = left_pos;
        init_right_pos_ = right_pos;
        initialized_ = true;
    }
    left_pos = left_pos - init_left_pos_;
    right_pos = right_pos - init_right_pos_;
    if (abs(left_vel) < 0.03) { left_vel = 0.0; }
    if (abs(right_vel) < 0.03) { right_vel = 0.0; }
    set_state("left_wheel_joint/velocity", left_vel);
    set_state("right_wheel_joint/velocity", right_vel);	
    set_state("left_wheel_joint/position", left_pos);
    set_state("right_wheel_joint/position", right_pos);
    return hardware_interface::return_type::OK;
}

hardware_interface::return_type DiffbotHardwareInterface::write
    (const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
    driver_->setGoalVelocity(left_dnmxl_id_, get_command("left_wheel_joint/velocity"));
    driver_->setGoalVelocity(right_dnmxl_id_, -1.0 * get_command("right_wheel_joint/velocity"));
    return hardware_interface::return_type::OK;
}

} // namespace my_diffbot_hardware
PLUGINLIB_EXPORT_CLASS(my_diffbot_hardware::DiffbotHardwareInterface, hardware_interface::SystemInterface)
