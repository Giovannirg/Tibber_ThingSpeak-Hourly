# Tibber_ThingSpeak-Hourly
Small PYTHON script to connect to the tibber API and fetch and forward data to be shown on ThingSpeak.

Run on a Raspeberry PI and set a cronjob to run everyhour + 10 minutes to make sure the hourly data is already available in the tibber API:

 bash CMD:
crontab -e

 and add this line to the bottom of the file: 

10 * * * * /usr/bin/python3 /home/YOUR_PATH_TO_FILE/... 

An additional .m file was added to have a better visualisation of the data on matLab or on thingSpeak:

https://thingspeak.mathworks.com
