---
layout: default
published: true
title: Terraform Scanning
nav_order: 8
---

# Terraform Plan and External Terraform Module Scanning

## Evaluate Checkov Policies on Terraform Plan
Checkov supports the evaluation of policies on resources declared in `.tf` files. It can also be used to evaluate `terraform plan` expressed in a json file. Plan evaluation provides Checkov additional dependencies and context that can result in a more complete scan result. Since Terraform plan files may contain arguments (like secrets) that are injected dynamically, it is advised to run a plan evaluation using Checkov in a secure CI/CD pipeline setting.

### Example

```json
terraform init
terraform plan --out tfplan.binary
terraform show -json tfplan.binary > tfplan.json

checkov -f tfplan.json
```

Note: The Terraform show output file `tf.json` will be a single line. For that reason Checkov will report all findings as line number 0.
If you have installed jq, you can convert a JSON file into multiple lines making it easier to read the scan result.

```json
terraform show -json tfplan.binary | jq '.' > tfplan.json

checkov -f tfplan.json
```

The output would look like:
```
checkov -f tf.json
Check: CKV_AWS_21: "Ensure all data stored in the S3 bucket have versioning enabled"
	FAILED for resource: aws_s3_bucket.customer
	File: /tf/tf1.json:224-268
	Guide: https://docs.bridgecrew.io/docs/s3_16-enable-versioning

		225 |               "values": {
		226 |                 "acceleration_status": "",
		227 |                 "acl": "private",
		228 |                 "arn": "arn:aws:s3:::mybucket",
```

## Scanning Third-Party Terraform Modules
Third-party Terraform modules often reduce complexity for deploying services made up of many objects.

For example, the third-party EKS module by howdio reduces the terraform required to the nine lines below, however, in doing so abstracts the terraform configuration away from a regular Checkov scan on the current directory.

```python
module "eks" {
  source = "howdio/eks/aws"

  name        = "examplecluster"
  default_vpc = true

  enable_kubectl   = true
  enable_dashboard = true
}
```

To ensure coverage of objects within these modules, you can instruct Checkov to scan the `.terraform` directory, after a `terraform init`, which will have retrieved the third-party modules and any associated `.tf` files:

```python
terraform init
checkov -d . # Your TF files.
checkov -d .terraform # Module TF files.
```

![](terraform-module-scanning)

It is worth noting however, that when scanning the `.terraform` directory, Checkov cannot differentiate between third-party and internally written modules. That said, you will benefit from scanning coverage across all of them.
