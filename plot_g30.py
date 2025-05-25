import argparse
import pandas as pd
from rosbag2_py import SequentialReader, StorageOptions, ConverterOptions
from g30esli_interface_msgs.msg import StatusStamped
import rclpy.serialization as serialization

def parse_args():
    parser = argparse.ArgumentParser(description='Extract speed.actual from g30esli/status topic')
    parser.add_argument('bag_path', help='Path to the .db3 (ros2 bag)')
    return parser.parse_args()

def main():
    args = parse_args()
    bag_path = args.bag_path
    selected_topic = "/g30esli/status"

    storage_options = StorageOptions(uri=bag_path, storage_id='sqlite3')
    converter_options = ConverterOptions('', '')

    reader = SequentialReader()
    reader.open(storage_options, converter_options)

    data = {
        'timestamp': [],
        'speed_actual': [],
    }

    while reader.has_next():
        topic, msg_data, t = reader.read_next()
        if topic == selected_topic:
            msg = serialization.deserialize_message(msg_data, StatusStamped)
            timestamp = t * 1e-9  # convert nanoseconds to seconds
            data['timestamp'].append(timestamp)
            data['speed_actual'].append(msg.status.speed.actual)

    df = pd.DataFrame(data)
    df.set_index('timestamp', inplace=True)
    
    output_file = 'speed_actual.csv'
    df.to_csv(output_file)
    print(f"Saved speed.actual data to '{output_file}'")

if __name__ == '__main__':
    main()
