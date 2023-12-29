# Import necessary modules
from datetime import datetime, timedelta
import time

# Ask the user to input the targeted date and time
targetedDate = input("Enter your targeted date. (month/day/year - hour:minute:second)  (Jul/12/2023 - 5:32:54)\n")

# Parse the input into a datetime object using the specified format
date1 = datetime.strptime(targetedDate, "%b/%d/%Y - %H:%M:%S")

# Initialize snooze variable
snooze = 0

# Main loop to handle snoozing or stopping the countdown
while snooze != "t":

    # Display the time left until the targeted date and time
    while datetime.now() < date1:
        now = datetime.now()
        left = date1 - now
        print(left)
        time.sleep(1)
    
    # Ask the user if they want to stop or snooze
    snooze = input("Times up. Press 'T' to stop or press 'S' to snooze for 5 minutes.  ")
    
    # Convert the input to lowercase for case-insensitive comparison
    snooze = snooze.casefold()

    # If user chooses to snooze, add 5 minutes to the targeted date and continue the countdown
    if snooze == 's':
        date1 = date1 + timedelta(minutes=5)
