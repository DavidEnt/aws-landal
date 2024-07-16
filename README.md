# Landal scraper

This repository contains the code and resources needed to deploy and run Selenium using AWS Lambda. It scrapes the availability of a accomodation on Landal.   

## How it works
1. A weekly event provides a trigger 
2. A lambda function, based on a Docker container, scrapes
3. The output is send to an SQS queue, to be send via an email. 

## Requirements
Before getting started, ensure you have the following:
- AWS account
- AWS CLI configured with appropriate permissions
- Docker installed locally
- Node.js and npm installed
- GitHub account (for using GitHub Actions)
- A deployed lambda function to send emails. (i.e. the aws-emailer repo)

## Getting Started
1. **Clone the repository**
2. **Set up Environment variables**: Set `AWS_ACCOUNT_ID` and `AWS_REGION` in your GitHub repository secrets. These are required for assuming the role to deploy resources in your AWS account.
3. **Deploy the Infrastructure**: By pushing to the main branch the GitHub actions will be deploy the application, if and only if, all required environment varbiables have been set.

## Test Locally
1. **Build the dockerfile**
``` PowerShell
docker build --platform linux/amd64 -t docker-image:test . 
```
2. **Start the docker image**
``` PowerShell
docker run --platform linux/amd64 -p 9000:8080 docker-image:test
```
3. **Post an event to the local endpoint** from a new terminal window
``` PowerShell
Invoke-WebRequest -Uri "http://localhost:9000/2015-03-31/functions/function/invocations" -Method Post -Body '{}' -ContentType "application/json"
```

## Inspiration

- https://docs.aws.amazon.com/lambda/latest/dg/python-image.html
- https://medium.com/@kroeze.wb/running-selenium-in-aws-lambda-806c7e88ec64
- https://www.youtube.com/watch?v=wbsbXfkv47A&ab_channel=pixegami