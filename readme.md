# 🚀 AWS EC2 Disaster Recovery Automation (Single Lambda Version)

This project demonstrates a **simple yet powerful Disaster Recovery automation** for EC2 using **AWS Lambda**, **EventBridge**, and **SNS**.

When the **primary EC2 instance stops or fails**, EventBridge automatically triggers a **Lambda function**, which:
- Launches a **new EC2** instance from your **AMI backup**
- Waits for it to start
- Sends a notification through **SNS**

---

## ⚙️ Architecture Overview

<img width="1024" height="1536" alt="architecture" src="https://github.com/user-attachments/assets/b81d16eb-8ac7-4c90-b75f-9e5952b0c8c9" />


**Flow:**
1. Primary EC2 is running your application.
2. EventBridge monitors EC2 state changes (stopped or terminated).
3. When EC2 stops, EventBridge triggers your Lambda.
4. Lambda launches a new EC2 from the AMI.
5. SNS sends an alert email with the result.

---

## 🧩 AWS Services Used

| Service | Purpose |
|----------|----------|
| **EC2** | Primary & Backup instances |
| **AMI** | Image backup of primary EC2 |
| **EventBridge** | Detects when primary EC2 stops |
| **Lambda** | Launches backup EC2 automatically |
| **SNS** | Sends email notifications |
| **CloudWatch Logs** | Stores Lambda execution logs |

---

## 🧠 Key Features

✅ Auto-detect EC2 stop or termination  
✅ Automatically launch backup EC2 from AMI  
✅ Sends success/failure alerts via SNS  
✅ Serverless – no need for servers running 24/7  
✅ Uses AWS native services only  

---

## 📂 Folder Structure
lambda/ → Lambda source code
cli-setup/ → CLI script to configure EventBridge
screenshots/ → Architecture & output screenshots
docs/ → Project report / explanation

---

## 🪜 Setup Steps

1️⃣ Create an IAM Role for Lambda
2️⃣ Create the Lambda Function
3️⃣ Create SNS Topic (for email alerts)
4️⃣ Create EventBridge Rule
---

## summary
| Failure Type   | Status                               |
| -------------- | ------------------------------------ |
| EC2 crash      | ✅ Auto recovery                      |
| EC2 stop       | ✅ Auto recovery                      |
| Region failure | ⚠️ Not covered (multi-region needed) |
| Email alert    | ✅ Sent via SNS                       |
| Automation     | ✅ 100% serverless                    |


---

## Flow
1. EventBridge watches for EC2 state change events.
2. When EC2 is stopped or terminated, EventBridge triggers a Lambda function.
3. Lambda:
   - Launches a new EC2 from AMI.
   - Waits for it to start.
   - Sends an SNS notification.

## Tools Used
- EC2
- Lambda
- EventBridge
- SNS
- CloudWatch Logs

## Testing
- Stop the primary EC2 using:
  ```bash
  aws ec2 stop-instances --instance-ids <INSTANCE_ID>

## Limitations
Handles instance-level recovery only.
Region-level failover requires replication to another AWS region.

## Future Improvements
Add multi-region replication (cross-region AMI + Route53 failover).
Attach Elastic IP to backup EC2.
Integrate Slack/Teams notifications.


