import boto3,pendulum,csv,sys
from botocore import UNSIGNED
from botocore.client import Config
from pathlib import Path
from base64 import b64decode

s3 = boto3.client('s3',config=Config(signature_version=UNSIGNED))
bucket = "noaa-nexrad-level2"
directory = Path(__file__).resolve().parent

def puller(dt,station):
    d = dt.in_tz("UTC")
    fill = lambda x: str(x).zfill(2)
    pth = f"{d.year}/{fill(d.month)}/{fill(d.day)}/{station}/"
    print(pth)
    return s3.list_objects(Bucket=bucket,Delimiter="/",Prefix=pth)["Contents"]

def download(key,b64):
    fname = key.split("/")[-1]+"-"+b64
    print(key,bucket)
    if not (directory / "radars" / fname).exists() and not ("MDM" in fname):
        s3.download_file(bucket,key,str(directory / "radars" / fname))
    else:
        print("File already downloaded, skipping...")

def interp_key(key):
    #2019/10/02/KVBX/KVBX20191002_000604_V06
    obj = key.split("/")
    #[2019,10,02,KVBX,KVBX20191002_000604_V06]
    #print(obj)
    ns = obj[-1].split("_")
    t = ns[1] #time section
    time = [int(t[:2]),int(t[2:4]),int(t[4:])]
    date = [int(x) for x in obj[:3]]
    #print(time,date)
    return to_time({
        "year": date[0],
        "month": date[1],
        "day": date[2],
        "hours": time[0],
        "minutes": time[1],
        "seconds": time[2],
        "timezone": "UTC"
    })

def to_time(obj):
    """
    {
        "year": 2019,
        "month": 10,
        "day": 2,
        "hours": 18,
        "minutes": 6,
        "seconds" 2,
        "timezone": "America/Los_Angeles"
    }
    """
    y = obj["year"]
    mo = obj["month"]
    d = obj["day"]
    h = obj["hours"]
    m = obj["minutes"]
    s = obj["seconds"]
    tz = obj["timezone"]
    return pendulum.datetime(y,mo,d,h,m,s,tz=tz)

def match_time(has,goal,debug=False):
    #has will be UTC
    #goal will be ${goal.timezone}
    if debug: print(has,goal)
    gutc = goal.in_tz("UTC")
    if debug: print(has,gutc)
    if has.diff(gutc).in_hours() != 0:
        return False
    if has.diff(gutc).in_minutes() < 15:
        return True
    if debug: print(has.diff(gutc).in_minutes())
    return False

def s3_to_csv(data):
    with open("s3","w+") as f:
        writer = csv.writer(f)
        for key in data:
            writer.writerow((key["Key"],))

def iter_tester(goal):
    with open("s3","r") as f:
        reader = csv.reader(f)
        for key in reader:
            has = interp_key(key[0])
            matched = match_time(has,goal)
            if matched: print(has,goal)

def iter_real(goal,b64):
    data = puller(goal,sys.argv[1])
    for obj in data:
        #print(obj["Key"])
        has = interp_key(obj["Key"])
        if match_time(has,goal):
            download(obj["Key"],b64)

if __name__ == "__main__":
    #key = "2019/10/02/KVBX/KVBX20191002_000604_V06"
    #data = puller("2019","10","02","KVBX")
    #s3_to_csv(data)
    #has = interp_key(key)
    #has = pendulum.datetime(2019,10,2,0,6,4,tz="UTC")
    """goal = pendulum.datetime(2019,10,2,18,34,00,tz="America/Los_Angeles")
    print("should return false: ",match_time(has,goal,debug=True))
    g = pendulum.datetime(2019,10,1,17,10,00,tz="America/Los_Angeles")
    print("should return true: ",match_time(has,g,debug=True))
    go = pendulum.datetime(2019,10,1,17,30,00,tz="America/Los_Angeles")
    print("should return false: ",match_time(has,go,debug=True))
    guu = pendulum.datetime(2019,10,1,17,20,00,tz="America/Los_Angeles")
    print("should return true: ",match_time(has,guu,debug=True))"""
    #goal = pendulum.datetime(2019,10,2,1,13,00,tz="America/Los_Angeles")
    #iter_tester(goal)
    y,mo,d,h,m = [int(x) for x in (b64decode(sys.argv[2]).split(b" "))]
    goal = pendulum.datetime(y,mo,d,h,m,0,tz="America/Los_Angeles")
    iter_real(goal,sys.argv[2])
