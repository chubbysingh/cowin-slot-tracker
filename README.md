# Cowin-Slot-Tracker
Tracker to check the covid vaccine slot availability in India and send mobile notifications through Twilio Messaging Service.

## Requirements
Docker must be installed in the local system. Refer [docker documentation](https://docs.docker.com/engine/install/) to set it locally based on your machine specification.
If you are a Windows user and wants to setup docker, follow this [video](
https://youtu.be/_9AWYlt86B8)
## How to use?
There are two parts to this system
1. Pinging the public COWIN API to get district wise data and checking for availability, every 15 minutes.
2. Relaying this information to the user's mobile via Twilio Messaging Service. For that, one must configure Twilio
    1. Sign up on [Twilio](https://www.twilio.com/) using your email id. After verifying your email log into the Twilio Dashboard. For this purpose, we will remain on free trial.
    2. Once you are in the dashboard, click **Get a trial phone number**.
    3. Under Project Info, you can find the **ACCOUNT SID**, **AUTH TOKEN** and **PHONE NUMBER** (Twilio Phone Number and not yours). Make a note of these numbers.
4. After successfully completing above steps, you are good to go.

Once all the above requirements are met, do the following
1. Git clone this repository(if you are techie enough), otherwise download the repository by clicking on **Download ZIP** under **Code**.
   
2. Replace <SECRET_TOKEN>, <ACCOUNT_SID>, <TWILIO_PHONE_NUMBER> & <CELL_PHONE_NUMBER_1> in `covin_slot_tracker.py` in line 83-87
3. Open Terminal and change your directory to the folder you have just cloned/ downloaded. (Remember to extract the .zip file if you have downloaded it)
4. Make sure Docker Desktop is running. if not, install it.
5. Run `docker build -t covin --rm .`
6. Run `docker run -it --name covin-schedule --rm covin`
7. Run `python covin_slot_tracker.py <DISTRICT_ID> <AGE>`
      * e.g. `python covin_slot_tracker.py 188 24`
8. If there is a slot available in the district code you have provided, you will receive an SMS on your phone.

#### Example Usage and Response
```
python covin_slot_tracker.py 200 24

43 Slots Available at B.Khera SDH, Civil Hospital Bhiwani 1 for 04-05-2021

Here 200 is the district id for Bhiwani
```

#### Sample District Codes in Haryana
- 188: Gurgaon
- 192: Rohtak
- 200: Bhiwani

#### Other States
To find District ID for other states:

Got to [Cowin Portal](https://www.cowin.gov.in/home) in the browser
- Open Network tab in browser
- Search for vaccine availabilty in portal
- Check Network tab for requests
- Find district_id property value from the requests
