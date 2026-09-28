# Sensor-Aware Autonomous Car Simulation
# Simulates vehicle motion, distance sensing, sensor faults,
# fault detection, and safety braking.

import matplotlib.pyplot as plt 

# Simulation Parameters
position = 0
speed = 20
acceleration = 0
time_step = 1 

obstacle_position = 150
braking_acceleration = -4
fault_threshold = 30
safety_margin = 10


# Data Storage for Analysis and Plotting
positions = [0]
times = [0]
speeds = [speed]
sensor_readings = [obstacle_position - position]
true_distances = [obstacle_position - position]
previous_sensor_distance = obstacle_position - position 
stuck_count = 0

# Main Simulation Loop

for second in range(10):

    # Update vehicle motion 
    old_speed = speed
    speed = speed + acceleration * time_step
    average_speed = (old_speed + speed) / 2
    position = position + average_speed * time_step 
    distance_to_obstacle = obstacle_position - position

    # Simulate distance sensor
    sensor_distance = distance_to_obstacle
    expected_sensor_distance = previous_sensor_distance - speed * time_step

    # Optional fault injection for testing 
    # if 4 <= second <= 6:
    #    sensor_distance = 70

    # Detect abnormal sensor behaviour
    residual = abs(sensor_distance - expected_sensor_distance)

    if sensor_distance == previous_sensor_distance:
        stuck_count = stuck_count + 1
    else:
        stuck_count = 0

    if residual > fault_threshold or stuck_count >= 1:
        sensor_fault = True
        print("WARNING: Suspicious sensor measurement!")
    else:
        sensor_fault = False
        previous_sensor_distance = sensor_distance 

    # Safety controller
    stopping_distance = (speed ** 2) / (2 * abs(braking_acceleration))
    safe_stopping_distance = stopping_distance + safety_margin 

    if sensor_fault:
        acceleration = braking_acceleration
    elif sensor_distance <= safe_stopping_distance:
        acceleration = braking_acceleration 
    else:
        acceleration = 0

    speeds.append(speed)
    positions.append(position)
    times.append((second + 1) * time_step)
    sensor_readings.append(sensor_distance)
    true_distances.append(distance_to_obstacle)

    print("Time:", second + 1, 
          "s | True Distance:", distance_to_obstacle, 
          "m | Expected:", expected_sensor_distance,
          "m | Sensor:", sensor_distance,
          "m | Residual:", residual)

            
# Visualize Simulation Results

# Graph 1: Position vs Time
plt.plot(times, positions)

plt.xlabel("Time (seconds)")
plt.ylabel("Position (metres)")
plt.title("Vehicle Position Over Time")
plt.grid()
plt.savefig("results/vehicle_position.png")
plt.show()

# Graph 2: Speed vs Time
plt.plot(times, speeds)

plt.xlabel("Time (seconds)")
plt.ylabel("Speed (m/s)")
plt.title("Vehicle Speed Over Time")
plt.grid()
plt.savefig("results/vehicle_speed.png")
plt.show()

# Graph 3: True Distance vs Sensor Distance 
plt.plot(times, true_distances, label="True Distance", marker="o")
plt.plot(times, sensor_readings, label="Sensor Distance", marker="x")

plt.xlabel("Time (seconds)")
plt.ylabel("Distance (m)")
plt.title("True Distance vs Sensor Measurement")
plt.legend()
plt.grid()
plt.savefig("results/sensor_comparison.png")
plt.show()
