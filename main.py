import tls_client
import csv
import re
import os
import threading
import concurrent.futures
from bs4 import BeautifulSoup
from datetime import datetime
from rich.console import Console
from rich import print as rprint

console = Console()
lock = threading.Lock()

# Config for proxy
PROXY = "http://geo.iproyal.com:12321"

def process_phone_number(raw_phone_number):
    session = tls_client.Session(
        client_identifier="chrome_112",
        random_tls_extension_order=True
    )
    
    formatted_phone = f"({raw_phone_number[0:3]}) {raw_phone_number[3:6]}-{raw_phone_number[6:10]}"
    
    resp = session.get(f"https://www.zabasearch.com/phone/{raw_phone_number}", proxy=PROXY)
    soup = BeautifulSoup(resp.text, 'html.parser')
    
    name_element = soup.select_one("#result-top-content h3")
    full_name = name_element.text.strip() if name_element else None
    
    if not full_name or full_name == "":
        rprint(f"[red]Not Found -> {formatted_phone}[/red]")
        return None
    
    try:
        age_row = soup.select_one("tr.column-2")
        if age_row and age_row.find_next_sibling("tr"):
            age_cell = age_row.find_next_sibling("tr").find("td")
            age = age_cell.text.strip() if age_cell else None
        else:
            age = None
        
        if not age or age == "":
            age_element = soup.select_one("table tr td:first-child")
            age = age_element.text.strip() if age_element else None
        
        if not age or age == "":
            birth_year_element = soup.select_one("tr.column-2 + tr td:nth-child(2)")
            if birth_year_element:
                birth_year_text = birth_year_element.text.strip()
                if birth_year_text:
                    birth_year = ''.join(filter(str.isdigit, birth_year_text))
                    if birth_year:
                        current_year = datetime.now().year
                        age = str(current_year - int(birth_year))
    except Exception:
        age = None
    
    carrier_element = soup.select_one("tr:has(th:contains('Carrier')) td")
    carrier = carrier_element.text.strip() if carrier_element else None
    
    licenses_elements = soup.select("#phone-number-licenses ul li")
    professional_licenses = []
    for license_elem in licenses_elements:
        license_text = license_elem.text.strip()
        if "No" not in license_text and license_text not in professional_licenses:
            professional_licenses.append(license_text)
    
    licenses_str = "; ".join(professional_licenses) if professional_licenses else None
    
    location_element = soup.select_one("#phone-number-locations h5:contains('Most Recent') + ul li")
    most_recent_location = location_element.text.strip() if location_element else None
    
    if not most_recent_location:
        rprint(f"[yellow]Partial Data -> {formatted_phone} {full_name}[/yellow]")
        return None
    
    person_info = {
        "phone_number": formatted_phone,
        "full_name": full_name,
        "age": age,
        "carrier": carrier,
        "professional_licenses": licenses_str,
        "most_recent_location": most_recent_location
    }
    
    rprint(f"[green]Found -> {formatted_phone} {full_name} {most_recent_location}[/green]")
    
    with lock:
        write_to_csv(person_info)
    
    return person_info

def write_to_csv(person_info):
    csv_headers = [
        "Phone Number", 
        "Full Name", 
        "Age", 
        "Carrier", 
        "Professional Licenses", 
        "Most Recent Address"
    ]
    
    csv_row = [
        person_info["phone_number"],
        person_info["full_name"],
        person_info["age"] if person_info["age"] else "",
        person_info["carrier"] if person_info["carrier"] else "",
        person_info["professional_licenses"] if person_info["professional_licenses"] else "",
        person_info["most_recent_location"]
    ]
    
    csv_filename = "phone_lookup_results.csv"
    file_exists = os.path.isfile(csv_filename)
    
    try:
        with open(csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(csv_headers)
            writer.writerow(csv_row)
    except Exception as e:
        rprint(f"[red]Error saving to CSV: {e}[/red]")

def extract_phone_numbers(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    pattern = r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{10})'
    matches = re.findall(pattern, content)
    
    clean_numbers = []
    for match in matches:
        digits_only = re.sub(r'\D', '', match)
        if len(digits_only) == 10:
            clean_numbers.append(digits_only)
    
    return clean_numbers

def main():
    console.print("[bold blue]Phone Lookup Tool[/bold blue]")
    
    input_file = "input.txt"
    if not os.path.exists(input_file):
        console.print(f"[red]File not found: {input_file}[/red]")
        return
    
    phone_numbers = extract_phone_numbers(input_file)
    console.print(f"Extracted [bold]{len(phone_numbers)}[/bold] phone numbers from file")
    
    max_workers = min(10, len(phone_numbers))  # Limit to 10 threads max
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        console.print(f"Processing with [bold]{max_workers}[/bold] threads")
        with console.status("[bold green]Processing phone numbers...") as status:
            futures = {executor.submit(process_phone_number, num): num for num in phone_numbers}
            for future in concurrent.futures.as_completed(futures):
                phone_number = futures[future]
                try:
                    result = future.result()
                except Exception as e:
                    rprint(f"[red]Error processing {phone_number}: {e}[/red]")
    
    console.print("[bold green]Processing complete![/bold green]")

if __name__ == "__main__":
    main()