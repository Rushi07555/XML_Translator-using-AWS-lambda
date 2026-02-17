# 🌍 AWS Lambda XML Translation Service

This project implements an AWS Lambda--based automated XML translation
pipeline using:

-   Amazon S3 (file storage & trigger)
-   AWS Lambda (processing)
-   Amazon Translate (text translation)
-   Python (boto3, XML parsing)

------------------------------------------------------------------------

## 📌 Architecture Overview

Flow:

1.  XML file uploaded to Source S3 Bucket
2.  S3 triggers AWS Lambda
3.  Lambda:
    -   Reads XML file
    -   Extracts `<source>`{=html} text
    -   Calls Amazon Translate
    -   Updates `<TranslatedText>`{=html} node
4.  Translated files saved to Output S3 Bucket
5.  Original file deleted (optional)

------------------------------------------------------------------------

## 📂 Project Structure

. ├── lambda_function.py ├── requirements.txt └── README.md

------------------------------------------------------------------------

## 🧾 Supported Languages

  Language                Code
  ----------------------- -------
  Chinese (Simplified)    zh
  French                  fr
  German                  de
  Korean                  ko
  Polish                  pl
  Portuguese (Portugal)   pt-PT
  Spanish                 es
  Thai                    th

------------------------------------------------------------------------

## 🛠 AWS Services Used

-   Amazon Web Services (AWS)
-   Amazon S3
-   AWS Lambda
-   Amazon Translate

------------------------------------------------------------------------

## ⚙️ Setup Instructions

### 1️⃣ Create S3 Buckets

-   Source bucket (upload XML files)
-   Output bucket (store translated files)

Example: source-bucket-name global-gage-translator

------------------------------------------------------------------------

### 2️⃣ Create IAM Role for Lambda

Attach policies:

-   AmazonS3FullAccess (or restricted custom policy)
-   TranslateFullAccess
-   AWSLambdaBasicExecutionRole

Recommended: Use least-privilege custom IAM policy in production.

------------------------------------------------------------------------

### 3️⃣ Create Lambda Function

Runtime: Python 3.10+

Handler: lambda_function.lambda_handler

Memory: 512 MB recommended

Timeout: 1--3 minutes

------------------------------------------------------------------------

### 4️⃣ Configure S3 Trigger

-   Add Trigger → S3
-   Select source bucket
-   Event type: PUT

------------------------------------------------------------------------

## 📄 Supported XML Format (XLIFF)

Example:

`<xliff version="1.0">`{=html}
`<file source-language="en" TranslatedText-language="en">`{=html}
```{=html}
<body>
```
`<trans-unit>`{=html} `<source>`{=html}Home`</source>`{=html}
`<TranslatedText>`{=html}Casa`</TranslatedText>`{=html}
`</trans-unit>`{=html}
```{=html}
</body>
```
`</file>`{=html} `</xliff>`{=html}

------------------------------------------------------------------------

## 🔄 How Translation Works

For each `<trans-unit>`{=html}:

1.  Read `<source>`{=html}
2.  Send text to Amazon Translate
3.  Replace `<TranslatedText>`{=html}
4.  Update TranslatedText-language attribute
5.  Save new XML to output bucket

Parallel processing is handled using ThreadPoolExecutor.

------------------------------------------------------------------------

## 📦 Output File Naming

output/translated\_`<Language>`{=html}\_`<original_filename>`{=html}.xml

Example: output/translated_French_f10025.xml

------------------------------------------------------------------------

## 💰 Cost Considerations

Amazon Translate: Charged per character\
AWS Lambda: Charged per execution time & memory\
Amazon S3: Charged per storage & requests

------------------------------------------------------------------------

## ⚠️ Limitations

-   5000 bytes per translation request
-   Large XML files may require batching
-   No retry logic implemented

------------------------------------------------------------------------

## 🏁 Summary

This project provides a fully serverless multilingual XML translation
system using AWS services.

✔ Event-driven\
✔ Scalable\
✔ Parallel processing\
✔ Automated workflow
