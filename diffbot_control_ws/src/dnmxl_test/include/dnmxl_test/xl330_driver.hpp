#pragma once

#include <cmath>
#include <stdexcept>
#include <string>
#include <iostream>
#include "rclcpp/rclcpp.hpp"

#include "dynamixel_sdk/dynamixel_sdk.h"

class XL330Driver
{
public:
    // Control table addresses (XL330, Protocol 2.0)
    static constexpr uint16_t ADDR_OPERATING_MODE  = 11;
    static constexpr uint16_t ADDR_TORQUE_ENABLE   = 64;
    static constexpr uint16_t ADDR_GOAL_VELOCITY   = 104;
    static constexpr uint16_t ADDR_GOAL_POSITION   = 116;
    static constexpr uint16_t ADDR_PRESENT_VELOCITY = 128;
    static constexpr uint16_t ADDR_PRESENT_POSITION = 132;

    // Operating modes
    static constexpr uint8_t MODE_VELOCITY = 1;
    static constexpr uint8_t MODE_POSITION = 3;

    // Unit conversions
    // Position: 4096 ticks / revolution → 0.088 deg/tick
    static constexpr double TICK_PER_RAD = 4096.0 / (2.0 * M_PI);
    static constexpr double RAD_PER_TICK = (2.0 * M_PI) / 4096.0;

    // Velocity: 0.229 RPM/unit  →  0.229 * 2π/60 rad/s per unit
    static constexpr double RAD_S_PER_UNIT = 0.229 * (2.0 * M_PI) / 60.0;
    static constexpr double UNIT_PER_RAD_S = 1.0 / RAD_S_PER_UNIT;

    static constexpr int   BAUDRATE         = 57600;
    static constexpr float PROTOCOL_VERSION = 2.0f;

    XL330Driver(const std::string& port_name)
        : port_name_(port_name),
          port_handler_(dynamixel::PortHandler::getPortHandler(port_name.c_str())),
          packet_handler_(dynamixel::PacketHandler::getPacketHandler(PROTOCOL_VERSION))
    {}

    int init()
    {
        std::cout << "Initializing connection with robot." << std::endl;
        if (!port_handler_->openPort()) {
            std::cout << "Failed to open the port!" << std::endl;
            return -1;
        }
        if (!port_handler_->setBaudRate(BAUDRATE)) {
            std::cout << "Failed to change the baudrate!" << std::endl;
            return -1;
        }
        return 0;
    }

    // Operating mode must be changed with torque off; these methods handle that sequence.
    void activatePositionMode(int dnmxl_id)
    {
        writeByte(dnmxl_id, ADDR_TORQUE_ENABLE, 0);
        writeByte(dnmxl_id, ADDR_OPERATING_MODE, MODE_POSITION);
        writeByte(dnmxl_id, ADDR_TORQUE_ENABLE, 1);
    }

    void activateVelocityMode(int dnmxl_id)
    {
        writeByte(dnmxl_id, ADDR_TORQUE_ENABLE, 0);
        writeByte(dnmxl_id, ADDR_OPERATING_MODE, MODE_VELOCITY);
        writeByte(dnmxl_id, ADDR_TORQUE_ENABLE, 1);
    }

    void deactivate(int dnmxl_id)
    {
        writeByte(dnmxl_id, ADDR_TORQUE_ENABLE, 0);
    }

    void setGoalPosition(int dnmxl_id, double radians)
    {
        auto ticks = static_cast<int32_t>(radians * TICK_PER_RAD);
        write4Byte(dnmxl_id, ADDR_GOAL_POSITION, static_cast<uint32_t>(ticks));
    }

    void setGoalVelocity(int dnmxl_id, double rad_per_sec)
    {
        auto units = static_cast<int32_t>(rad_per_sec * UNIT_PER_RAD_S);
        write4Byte(dnmxl_id, ADDR_GOAL_VELOCITY, static_cast<uint32_t>(units));
    }

    double getPosition(int dnmxl_id)
    {
        auto ticks = static_cast<int32_t>(read4Byte(dnmxl_id, ADDR_PRESENT_POSITION));
        return ticks * RAD_PER_TICK;
    }

    double getVelocity(int dnmxl_id)
    {
        auto units = static_cast<int32_t>(read4Byte(dnmxl_id, ADDR_PRESENT_VELOCITY));
        return units * RAD_S_PER_UNIT;
    }

private:
    std::string                port_name_;
    dynamixel::PortHandler *   port_handler_;
    dynamixel::PacketHandler * packet_handler_;

    void writeByte(int id, uint16_t address, uint8_t value)
    {
        uint8_t err = 0;
        int rc = packet_handler_->write1ByteTxRx(port_handler_, id, address, value, &err);
        checkComm(rc, err, id, address);
    }

    void write4Byte(int id, uint16_t address, uint32_t value)
    {
        uint8_t err = 0;
        int rc = packet_handler_->write4ByteTxRx(port_handler_, id, address, value);
        checkComm(rc, err, id, address);
    }

    uint32_t read4Byte(int id, uint16_t address)
    {
        uint8_t  err   = 0;
        uint32_t value = 0;
        int rc = packet_handler_->read4ByteTxRx(port_handler_, id, address, &value, &err);
        checkComm(rc, err, id, address);
        return value;
    }

    void checkComm(int rc, uint8_t err, int id, uint16_t address)
    {
        if (rc != COMM_SUCCESS) {
            throw std::runtime_error(
                "Comm error on dnmxl " + std::to_string(id) +
                " addr " + std::to_string(address) + ": " +
                packet_handler_->getTxRxResult(rc));
        }
        if (err != 0) {
            throw std::runtime_error(
                "Packet error on dnmxl " + std::to_string(id) +
                ": " + packet_handler_->getRxPacketError(err));
        }
    }
};
