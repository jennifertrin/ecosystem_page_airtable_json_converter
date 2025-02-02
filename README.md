# Airtable to Ecosystem JSON Transformer

This script transforms Airtable form submissions into a structured JSON format for use in the ecosystem page. It handles data transformation, logo downloads, and filtering of submissions based on specific criteria.

## Features

- Fetches records from a specified Airtable base
- Downloads and manages project logos
- Transforms Airtable records into a standardized JSON format
- Filters out rejected and already published submissions
- Handles field sanitization and validation
- Supports Internet Identity status tracking

## Prerequisites

- Python 3.x
- Required Python packages:
  ```
  python-dotenv
  pyairtable
  requests
  ```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```
AIRTABLE_API_KEY=your_api_key
AIRTABLE_BASE_ID=your_base_id
AIRTABLE_TABLE_ID=your_table_id
```

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install python-dotenv pyairtable requests
   ```
3. Create the `.env` file with your Airtable credentials

## Usage

Run the script using:

```bash
python transform_airtable.py
```

The script will:
1. Create a `logos` directory if it doesn't exist
2. Fetch records from Airtable
3. Filter out rejected and published submissions
4. Transform the records into the required format
5. Download project logos
6. Save the transformed data to `transformed_records.json`

## Output Format

The script generates a JSON file with the following structure for each record:

```json
{
  "name": "Project Name",
  "id": "project-id",
  "logo": "/img/showcase/project_name_logo.png",
  "tags": ["tag1", "tag2"],
  "website": "https://example.com",
  "github": "https://github.com/example",
  "description": "Project description",
  "twitter": "https://twitter.com/example",
  "usesInternetIdentity": true,
  "display": "Normal"
}
```

## Field Transformations

- **Product name**: Used as `name` and for generating logo filenames
- **Logo**: Downloaded and stored in the `logos` directory
- **Tags**: Transformed into a standardized format
- **Website, Github, Twitter**: Stored as direct URLs
- **Use Internet Identity?**: Converted to boolean
- **Display**: Set to "Normal" by default

## Filtering Logic

Records are filtered out if they:
- Have been rejected (`[Growth team] Rejected?` is true)
- Have already been published (`[Growth team] Publish?` is true)

## Error Handling

- Creates missing directories as needed
- Handles missing or malformed fields gracefully
- Reports progress and record counts during processing
- Validates logo downloads and file operations

## Contributing

Feel free to submit issues and enhancement requests.