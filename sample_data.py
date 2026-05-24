sample_ec2_instances = [
    {
        "id": "i-0123456789",
        "name": "dev-server",
        "state": "running",
        "type": "t2.micro",
        "cpu_usage": 4,
        "monthly_cost": 8
    },
    {
        "id": "i-9876543210",
        "name": "test-server",
        "state": "stopped",
        "type": "t3.medium",
        "cpu_usage": 0,
        "monthly_cost": 0
    },
    {
        "id": "i-5555555555",
        "name": "old-backend",
        "state": "running",
        "type": "t3.large",
        "cpu_usage": 7,
        "monthly_cost": 60
    }
]

sample_ebs_volumes = [
    {
        "id": "vol-111",
        "size": 30,
        "state": "available",
        "monthly_cost": 3
    },
    {
        "id": "vol-222",
        "size": 100,
        "state": "in-use",
        "monthly_cost": 10
    }
]

sample_s3_buckets = [
    {
        "name": "project-logs-bucket",
        "lifecycle_enabled": False,
        "monthly_cost": 5
    },
    {
        "name": "analytics-data-bucket",
        "lifecycle_enabled": True,
        "monthly_cost": 12
    }
]