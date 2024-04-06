# Script interacts with the AlienVault Open Threat Exchange (OTX) API to 
# retrieve indicators associated with a specified pulse ID. 
# It then exports these indicators to both a CSV file and a YARA rule file.
# Both files will be basic output don't expect much from this (sincerely Yetkin) 

import requests
import csv
import yara

# Function to retrieve indicators associated with a pulse from OTX API
def get_pulse_indicators(api_key, pulse_id):
    url = f"https://otx.alienvault.com/api/v1/pulses/{pulse_id}"
    headers = {"X-OTX-API-KEY": api_key}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for any error status codes
        pulse_info = response.json()  # Convert response to JSON
        return pulse_info.get("indicators", [])  # Return indicators if present, otherwise return an empty list
    except requests.exceptions.RequestException as e:
        print(f"Error retrieving pulse indicators: {e}")
        return []

# Function to export pulse indicators to a CSV file
def export_to_csv(indicators, file_path):
    if not indicators:
        print("No indicators to export.")
        return
    
    # Define CSV field names and data
    field_names = ["Type", "Indicator"]
    data = [[indicator["type"], indicator["indicator"]] for indicator in indicators]

    # Write data to CSV file
    with open(file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(field_names)
        writer.writerows(data)

    print(f"Pulse indicators exported to '{file_path}' successfully.")

# Function to generate YARA rule from pulse indicators
def generate_yara_rule(indicators, file_path):
    if not indicators:
        print("No indicators to generate YARA rule.")
        return
    
    # YARA rule template
    rule_text = """
rule PulseIndicators
{
    strings:
%s
    condition:
        any of them
}
""" % "".join('$s%d = "%s" ascii nocase\n' % (i, indicator['indicator']) for i, indicator in enumerate(indicators, start=1))

    # Compile YARA rule
    try:
        rules = yara.compile(source=rule_text)
    except yara.SyntaxError as e:
        print(f"Error compiling YARA rule: {e}")
        return

    # Write YARA rule to file
    try:
        with open(file_path, "w") as rule_file:
            rule_file.write(rule_text)
        print(f"YARA rule generated and saved to '{file_path}' successfully.")
    except IOError as e:
        print(f"Error writing YARA rule to file: {e}")

# Main function
def main():
    # Replace 'YOUR_API_KEY' with your OTX API key
    api_key = 'YOUR_API_KEY'

    # Input pulse ID from the user
    pulse_id = input("Enter the ID of the pulse you want to export: ")

    # Retrieve pulse indicators from OTX API
    indicators = get_pulse_indicators(api_key, pulse_id)

    # Export pulse indicators to a CSV file
    export_to_csv(indicators, "pulse_indicators.csv")

    # Generate YARA rule from pulse indicators
    generate_yara_rule(indicators, "pulse_indicators.yar")

if __name__ == "__main__":
    main()
