def analyze_ec2(instances):
    findings = []
    savings = 0

    for instance in instances:
        if instance["state"] == "running" and instance["cpu_usage"] < 10:
            findings.append({
                "resource": instance["id"],
                "type": "EC2 Instance",
                "issue": "Low CPU usage detected",
                "recommendation": "Consider stopping, resizing, or using a smaller instance type.",
                "priority": "High",
                "estimated_saving": instance["monthly_cost"] * 0.5
            })
            savings += instance["monthly_cost"] * 0.5

        elif instance["state"] == "stopped":
            findings.append({
                "resource": instance["id"],
                "type": "EC2 Instance",
                "issue": "Stopped instance found",
                "recommendation": "Check if this instance is still required. Delete if unused.",
                "priority": "Medium",
                "estimated_saving": 0
            })

    return findings, savings


def analyze_ebs(volumes):
    findings = []
    savings = 0

    for volume in volumes:
        if volume["state"] == "available":
            findings.append({
                "resource": volume["id"],
                "type": "EBS Volume",
                "issue": "Unattached EBS volume",
                "recommendation": "Delete this volume if it is no longer needed.",
                "priority": "High",
                "estimated_saving": volume["monthly_cost"]
            })
            savings += volume["monthly_cost"]

    return findings, savings


def analyze_s3(buckets):
    findings = []
    savings = 0

    for bucket in buckets:
        if not bucket["lifecycle_enabled"]:
            findings.append({
                "resource": bucket["name"],
                "type": "S3 Bucket",
                "issue": "Lifecycle policy not enabled",
                "recommendation": "Enable lifecycle rules to move old files to cheaper storage classes.",
                "priority": "Medium",
                "estimated_saving": bucket["monthly_cost"] * 0.3
            })
            savings += bucket["monthly_cost"] * 0.3

    return findings, savings


def generate_ai_summary(findings, total_savings):
    if not findings:
        return "Your cloud infrastructure looks optimized. No major cost issues were found."

    high_priority = [f for f in findings if f["priority"] == "High"]

    summary = f"""
CloudWise AI found {len(findings)} cost optimization opportunities.

Estimated monthly savings: ${round(total_savings, 2)}

Most important actions:
"""

    for item in high_priority:
        summary += f"""
- {item['resource']} has issue: {item['issue']}.
  Suggested action: {item['recommendation']}
"""

    summary += """
These recommendations can help reduce unnecessary AWS spending and improve cloud resource efficiency.
"""

    return summary