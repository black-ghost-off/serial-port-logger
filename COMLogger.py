import os
import serial
import csv
import argparse
from datetime import datetime

def parse_arguments():
    parser = argparse.ArgumentParser(description="Serial Port Logger")
    parser.add_argument('--virt', required=True, help='Virtual COM port (e.g., COM7)')
    parser.add_argument('--real', required=True, help='Real COM port (e.g., COM8)')
    parser.add_argument('--baud', type=int, default=115200, help='Baud rate (default: 115200)')
    parser.add_argument('--mode', choices=['ascii', 'hex', 'bin'], default='ascii', help='Logging mode (default: ascii)')
    return parser.parse_args()

def format_data(data, format_type):
    if format_type == 'ascii':
        return ' '.join(format(byte, '02x') for byte in data)
    elif format_type == 'hex':
        return data.hex()
    elif format_type == 'bin':
        return ' '.join(format(byte, '08b') for byte in data)
    else:
        return data.decode('ascii', errors='replace')

def main():
    args = parse_arguments()

    log_folder = 'logs'
    os.makedirs(log_folder, exist_ok=True)

    start_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_filename = f"{start_time}.csv"

    virtual_ser = serial.Serial(args.input, args.baud)
    real_ser = serial.Serial(args.output, args.baud)

    log_file_path = os.path.join(log_folder, log_filename)
    log_file = open(log_file_path, mode='w', newline='', encoding='ascii')
    log_writer = csv.writer(log_file)

    log_writer.writerow(['Timestamp', 'Direction', 'Data'])

    try:
        while True:
            if virtual_ser.in_waiting > 0:
                data_from_virtual = virtual_ser.read(virtual_ser.in_waiting)
                real_ser.write(data_from_virtual)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                formatted_data = format_data(data_from_virtual, args.mode)
                log_writer.writerow([timestamp, 'Virtual to Real', formatted_data])
                log_file.flush()
            
            if real_ser.in_waiting > 0:
                data_from_real = real_ser.read(real_ser.in_waiting)
                virtual_ser.write(data_from_real)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                formatted_data = format_data(data_from_real, args.mode)
                log_writer.writerow([timestamp, 'Real to Virtual', formatted_data])
                log_file.flush()

    except KeyboardInterrupt:
        end_time = datetime.now().strftime('%Y%m%d_%H%M%S')
        new_log_filename = f"{start_time}_{end_time}.csv"
        new_log_file_path = os.path.join(log_folder, new_log_filename)
        os.rename(log_file_path, new_log_file_path)

        virtual_ser.close()
        real_ser.close()
        log_file.close()

if __name__ == "__main__":
    main()
