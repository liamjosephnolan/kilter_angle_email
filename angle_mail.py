import re 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import time 
from datetime import datetime 
from bs4 import BeautifulSoup
import os

# URL of the page to scrape
url = 'https://www.kletterzentrum-innsbruck.at/'
# Fetch the webpage content
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Print the HTML content of the page.
    html_content = response.text
    print("Content Fetched")
else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
    html_content = ""

# Create a BeautifulSoup object only if content was fetched
if html_content:
    website_soup = BeautifulSoup(html_content, 'html.parser')




# Search for a text that contains a number followed by the degree symbol (°)
    match = re.search(r'(\d+°)', website_soup.get_text())

# Extract the value (number with degree symbol)
    if match:
        kilter_angle = match.group(1)  # Extracts "40°"
        print("Kilter angle:", kilter_angle)
    else:
        print("Kilter angle not found.")





# Email and password for Gmail account
email = os.getenv('EMAIL')  # GitHub Actions will inject this secret
password = os.getenv('PASSWORD')

msg = MIMEMultipart('alternative')
now = datetime.now()
now_time = now.time()
now_time = now_time.strftime('%H:%M')
now = now.strftime('%Y-%m-%d %H:%M:%S')
msg['Subject'] = "Kilter Status @" + now 
msg['From'] = email
msg['To'] = 'liamjosephnolan@gmail.com'  # Replace with recipient email address

# Create the body of the message (a plain-text and an HTML version).
text = f"""Hello,

I just wanted to let you know that today at {now_time} the kilter is currently set to {kilter_angle} 

The kilter should really be set steeper! 50 Degrees would be really great!!

This email will send hourly until the angle is changed :)

Danke!

"""

# Record the MIME types of both parts - text/plain and text/html.
part1 = MIMEText(text, 'plain')

# Attach parts into message container.
msg.attach(part1)

if kilter_angle == "40°":
# Send the message via Gmail's SMTP server.
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(email, password)
        server.sendmail(email, msg['To'], msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Error: Unable to send email - ", e)
else:
    print("No need to spam, the kilter is steep today")
