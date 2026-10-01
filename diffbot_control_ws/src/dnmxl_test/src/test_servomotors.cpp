#include "rclcpp/rclcpp.hpp"
#include "dnmxl_test/xl330_driver.hpp"
#include <thread>

using namespace std::chrono_literals;

int main()
{
    int dnmxl_id_1 = 2;
    int dnmxl_id_2 = 4;

    auto driver = XL330Driver("/dev/ttyACM0");
    driver.init();

    // Velocity mode
    driver.activateVelocityMode(dnmxl_id_1);
    driver.activateVelocityMode(dnmxl_id_2);
    driver.setGoalVelocity(dnmxl_id_1, 2*M_PI);
    driver.setGoalVelocity(dnmxl_id_2, -M_PI);
    std::this_thread::sleep_for(3s);
    double velocity1 = driver.getVelocity(dnmxl_id_1);
    double velocity2 = driver.getVelocity(dnmxl_id_2);
    std::cout << "Velocity dnmxl_id_1 : " << velocity1 << std::endl;
    std::cout << "Velocity dnmxl_id_2 : " << velocity2 << std::endl;
    driver.deactivate(dnmxl_id_1);
    driver.deactivate(dnmxl_id_2);

    std::this_thread::sleep_for(3s);

    // Position mode
    driver.activatePositionMode(dnmxl_id_1);
    driver.activatePositionMode(dnmxl_id_2);
    driver.setGoalPosition(dnmxl_id_1, M_PI/2);
    driver.setGoalPosition(dnmxl_id_2, M_PI/2);
    std::this_thread::sleep_for(3s);
    double position1 = driver.getPosition(dnmxl_id_1);
    double position2 = driver.getPosition(dnmxl_id_2);
    std::cout << "Position dnmxl_id_1: " << position1 << std::endl;
    std::cout << "Position dnmxl_id_2: " << position2 << std::endl;
    driver.deactivate(dnmxl_id_1);
    driver.deactivate(dnmxl_id_2);

    return 0;
}
