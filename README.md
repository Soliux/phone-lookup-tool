# Phone Lookup Tool

A multi-threaded Python tool that performs bulk phone number lookups using Zabasearch. The tool extracts phone numbers from an input file and retrieves detailed information about each number including the owner's name, age, carrier information, professional licenses, and most recent location.

## Features

- Bulk phone number lookup from text file
- Multi-threaded processing for improved performance
- Detailed information retrieval:
  - Full name
  - Age
  - Carrier information
  - Professional licenses
  - Most recent location
- CSV export of results
- Progress tracking with rich console output

## Requirements

- Python 3.6+
- Required Python packages (see requirements.txt)
- IProyal proxy credentials

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/phone-lookup-tool.git
cd phone-lookup-tool
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Create an input.txt file with phone numbers (one per line or in any format - the tool will extract valid 10-digit numbers)

2. Run the script:
```bash
python main.py
```

3. Results will be saved to `phone_lookup_results.csv`

## Input Format

The tool accepts phone numbers in various formats in the input.txt file:
- 1234567890
- 123-456-7890
- (123) 456-7890
- 123.456.7890

## Output Format

Results are saved to a CSV file with the following columns:
- Phone Number
- Full Name
- Age
- Carrier
- Professional Licenses
- Most Recent Address

## Configuration

The tool uses an IProyal proxy by default. Update the `PROXY` variable in `main.py` if you need to use a different proxy service.

## Limitations

- Maximum 10 concurrent threads to prevent overloading
- Requires valid proxy configuration
- Rate limiting may apply based on the proxy service used

## License

MIT License - see LICENSE file for details.

## Disclaimer

This tool is for educational purposes only. Ensure you comply with all applicable laws and terms of service when performing phone number lookups.