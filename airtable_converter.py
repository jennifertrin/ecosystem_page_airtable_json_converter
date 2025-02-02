import os
import json
import requests
import re
from pyairtable import Api
from dotenv import load_dotenv

def transform_record(record):
    fields = record['fields']
    transformed = {}
    
    # Create logos directory if it doesn't exist
    logos_dir = 'logos'
    if not os.path.exists(logos_dir):
        os.makedirs(logos_dir)
    
    # Basic fields
    if name := fields.get('Product name'):
        transformed['name'] = name
        
        # Handle logo
        if logo_list := fields.get('Logo '):
            if isinstance(logo_list, list) and logo_list:
                logo_data = logo_list[0]
                
                # Get original filename and extension
                original_filename = logo_data.get('filename', '')
                _, file_extension = os.path.splitext(original_filename)
                
                # Create sanitized filename
                sanitized_name = re.sub(r'[^\w\s-]', '', name)
                new_filename = f"{sanitized_name.lower().replace(' ', '_')}_logo{file_extension}"
                logo_path = os.path.join(logos_dir, new_filename)
                
                # Download using the URL
                if download_url := logo_data.get('url'):
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        with open(logo_path, 'wb') as f:
                            f.write(response.content)
                        transformed['logo'] = f'/img/showcase/{new_filename}'
            else:
                transformed['logo'] = f'/img/showcase/{name.lower().replace(" ", "_")}.png'
        else:
            transformed['logo'] = f'/img/showcase/{name.lower().replace(" ", "_")}.png'
    
    # Other fields
    if id_value := fields.get('id', '').lower().replace(' ', '-'):
        transformed['id'] = id_value
    
    if tags := fields.get('Tags'):
        if isinstance(tags, list) and tags:
            transformed['tags'] = transform_tags(tags)
            
    if website := fields.get('Website'):
        transformed['website'] = website
        
    if github := fields.get('Github'):
        transformed['github'] = github
        
    if description := fields.get('Description'):
        transformed['description'] = description

    if twitter := fields.get('Twitter'):
        transformed['twitter'] = twitter
        
    if fields.get('Use Internet Identity?') is not None:
        transformed['usesInternetIdentity'] = True if fields['Use Internet Identity?'] == "Yes" else False
        
    transformed['display'] = "Normal"
    
    return transformed

def main():
    # Load environment variables
    load_dotenv()
    
    # Initialize Airtable API
    api = Api(os.environ['AIRTABLE_API_KEY'])
    base_id = os.environ.get('AIRTABLE_BASE_ID')
    table_id = os.environ.get('AIRTABLE_TABLE_ID')
    table = api.table(base_id, table_id)
    
    # Fetch all records
    print("Fetching records from Airtable...")
    records = table.all()
    print(f"Total records fetched: {len(records)}")
    
    # Filter records
    filtered_records = []
    for record in records:
        try:
            fields = record.get('fields', {})
            is_not_rejected = fields.get('[Growth team] Rejected?') in [None, False]
            is_not_published = fields.get('[Growth team] Publish?') in [None, False]
            
            if is_not_rejected and is_not_published:
                filtered_records.append(record)
        except KeyError as e:
            print(f"KeyError while filtering record: {e}")
            continue
    
    print(f"Records after filtering: {len(filtered_records)}")
    
    # Transform filtered records
    transformed_records = [transform_record(record) for record in filtered_records]
    print(f"Records after transformation: {len(transformed_records)}")
    
    # Filter out None values
    valid_records = [r for r in transformed_records if r is not None]
    print(f"Valid records: {len(valid_records)}")
    
    # Save to JSON file
    with open('transformed_records.json', 'w') as f:
        json.dump(valid_records, indent=2, fp=f)
    
    print("Transformation complete. Results saved to transformed_records.json")

if __name__ == "__main__":
    main()