import lirc
import time

# Initialize the LIRC client. The 'myprogram' is the name of your program
# as defined in an optional ~/.lircrc file (though not strictly needed for this basic example).
client = lirc.Client(remote="*", blocking=False) # Use blocking=False for non-blocking read

print("LIRC client started. Press buttons on your remote...")

try:
    while True:
        # Read a command from the LIRC daemon
        # The data format is usually a list like [remote_name, button_name, repitition_count, ... ]
        lirc_data = client.recv_config()

        if lirc_data:
            # lirc_data is a list of strings
            remote_name = lirc_data[0]
            button_name = lirc_data[1]
            print(f"Received button press: {button_name} from remote {remote_name}")

        # Small delay to prevent the loop from running too fast
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # It's a good practice to close the client connection
    client.close()
