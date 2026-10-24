# Python AWS Static Website Deployment Using GitHub Actions

## 1. Project Overview

This project demonstrates how to deploy a static website to **Amazon S3 using GitHub Actions CI/CD**.

Whenever changes are pushed to the `main` branch of the GitHub repository, GitHub Actions automatically validates the Python script and uploads the website files to an existing S3 bucket.

The deployment authenticates to AWS using **OpenID Connect (OIDC)** and an IAM role instead of storing permanent AWS access keys in GitHub.

## 2. Project Objectives

- Create a simple static website using HTML.
- Store application code in GitHub.
- Automate deployment using GitHub Actions.
- Configure secure GitHub-to-AWS authentication using OIDC.
- Use AWS IAM policies to restrict S3 access.
- Deploy website files to Amazon S3.
- Understand the CI/CD workflow.

## 3. Architecture

```text
Developer
   |
   | Updates HTML / Python code
   v
GitHub Repository
   |
   | Push to main branch
   v
GitHub Actions Workflow
   |
   | 1. Checkout repository
   | 2. Set up Python
   | 3. Validate Python syntax
   | 4. Authenticate to AWS using OIDC
   | 5. Upload website files
   v
AWS IAM Role
   |
   | Temporary AWS credentials
   v
Amazon S3 Bucket
   |
   v
Static Website
```

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Script validation and AWS automation |
| HTML | Website content |
| Git | Version control |
| GitHub | Source code repository |
| GitHub Actions | CI/CD automation |
| AWS IAM | Access control and permissions |
| AWS OIDC | Secure authentication without long-term access keys |
| Amazon S3 | Static website file storage |
| AWS CLI | Uploading website files to S3 |

## 5. Project Structure

```text
python-demo-/
│
├── deploy.py
├── README.md
├── website/
│   └── index.html
│
└── .github/
    └── workflows/
        └── deploy.yml
```

### File descriptions

- `deploy.py`: Python script for AWS S3 website automation.
- `README.md`: Project documentation.
- `website/index.html`: Static website homepage.
- `.github/workflows/deploy.yml`: GitHub Actions CI/CD pipeline.

## 6. Prerequisites

Before starting, ensure you have:

- An AWS account.
- An existing S3 bucket.
- An AWS IAM OIDC identity provider for GitHub Actions.
- An IAM role with a GitHub OIDC trust policy.
- An IAM permissions policy allowing the required S3 operations.
- A GitHub repository.
- Git installed on your computer.

**Important:** This workflow uploads files to an existing S3 bucket. It does not create the bucket automatically.

## 7. Step 1: Create an S3 Bucket

1. Sign in to the AWS Management Console.
2. Open Amazon S3.
3. Create a bucket with a globally unique name.
4. Keep the bucket name for later configuration.
5. Enable static website hosting if you intend to use the direct S3 website endpoint.

Example bucket name:

```text
pooja-python-static-website
```

Replace this example with your actual bucket name.

For a public S3 website endpoint, S3 public-access settings and the bucket policy must also permit public reads. For production, prefer a private S3 bucket behind Amazon CloudFront.

## 8. Step 2: Create the GitHub OIDC Provider

GitHub Actions needs a trusted way to authenticate to AWS.

In the AWS Console:

1. Open **IAM → Identity providers**.
2. Choose **Add provider**.
3. Select **OpenID Connect**.
4. Enter the provider URL:

```text
https://token.actions.githubusercontent
