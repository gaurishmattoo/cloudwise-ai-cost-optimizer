import streamlit as st
import pandas as pd

from sample_data import sample_ec2_instances, sample_ebs_volumes, sample_s3_buckets
from optimizer import analyze_ec2, analyze_ebs, analyze_s3, generate_ai_summary

st.set_page_config(
    page_title="CloudWise AI",
    page_icon="☁️",
    layout="wide"
)

st.title("☁️ CloudWise AI")
st.subheader("AI-Powered Cloud Cost Optimization Agent for DevOps Teams")

st.write(
    "CloudWise AI scans cloud resources, detects cost wastage, "
    "and provides smart optimization recommendations."
)

st.sidebar.title("Settings")
mode = st.sidebar.radio("Select Mode", ["Demo Mode", "Live AWS Mode"])

if mode == "Demo Mode":
    ec2_instances = sample_ec2_instances
    ebs_volumes = sample_ebs_volumes
    s3_buckets = sample_s3_buckets
else:
    st.warning("Live AWS Mode requires AWS credentials configured using AWS CLI.")
    from aws_scanner import scan_ec2_instances, scan_ebs_volumes, scan_s3_buckets

    region = st.sidebar.text_input("AWS Region", "ap-south-1")

    try:
        ec2_instances = scan_ec2_instances(region)
        ebs_volumes = scan_ebs_volumes(region)
        s3_buckets = scan_s3_buckets()
    except Exception as e:
        st.error("Could not connect to AWS. Showing demo data instead.")
        st.error(e)
        ec2_instances = sample_ec2_instances
        ebs_volumes = sample_ebs_volumes
        s3_buckets = sample_s3_buckets

ec2_findings, ec2_savings = analyze_ec2(ec2_instances)
ebs_findings, ebs_savings = analyze_ebs(ebs_volumes)
s3_findings, s3_savings = analyze_s3(s3_buckets)

all_findings = ec2_findings + ebs_findings + s3_findings
total_savings = ec2_savings + ebs_savings + s3_savings

total_resources = len(ec2_instances) + len(ebs_volumes) + len(s3_buckets)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Resources Scanned", total_resources)

with col2:
    st.metric("Issues Found", len(all_findings))

with col3:
    st.metric("Estimated Monthly Savings", f"${round(total_savings, 2)}")

st.divider()

st.header("📊 Cloud Resources")

tab1, tab2, tab3 = st.tabs(["EC2 Instances", "EBS Volumes", "S3 Buckets"])

with tab1:
    st.dataframe(pd.DataFrame(ec2_instances), use_container_width=True)

with tab2:
    st.dataframe(pd.DataFrame(ebs_volumes), use_container_width=True)

with tab3:
    st.dataframe(pd.DataFrame(s3_buckets), use_container_width=True)

st.divider()

st.header("🚨 Optimization Findings")

if all_findings:
    findings_df = pd.DataFrame(all_findings)
    st.dataframe(findings_df, use_container_width=True)
else:
    st.success("No cost optimization issues found.")

st.divider()

st.header("🤖 AI Recommendation Summary")

summary = generate_ai_summary(all_findings, total_savings)
st.info(summary)

st.download_button(
    label="Download Optimization Report",
    data=summary,
    file_name="cloudwise_ai_report.txt",
    mime="text/plain"
)

st.divider()

st.header("✅ Final Suggested Actions")

for finding in all_findings:
    with st.expander(f"{finding['priority']} Priority - {finding['resource']}"):
        st.write(f"**Resource Type:** {finding['type']}")
        st.write(f"**Issue:** {finding['issue']}")
        st.write(f"**Recommendation:** {finding['recommendation']}")
        st.write(f"**Estimated Saving:** ${round(finding['estimated_saving'], 2)} per month")