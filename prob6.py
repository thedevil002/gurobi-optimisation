from pysnmp.hlapi import *
import time
import matplotlib.pyplot as plt

# Previous data and time variables for calculating transfer rate
prev_data = 0
prev_time = time.perf_counter()  # Use a high precision timer

# SNMP OID for the network interface data
data_oid = ObjectType(ObjectIdentity('.1.3.6.1.2.1.2.2.1.10.34'))

# Initialize lists to store time stamps and data rates
time_stamps = []
data_rates = []

# Determine the duration for which data should be collected (in seconds)
monitoring_duration = 60  # For example, monitor for 60 seconds

start_time = time.perf_counter()

while True:
    current_time = time.perf_counter()

    # Check if the monitoring duration has been reached
    if current_time - start_time > monitoring_duration:
        break

    # Send SNMP GET request to retrieve the data
    g = getCmd(SnmpEngine(), CommunityData('com', mpModel=0),
               UdpTransportTarget(('127.0.0.1', 161)),
               ContextData(), data_oid)

    errorIndication, errorStatus, errorIndex, varBinds = next(g)

    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('Error status')
    else:
        current_data = int(varBinds[0][1])
        time_difference = current_time - prev_time

        # Ensure there's a non-zero time difference
        if time_difference > 0:
            data_rate = (current_data - prev_data) / time_difference
            print(f'Transfer Rate: {data_rate} units per second')

            # Update lists with the current timestamp and data rate
            time_stamps.append(current_time - start_time)
            data_rates.append(data_rate)

        # Update previous data and time for the next iteration
        prev_data = current_data
        prev_time = current_time

        # Save the transfer rate in the "debit.txt" file
        with open("debit.txt", "a+") as f:
            f.write(f"{data_rate}\n")

    time.sleep(1)  # Wait for one second before the next iteration

# Ensure there's at least one data rate to plot
if data_rates:
    # Plot the results
    plt.plot(time_stamps, data_rates)
    plt.xlabel('Time (seconds)')
    plt.ylabel('Data Rate (units per second)')
    plt.title('Network Interface Data Rate Over Time')
    plt.show()