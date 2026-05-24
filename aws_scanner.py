import boto3


def scan_ec2_instances(region="ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_instances()

    instances = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            name = "Unnamed"

            for tag in instance.get("Tags", []):
                if tag["Key"] == "Name":
                    name = tag["Value"]

            instances.append({
                "id": instance["InstanceId"],
                "name": name,
                "state": instance["State"]["Name"],
                "type": instance["InstanceType"],
                "cpu_usage": 5,
                "monthly_cost": 10
            })

    return instances


def scan_ebs_volumes(region="ap-south-1"):
    ec2 = boto3.client("ec2", region_name=region)
    response = ec2.describe_volumes()

    volumes = []

    for volume in response["Volumes"]:
        volumes.append({
            "id": volume["VolumeId"],
            "size": volume["Size"],
            "state": volume["State"],
            "monthly_cost": volume["Size"] * 0.1
        })

    return volumes


def scan_s3_buckets():
    s3 = boto3.client("s3")
    response = s3.list_buckets()

    buckets = []

    for bucket in response["Buckets"]:
        buckets.append({
            "name": bucket["Name"],
            "lifecycle_enabled": False,
            "monthly_cost": 5
        })

    return buckets