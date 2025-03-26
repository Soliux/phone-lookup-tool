# 🔍 ZabaSearch Tool

A powerful multi-threaded Python tool for bulk phone number lookups using [ZabaSearch](http://zabasearch.com). This tool automates the process of extracting information from ZabaSearch, providing detailed data about phone numbers including owner details, carrier information, and location data.

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

</div>

## ✨ Features

- 📱 Bulk phone number lookup from text file
- ⚡ Multi-threaded processing for improved performance
- 📊 Comprehensive information retrieval:
  - 👤 Full name
  - 📅 Age
  - 📡 Carrier information
  - 📜 Professional licenses
  - 📍 Most recent location
- 📁 CSV export of results
- 🎯 Real-time progress tracking with rich console output

## 🚀 Quick Start

### Prerequisites

- Python 3.6 or higher
- Required Python packages (see requirements.txt)
- IProyal proxy credentials

### Installation

1. Clone this repository:
```bash
git clone https://github.com/Soliux/ZabaSearch.git
cd ZabaSearch
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

## 📖 Usage

1. Create an `input.txt` file with phone numbers (one per line or in any format - the tool will extract valid 10-digit numbers)

2. Run the script:
```bash
python main.py
```

3. Results will be automatically saved to `phone_lookup_results.csv`

## 📝 Input Format

The tool is flexible and accepts phone numbers in various formats:

Format | Example
-------|--------
Plain | 1234567890
Dashed | 123-456-7890
Parentheses | (123) 456-7890
Dotted | 123.456.7890

## 📊 Output Format

Results are saved to a CSV file with the following columns:

Column | Description
-------|------------
Phone Number | Formatted phone number
Full Name | Owner's full name
Age | Age of the person
Carrier | Phone carrier information
Professional Licenses | Any professional licenses found
Most Recent Address | Last known location

## ⚙️ Configuration

The tool uses an IProyal proxy by default. To use a different proxy service, update the `PROXY` variable in `main.py`:

```python
PROXY = "your_proxy_here"
```

## ⚠️ Limitations

- 🔄 Maximum 10 concurrent threads to prevent overloading
- 🔑 Requires valid proxy configuration
- ⏱️ Rate limiting may apply based on the proxy service used

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚖️ Disclaimer

This tool is for educational purposes only. Users must ensure compliance with all applicable laws and terms of service when performing phone number lookups. The developers are not responsible for any misuse of this tool.