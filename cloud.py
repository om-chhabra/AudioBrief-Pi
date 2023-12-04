import requests
import json
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
short_pin = 27
medium_pin = 22
large_pin = 5
GPIO.setup(short_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(medium_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(large_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def summary_length_options():
    print("Select summary length:")
    print("1: Short")
    print("2: Medium")
    print("3: Large")

    try:
        print("Press Ctrl+C to exit")
        while True:
            if GPIO.input(short_pin) == GPIO.LOW:
                print("Short Summary Chosen")
                return (30, 75)
            elif GPIO.input(medium_pin) == GPIO.LOW:
                print("Medium Summary Chosen")
                return (76, 150)
            elif GPIO.input(large_pin) == GPIO.LOW:
                print("Large Summary Chosen")
                return (151, 300)
            time.sleep(0.1) 
    except KeyboardInterrupt:
        print("Exiting...choosing default option")
        return (76, 150)
    finally:
        # Cleanup GPIO on exit
        GPIO.cleanup()

def cloud_function(cloud_function_url, input_file_path, output_file_path, min_length, max_length):
    print("Processing in Cloud... ")
    # Read the content of the input file
    with open(input_file_path, 'r') as file:
        input_text = file.read()

    # Create a payload with the input text and parameters
    payload = {
        'input_text': input_text,
        'min_length': min_length,
        'max_length': max_length
    }

    # Make a POST request to the Cloud Function
    response = requests.post(cloud_function_url, json=payload)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        response_data = json.loads(response.text)

        # Extract information from the response
        summarized_text = response_data.get("Summarized Text", "")
        confidence_score = response_data.get("Average Confidence Score", "")  # Assuming the key is "Confidence Score"
        reduction_percentage = response_data.get("Reduction in word count", "")  # Assuming the key is "Reduction Percentage"

        # Save the extracted information in the desired format
        with open(output_file_path, "w") as output_file:
            output_file.write("Summarized Text:\n")
            output_file.write(f"{summarized_text}\n\n")
            output_file.write(f"Average Confidence Score: {confidence_score:}%\n")
            output_file.write(f"Reduction in word count: {reduction_percentage:}%")
        
        print(f"Summary saved to {output_file_path}")

    else:
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    input_file = "./transcribes/26-11-2023_17-37_transcription.txt"  # Replace with your transcription file path
    output_file = "./summaries/summary.txt"
    url = "" 
    cloud_function(url, input_file, output_file)
