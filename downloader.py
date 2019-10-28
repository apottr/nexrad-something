import boto3
from botocore import UNSIGNED
from botocore.client import Config


def puller(year,month,day,station):
    s3 = boto3.client('s3', config=Config(signature_version=UNSIGNED))

    buck = "noaa-nexrad-level2"
    pth = f"{year}/{month}/{day}/{station}/"
    return s3.list_objects(Bucket=buck,Delimiter="/",Prefix=pth)

def interp_key(key):
    to_time = lambda x: [x[:2],x[2:4],x[4:]]
    name = key.split("/")[-1]
    print(name)
    t = name.split("_")[1]
    return to_time(t)

def match_time(has,goal,timezone):
    #has will be UTC
    #goal will be ${timezone}
    
    utc = goal.to("utc")
    if()
    

if __name__ == "__main__":
    key = "2019/10/02/KVBX/KVBX20191002_000604_V06"
    #data = puller("2019","10","02","KVBX")
    #print(data["Contents"][0])
    interp_key(key)