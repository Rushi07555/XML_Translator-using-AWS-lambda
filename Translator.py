import boto3
import xml.etree.ElementTree as ET
from io import StringIO
import urllib.parse
from concurrent.futures import ThreadPoolExecutor

s3 = boto3.client('s3')

language_mapping = {
    "Chinese (Simplified)": "zh",
    "French": "fr",
    "German": "de",
    "Korean": "ko",
    "Polish": "pl",
    "Portuguese (Portugal)": "pt-PT",
    "Spanish": "es",
    "Thai": "th"
}

def translate_text(text, target_language_code):
    # Create a Boto3 client for the AWS Translate service
    translate_client = boto3.client('translate')
    try:
        # Translate the text using AWS Translate
        response = translate_client.translate_text(
            Text=text,
            SourceLanguageCode='en',  # Automatically detect source language
            TargetLanguageCode=target_language_code
        )
        return response['TranslatedText']
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        return None

def translate_and_store(language, language_code, content, output_bucket_name, output_key):
    try:
        # Parse the XML content
        tree = ET.parse(StringIO(content))
        root = tree.getroot()
        
        # Update target-language attribute
        file_element = root.find('file')
        file_element.set('target-language', language_code)
        
        # Iterate through <trans-unit> elements
        for trans_unit in root.findall('.//trans-unit'):
            # Extract target text
            target_element = trans_unit.find('target')
            if target_element is not None:
                target_text = target_element.text

                # Translate the target text to the specified language
                translated_text = translate_text(target_text, language_code)

                # Update the target text with the translated result
                target_element.text = translated_text

        # Convert the modified XML tree back to a string
        modified_xml_content = ET.tostring(root, encoding='utf-8').decode('utf-8')

        # Store the translated content in the output bucket
        s3.put_object(Bucket=output_bucket_name, Key=output_key, Body=modified_xml_content.encode('utf-8'))
        print(f'Translated XML content successfully for {language} ({language_code})')
    except Exception as e:
        print(f'Failed to translate XML content for {language} ({language_code}): {e}')

def lambda_handler(event, context):
    try:
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

        # Get the object
        obj = s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')

        output_bucket_name = 'global-gage-translator'

        with ThreadPoolExecutor(max_workers=len(language_mapping)) as executor:
            futures = []
            for language, language_code in language_mapping.items():
                output_key = f"output/translated_{language}_{key.split('/')[-1][:-4]}.xml"
                futures.append(executor.submit(translate_and_store, language, language_code, content, output_bucket_name, output_key))

            # Wait for all futures to complete
            for future in futures:
                future.result()

        # Delete the original file from S3
        s3.delete_object(Bucket=bucket, Key=key)

        return {
            'statusCode': 200,
            'body': 'Translation complete!'
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': 'Error occurred during translation'
        }
