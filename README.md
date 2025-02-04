# Serial Port Logger

This Python script logs data transmitted between a virtual COM port and a real COM port. It supports logging data in ASCII, hex, or binary formats and saves the logs as CSV files.

## Requirements

- Python 3
- `pyserial` library

## Installation

Install the `pyserial` library:
   ```sh
   pip install pyserial
   ```

## Usage
#### Arguments
* --virt: Virtual COM port (e.g., COM7) [required]
* --real: Real COM port (e.g., COM8) [required]
* --baud: Baud rate (default: 115200)
* --mode: Logging mode (default: ascii). Choices: ascii, hex, bin

## Running the Script
``` sh
python serial_logger.py --virt COM7 --real COM8 --baud 115200 --mode ascii
```

## How It Works
The script opens two serial ports, one virtual and one real, and logs the data transmitted between them in the specified format. The logs are saved in a subfolder named logs with filenames indicating the start and end times of the logging session.

### Format Data
* ascii: Logs data as ASCII characters.
* hex: Logs data as hexadecimal values.
* bin: Logs data as binary values.
### Log File
Log files are created in the logs folder with a filename format of start_time_end_time.csv.

Example Log Entry
Each log entry includes a timestamp, the direction of the data flow, and the formatted data.

``` csv
Timestamp, Direction, Data
2023-01-01 00:00:00, Virtual to Real, 48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21
2023-01-01 00:00:01, Real to Virtual, 41 43 4b 3a 20 48 65 6c 6c 6f 2c 20 57 6f 72 6c 64 21
```