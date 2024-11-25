from django.test import TestCase

# Create your tests here.
from datetime import datetime, timedelta, timezone 
import pytz 
  
# get the standard UTC time  
UTC = pytz.utc 
  
# it will get the time zone  
# of the specified location 
IST = pytz.timezone('Asia/Jakarta') 
  
# print the date and time in 
# standard format 
print("UTC in Default Format : ",  
      datetime.now(UTC)) 
  
print("IST in Default Format : ",  
      datetime.now(IST)) 
  
# print the date and time in  
# specified format 
datetime_utc = datetime.now(UTC) 
print("Date & Time in UTC : ", 
      datetime_utc.strftime('%Y:%m:%d %H:%M:%S %Z %z')) 
  
datetime_ist = datetime.now(IST) 
print("Date & Time in IST : ",  
      datetime_ist.strftime('%Y:%m:%d %H:%M:%S %Z %z')) 

jakarta_tz = pytz.timezone('Asia/Jakarta')
# print((datetime.now(jakarta_tz) + timedelta(hours=48)).strftime('%Y:%m:%d %H:%M:%S %Z %z'))

def get_expiry_time():
    jakarta_tz = pytz.timezone('Asia/Jakarta')
    return (datetime.now(jakarta_tz) + timedelta(hours=48)).strftime('%Y:%m:%d %H:%M:%S %Z %z')

print(get_expiry_time())