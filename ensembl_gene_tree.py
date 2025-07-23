import requests
import csv
import json
import os
import time
import signal
import xml.etree.ElementTree as ET
import argparse
from datetime import datetime
import logging
from tqdm import tqdm
import timeout_decorator
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Global variables to track progress
last_processed_gene = None
processed_genes = set()
total_genes = 0
current_gene_number = 0

# Configure logging
logging.basicConfig(
    filename=f'ensembl_gene_tree_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.DEBUG,  # Changed from INFO to DEBUG for more detailed logs
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Ensembl API endpoints
ENSEMBL_APIS = {
    'Ensembl': {
        'rest': 'https://rest.ensembl.org',
        'mart': 'https://asia.ensembl.org/biomart/martservice'
    },
    'Metazoa': {
        'rest': 'https://rest.ensemblgenomes.org',
        'mart': 'https://metazoa.ensembl.org/biomart/martservice'
    },
    'Plants': {
        'rest': 'https://rest.ensemblgenomes.org',
        'mart': 'https://plants.ensembl.org/biomart/martservice'
    },
    'Fungi': {
        'rest': 'https://rest.ensemblgenomes.org',
        'mart': 'https://fungi.ensembl.org/biomart/martservice'
    },
    'Protists': {
        'rest': 'https://rest.ensemblgenomes.org',
        'mart': 'https://protists.ensembl.org/biomart/martservice'
    }
}

def request_with_retry(url, headers=None, max_retries=3, initial_backoff=1):
    """Make requests with exponential backoff retry logic"""
    if headers is None:
        headers = {"Content-Type": "application/json"}
        
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers=headers, verify=False, timeout=60)
            return response
        except requests.RequestException as e:
            wait_time = initial_backoff * (2 ** retries)
            logging.warning(f"Request failed: {e}. Retrying in {wait_time}s...")
            time.sleep(wait_time)
            retries += 1
            
    # If we get here, all retries failed
    logging.error(f"All {max_retries} requests failed for {url}")
    return None

def get_registry_info(api_key):
    """
    Get BioMart registry information for a specific Ensembl API
    Returns: (mart_name, virtual_schema, datasets) or (None, None, []) on error
    """
    if api_key not in ENSEMBL_APIS:
        logging.error(f"Unknown API key: {api_key}")
        return None, None, []
        
    api_base = ENSEMBL_APIS[api_key]['mart']
    registry_url = f"{api_base}?type=registry"
    
    try:
        response = requests.get(registry_url, timeout=30)
        response.raise_for_status()
        
        # Parse the XML registry
        registry_xml = response.text
        
        try:
            root = ET.fromstring(registry_xml)
        except ET.ParseError as e:
            logging.error(f"Error parsing XML from {api_key}: {e}")
            return None, None, []
        
        # Find available marts
        marts = []
        for mart in root.findall(".//MartURLLocation"):
            mart_name = mart.get('name')
            virtual_schema = mart.get('serverVirtualSchema')
            mart_display = mart.get('displayName')
            database = mart.get('database')
            
            marts.append({
                'name': mart_name,
                'displayName': mart_display,
                'virtualSchema': virtual_schema,
                'database': database
            })
        
        if not marts:
            logging.warning(f"No marts found in registry for {api_key}")
            return None, None, []
        
        # Find gene mart - usually has "gene" in the name
        gene_mart = None
        for mart in marts:
            if 'gene' in mart['name'].lower() or 'gene' in mart['displayName'].lower():
                gene_mart = mart
                break
        
        # If no gene mart found, try to find a mart with "ensembl" in the name
        if not gene_mart:
            for mart in marts:
                if 'ensembl' in mart['name'].lower():
                    gene_mart = mart
                    break
        
        # If still not found, use the first mart
        if not gene_mart and marts:
            gene_mart = marts[0]
        
        if not gene_mart:
            logging.warning(f"No suitable mart found in {api_key}")
            return None, None, []
        
        logging.info(f"Found mart in {api_key}: {gene_mart['displayName']} ({gene_mart['name']})")
        
        # Get datasets for this mart - KEY FIX: Handle TSV response
        datasets_url = f"{api_base}?type=datasets&mart={gene_mart['name']}"
        
        response = requests.get(datasets_url, timeout=30)
        response.raise_for_status()
        
        # Parse the datasets - TSV format, NOT XML
        datasets = []
        lines = response.text.strip().split("\n")
        
        for line in lines:
            if line:
                parts = line.split("\t")
                if len(parts) >= 4:
                    dataset_name = parts[1]
                    display_name = parts[2]
                    interface = parts[3]
                    datasets.append({
                        'name': dataset_name,
                        'displayName': display_name,
                        'interface': interface
                    })
        
        logging.info(f"Found {len(datasets)} datasets in {api_key}")
        return gene_mart['name'], gene_mart['virtualSchema'], datasets
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Network error fetching registry from {api_key}: {e}")
        return None, None, []
    except Exception as e:
        logging.error(f"Unexpected error in get_registry_info for {api_key}: {e}")
        import traceback
        traceback.print_exc()
        return None, None, []

def find_dataset_for_species(scientific_name, datasets):
    """
    Find the dataset name for a given species in the list of available datasets
    Returns a tuple of (dataset_name, match_score) where higher score means better match
    """
    if not datasets:
        return None, 0
    
    # Extract genus and species
    parts = scientific_name.strip().lower().split()
    if len(parts) < 2:
        logging.warning(f"Invalid species format: {scientific_name}")
        return None, 0
    
    genus, species = parts[0], parts[1]
    
    # Match patterns with scores (higher score = better match)
    match_patterns = [
        # Exact matches (score: 100)
        {'pattern': f"{genus}_{species}", 'where': 'name', 'score': 100},
        {'pattern': scientific_name.lower(), 'where': 'display', 'score': 100},
        
        # Strong matches (score: 90)
        {'pattern': f"{genus[0]}{species}", 'where': 'name', 'score': 90},
        
        # Good matches (score: 80)
        {'pattern': f"{species}", 'where': 'name', 'score': 80},
        {'pattern': f"{genus}", 'where': 'name', 'score': 80},
    ]
    
    # Check for matches
    potential_matches = []
    
    for dataset in datasets:
        dataset_name = dataset['name'].lower()
        display_name = dataset['displayName'].lower()
        
        for match in match_patterns:
            pattern = match['pattern']
            where = match['where']
            base_score = match['score']
            
            # Check for pattern in the appropriate field
            if where == 'name' and pattern in dataset_name:
                # Adjust score based on how much of the dataset name matches the pattern
                closeness = len(pattern) / len(dataset_name) if len(dataset_name) > 0 else 0
                adjusted_score = base_score * (0.5 + 0.5 * closeness)
                potential_matches.append((dataset['name'], adjusted_score))
            
            elif where == 'display' and pattern in display_name:
                # Similar adjustment for display name
                closeness = len(pattern) / len(display_name) if len(display_name) > 0 else 0
                adjusted_score = base_score * (0.5 + 0.5 * closeness)
                potential_matches.append((dataset['name'], adjusted_score))
    
    # Return the best match
    if potential_matches:
        best_match = max(potential_matches, key=lambda x: x[1])
        return best_match
    
    return None, 0

def search_species_dataset(species_name):
    """
    Search for a species dataset across Ensembl APIs
    Returns a dictionary with API details and dataset information
    """
    matches = []
    
    for api_key, api_urls in ENSEMBL_APIS.items():
        print(f"Searching for {species_name} in {api_key}...")
        
        # Get registry information
        mart_name, virtual_schema, datasets = get_registry_info(api_key)
        
        if datasets:
            # Find matching dataset
            dataset_match, score = find_dataset_for_species(species_name, datasets)
            
            if dataset_match and score > 0:
                matches.append({
                    'api_key': api_key,
                    'rest_url': api_urls['rest'],
                    'mart_url': api_urls['mart'],
                    'dataset': dataset_match,
                    'score': score,
                    'virtual_schema': virtual_schema,
                    'mart_name': mart_name
                })
    
    # Sort by score (descending)
    matches = sorted(matches, key=lambda x: x['score'], reverse=True)
    
    if matches:
        best_match = matches[0]
        print(f"Found best match for {species_name}: {best_match['dataset']} in {best_match['api_key']} (score: {best_match['score']})")
        return best_match
    else:
        print(f"No matching dataset found for {species_name}")
        return None

def fetch_genes_from_biomart(species_api_info):
    """
    FIXED: Fetch protein-coding genes from BioMart for a specific species
    Handles TSV response format correctly
    """
    dataset = species_api_info['dataset']
    mart_url = species_api_info['mart_url']
    mart_name = species_api_info.get('mart_name', 'metazoa_mart')
    virtual_schema = species_api_info.get('virtual_schema', 'metazoa_mart')
    
    # Create BioMart XML query
    xml_query = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE Query>
<Query  virtualSchemaName="{virtual_schema}" formatter="TSV" header="0" uniqueRows="1" count="" datasetConfigVersion="0.6">
    <Dataset name="{dataset}" interface="default">
        <Attribute name="ensembl_gene_id" />
        <Attribute name="external_gene_name" />
        <Filter name="biotype" value="protein_coding"/>
    </Dataset>
</Query>'''
    
    print(f"Fetching genes from BioMart using dataset: {dataset}")
    
    try:
        # Post the XML query to BioMart
        response = requests.post(
            mart_url,
            data={'query': xml_query},
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=300  # 5 minutes timeout
        )
        response.raise_for_status()
        
        # Parse the TSV response - NOT XML!
        genes = []
        lines = response.text.strip().split('\n')
        
        if not lines or lines[0].strip() == '':
            print("Empty response from BioMart")
            return []
            
        # Check if response contains an error message
        if 'error' in response.text.lower() or 'exception' in response.text.lower():
            print(f"BioMart error response: {response.text[:500]}")
            return []
            
        print(f"BioMart returned {len(lines)} lines")
        
        # Parse TSV format
        for line_num, line in enumerate(lines):
            if line.strip():  # Skip empty lines
                parts = line.split('\t')
                if len(parts) >= 2:
                    gene_id = parts[0].strip()
                    gene_symbol = parts[1].strip() if parts[1].strip() else 'Unknown'
                    
                    if gene_id:  # Only add if gene_id is not empty
                        genes.append({
                            'gene_id': gene_id,
                            'gene_symbol': gene_symbol,
                            'ensembl_id': gene_id
                        })
                else:
                    print(f"Warning: Line {line_num + 1} has unexpected format: {line}")
        
        print(f"Successfully parsed {len(genes)} genes from BioMart")
        
        # Filter out any genes without proper IDs
        valid_genes = [g for g in genes if g['gene_id'] and g['gene_id'] != '']
        
        if len(valid_genes) != len(genes):
            print(f"Filtered out {len(genes) - len(valid_genes)} genes with invalid IDs")
        
        return valid_genes
        
    except requests.exceptions.Timeout:
        print("BioMart request timed out")
        return []
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching genes from BioMart: {e}")
        return []
    except Exception as e:
        print(f"Error parsing BioMart response: {e}")
        print(f"Response content (first 500 chars): {response.text[:500]}")
        return []
        
def save_genes_to_csv(genes, species_name):
    """
    Save genes to CSV file with proper headers
    """
    if not genes:
        print("No genes to save")
        return None
        
    filename = f"{species_name.replace(' ', '_')}_protein-coding_genes.csv"
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['gene_id', 'gene_symbol', 'ensembl_id']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for gene in genes:
                writer.writerow({
                    'gene_id': gene['gene_id'],
                    'gene_symbol': gene['gene_symbol'],
                    'ensembl_id': gene['ensembl_id']
                })
        
        print(f"CSV file '{filename}' has been created with {len(genes)} genes.")
        return filename
        
    except Exception as e:
        print(f"Error saving genes to CSV: {e}")
        return None

def convert_to_ensembl_format(species_name):
    """
    Convert species name to Ensembl API format
    """
    # Convert "Drosophila melanogaster" to "drosophila_melanogaster"
    return species_name.lower().replace(' ', '_')

def read_species_from_file(filename):
    """
    Read a list of species from a text file.
    Each species should be on a separate line in 'Genus species' format.
    """
    species_list = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                species = line.strip()
                if species and not species.startswith('#'):  # Skip empty lines and comments
                    species_list.append(species)
        
        if not species_list:
            print(f"Warning: No valid species found in file {filename}")
        else:
            print(f"Read {len(species_list)} species from {filename}")
            
        return species_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading species file: {e}")
        return None

# Function to fetch gene information from Ensembl with timeout
@timeout_decorator.timeout(300)  # 5 minutes timeout
def fetch_gene_info(gene_id, base_url):
    """Fetch gene information with better error handling"""
    lookup_url = f"{base_url}/lookup/id/{gene_id}?content-type=application/json"
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    
    logging.debug(f"Fetching gene info. URL: {lookup_url}")
    
    try:
        response = requests.get(lookup_url, headers=headers, verify=False, timeout=60)
        logging.debug(f"Fetching gene info: Status Code {response.status_code}")
        
        if response.status_code == 200 and response.text.strip():
            try:
                return response.json()
            except json.JSONDecodeError as e:
                logging.error(f"Failed to parse gene info JSON: {e}")
                logging.debug(f"Response text: {response.text[:200]}...")
                return None
        else:
            logging.error(f"Failed to fetch gene information. Status: {response.status_code}")
            if response.text:
                logging.error(f"Response: {response.text[:200]}...")
            return None
            
    except (requests.RequestException, timeout_decorator.TimeoutError) as e:
        logging.error(f"Request error fetching gene info: {e}")
        return None

# Function to fetch gene tree information from Ensembl with timeout
@timeout_decorator.timeout(300)  # 5 minutes timeout
def fetch_gene_tree_info(gene_id, gene_symbol, species_name, base_url, timeout=30):
    """
    FIXED: Fetch gene tree information for a specific gene using the correct API endpoint
    """
    # Convert species name to Ensembl format for API calls
    species_ensembl_format = convert_to_ensembl_format(species_name)
    
    # For Metazoa API, we need to add compara parameter
    if 'ensemblgenomes.org' in base_url:
        compara_param = 'compara=metazoa'
    else:
        compara_param = ''
    
    # Primary endpoint: gene tree by member ID
    primary_url = f"{base_url}/genetree/member/id/{species_ensembl_format}/{gene_id}"
    if compara_param:
        primary_url += f"?{compara_param}"
    
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    try:
        print(f"Fetching gene tree for {gene_id} from {primary_url}")
        
        # Try primary endpoint first
        response = requests.get(primary_url, headers=headers, timeout=timeout)
        
        if response.status_code == 200:
            try:
                gene_tree_data = response.json()
                if gene_tree_data and 'tree' in gene_tree_data:
                    return gene_tree_data
                else:
                    print(f"No gene tree data found for {gene_id}")
                    return None
            except json.JSONDecodeError:
                print(f"Invalid JSON response for {gene_id}")
                return None
        elif response.status_code == 400:
            print(f"Bad request for {gene_id} - possibly invalid gene ID format")
            return None
        elif response.status_code == 404:
            print(f"Gene {gene_id} not found in gene trees")
            return None
        else:
            print(f"API returned status code {response.status_code} for {gene_id}")
            return None
            
    except requests.exceptions.Timeout:
        print(f"Timeout fetching gene tree for {gene_id}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching gene tree for {gene_id}: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error fetching gene tree for {gene_id}: {e}")
        return None

# Function to process gene tree data
def process_gene_tree(gene_id, gene_symbol, species_name, base_url, output_dir):
    """
    FIXED: Process gene tree information for a single gene
    """
    try:
        gene_tree_info = fetch_gene_tree_info(gene_id, gene_symbol, species_name, base_url)
        
        if gene_tree_info:
            # Save the gene tree data
            file_identifier = gene_symbol if gene_symbol and gene_symbol.lower() != "unknown" else gene_id
            output_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.json')
            
            with open(output_file, 'w') as f:
                json.dump(gene_tree_info, f, indent=2)
            
            print(f"Gene tree saved to {output_file}")
            
            # Also save a summary text file
            summary_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.txt')
            with open(summary_file, 'w') as f:
                f.write(f"Gene Tree Information for {gene_id} ({gene_symbol})\n")
                f.write(f"Species: {species_name}\n")
                f.write(f"Tree ID: {gene_tree_info.get('id', 'N/A')}\n")
                f.write(f"Tree Type: {gene_tree_info.get('type', 'N/A')}\n")
                
                if 'tree' in gene_tree_info:
                    tree_data = gene_tree_info['tree']
                    f.write(f"Tree Structure: {tree_data.get('newick', 'N/A')}\n")
                    
                    # Count species in the tree
                    if 'children' in tree_data:
                        species_count = count_species_in_tree(tree_data)
                        f.write(f"Species count in tree: {species_count}\n")
            
            return True
        else:
            # Create a "no tree" file
            file_identifier = gene_symbol if gene_symbol and gene_symbol.lower() != "unknown" else gene_id
            output_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.txt')
            
            with open(output_file, 'w') as f:
                f.write(f"No gene tree available for {gene_id} ({gene_symbol})\n")
                f.write(f"Species: {species_name}\n")
                f.write(f"This gene may not be included in comparative genomics analyses.\n")
            
            print(f"No gene tree available for {gene_id}. Written to {output_file}")
            return False
            
    except Exception as e:
        print(f"Error processing gene tree for {gene_id}: {e}")
        # Create error file
        file_identifier = gene_symbol if gene_symbol and gene_symbol.lower() != "unknown" else gene_id
        error_file = os.path.join(output_dir, f'{file_identifier}_ERROR.txt')
        with open(error_file, 'w') as f:
            f.write(f"Error processing gene tree for {gene_id}: {str(e)}\n")
        return False

def count_species_in_tree(tree_node):
    """
    Recursively count unique species in a gene tree
    """
    species_set = set()
    
    def traverse_tree(node):
        if isinstance(node, dict):
            # Check if this is a leaf node with sequence info
            if 'sequence' in node:
                seq_info = node['sequence']
                if 'name' in seq_info:
                    # Extract species from sequence name (usually format: SPECIES_GENEID)
                    seq_name = seq_info['name']
                    if '_' in seq_name:
                        species_part = seq_name.split('_')[0]
                        species_set.add(species_part)
            
            # Recursively process children
            if 'children' in node:
                for child in node['children']:
                    traverse_tree(child)
    
    traverse_tree(tree_node)
    return len(species_set)

def process_gene_batch_for_species(genes, output_dir, total_genes, species_name, checkpoint_file, base_url):
    """
    Process a batch of genes for gene tree information
    """
    global current_gene_number, processed_genes
    
    for gene in tqdm(genes, desc="Processing genes"):
        current_gene_number += 1
        
        if gene['gene_id'] in processed_genes:
            print(f"Skipping already processed gene: {gene['gene_id']}")
            continue
        
        print(f"Processing gene {current_gene_number} of {total_genes}: {gene['gene_id']}")
        
        try:
            success = process_gene_tree(
                gene['gene_id'], 
                gene['gene_symbol'], 
                species_name, 
                base_url, 
                output_dir
            )
            
            if success:
                print(f"Successfully processed {gene['gene_id']}")
            else:
                print(f"No gene tree found for {gene['gene_id']}")
            
            # Mark as processed regardless of success
            processed_genes.add(gene['gene_id'])
            save_checkpoint(processed_genes, checkpoint_file)
            
        except Exception as e:
            print(f"Error processing gene {gene['gene_id']}: {e}")
            # Create error file
            file_identifier = gene['gene_symbol'] if gene['gene_symbol'].lower() != "unknown" else gene['gene_id']
            error_file = os.path.join(output_dir, f'{file_identifier}_ERROR.txt')
            with open(error_file, 'w') as f:
                f.write(f"Error processing gene: {str(e)}")
            
            # Still mark as processed to avoid infinite loop
            processed_genes.add(gene['gene_id'])
            save_checkpoint(processed_genes, checkpoint_file)

        # Add delay to avoid overwhelming the API
        time.sleep(0.5)
    
# Function to save checkpoint for a specific species
def save_checkpoint(processed_genes, checkpoint_file):
    with open(checkpoint_file, 'w') as f:
        json.dump({
            'processed_genes': list(processed_genes),
            'last_gene': last_processed_gene,
            'current_gene_number': current_gene_number
        }, f)
    print(f"Checkpoint saved to {checkpoint_file}. Last processed gene: {last_processed_gene}")

# Function to load checkpoint for a specific species
def load_checkpoint(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
            return (
                set(checkpoint_data['processed_genes']),
                checkpoint_data['last_gene'],
                checkpoint_data.get('current_gene_number', 0)
            )
    return set(), None, 0

# Signal handler function
def signal_handler(signum, frame):
    global current_checkpoint_file
    print("\nProcess interrupted. Saving checkpoint...")
    if 'current_checkpoint_file' in globals():
        save_checkpoint(processed_genes, current_checkpoint_file)
    print("You can resume later by running the script again.")
    exit(0)

# Function to process a batch of genes for a specific species
def process_gene_batch_for_species(batch, output_dir, total_genes, species_ensembl_format, checkpoint_file, base_url):
    global last_processed_gene, processed_genes, current_gene_number, current_checkpoint_file
    
    # Set current checkpoint file for the signal handler
    current_checkpoint_file = checkpoint_file

    for gene in tqdm(batch, desc="Processing genes", unit="gene"):
        current_gene_number += 1
        # Skip if gene has already been processed
        if gene['gene_id'] in processed_genes:
            print(f"Skipping already processed gene: {gene['gene_id']}")
            continue

        print(f"\nProcessing gene {current_gene_number} of {total_genes}: {gene['gene_id']}")

        try:
            # Fetch gene information with base_url
            gene_info = fetch_gene_info(gene['gene_id'], base_url)
            gene_symbol = gene['gene_symbol']  # Default to what we have
            
            if gene_info:
                gene_symbol = gene_info.get('display_name', gene['gene_symbol'])
                print(f"Retrieved gene info for: {gene_symbol}")
            else:
                print(f"Using provided gene symbol: {gene_symbol}")

            # Fetch gene tree information with species parameter and base_url
            gene_tree_info = fetch_gene_tree_info(gene['gene_id'], gene_symbol, species_ensembl_format, base_url)

            # Process gene tree data or write "No gene tree available"
            if gene_tree_info:
                processed_data = process_gene_tree_data(gene_tree_info)

                if processed_data:
                    # Use gene_id for file naming when gene_symbol is "Unknown"
                    file_identifier = gene_symbol if gene_symbol.lower() != "unknown" else gene['gene_id']
                    output_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.csv')
                    with open(output_file, 'w', newline='') as csvfile:
                        fieldnames = ['gene_id', 'gene_name', 'species']
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                        writer.writeheader()
                        for row in processed_data:
                            writer.writerow(row)

                    print(f"Gene tree information for {file_identifier} has been written to {output_file}")
                    print(f"Number of entries: {len(processed_data)}")
                else:
                    print(f"No gene tree data found for {gene_symbol} after processing.")
                    file_identifier = gene_symbol if gene_symbol.lower() != "unknown" else gene['gene_id']
                    output_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.txt')
                    with open(output_file, 'w') as txtfile:
                        txtfile.write("No gene tree available")
                    print(f"No gene tree available for {gene_symbol}. Written to {output_file}")
            else:
                file_identifier = gene_symbol if gene_symbol.lower() != "unknown" else gene['gene_id']
                output_file = os.path.join(output_dir, f'{file_identifier}_gene_tree.txt')
                with open(output_file, 'w') as txtfile:
                    txtfile.write("No gene tree available")
                print(f"No gene tree available for {file_identifier}. Written to {output_file}")

            print(f"Successfully processed {gene['gene_id']}")

            # Add processed gene to the set and update last processed gene
            processed_genes.add(gene['gene_id'])
            last_processed_gene = gene['gene_id']

            # Save checkpoint after each gene
            save_checkpoint(processed_genes, checkpoint_file)

        except timeout_decorator.TimeoutError:
            print(f"Timeout occurred while processing gene {gene['gene_id']}. Moving to next gene.")
        except Exception as e:
            print(f"An error occurred while processing gene {gene['gene_id']}: {str(e)}")
            logging.exception(f"Error processing gene {gene['gene_id']}:")
            
            # Create a file to show the error
            file_identifier = gene['gene_symbol'] if gene['gene_symbol'].lower() != "unknown" else gene['gene_id']
            error_file = os.path.join(output_dir, f'{file_identifier}_ERROR.txt')
            with open(error_file, 'w') as txtfile:
                txtfile.write(f"Error processing gene: {str(e)}")
            
            # Still mark as processed to avoid infinite loop
            processed_genes.add(gene['gene_id'])
            last_processed_gene = gene['gene_id']
            save_checkpoint(processed_genes, checkpoint_file)

        # Add backoff delay to avoid overwhelming the API
        time.sleep(1)

# Function to process genes for a specific species
def process_species_genes(species_name, species_api_info, gene_csv_file, output_dir):
    global last_processed_gene, processed_genes, total_genes, current_gene_number
    
    base_url = species_api_info['rest_url']
    species_ensembl_format = convert_to_ensembl_format(species_name)
    
    # Reset tracking variables for this species
    checkpoint_file = os.path.join(output_dir, "checkpoint.json")
    processed_genes, last_processed_gene, current_gene_number = load_checkpoint(checkpoint_file)
    
    # Read the species protein-coding genes CSV file
    species_genes = []
    try:
        with open(gene_csv_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            fieldnames = reader.fieldnames
            print(f"CSV columns: {fieldnames}")
            
            for i, row in enumerate(reader):
                if i < 5:  # Print first 5 rows for debugging
                    print(f"Row {i+1}: {row}")

                gene_id = row.get('gene_id') or row.get('ensembl_id') or row.get('WBGeneID')
                gene_symbol = row.get('gene_symbol') or row.get('symbol') or gene_id

                if not gene_id:
                    print(f"Warning: No gene ID found for row: {row}")
                    continue

                species_genes.append({
                    'gene_id': gene_id,
                    'gene_symbol': gene_symbol
                })
    except FileNotFoundError:
        print(f"Error: Gene list file {gene_csv_file} not found for {species_name}")
        return False
    except Exception as e:
        print(f"Error reading gene file {gene_csv_file}: {str(e)}")
        return False

    total_genes = len(species_genes)
    print(f"Total {species_name} protein-coding genes: {total_genes}")
    print(f"Starting from gene number: {current_gene_number + 1}")
    
    # Process genes in batches
    batch_size = 100
    for i in range(current_gene_number, len(species_genes), batch_size):
        batch = species_genes[i:i+batch_size]
        print(f"\nProcessing batch {i//batch_size + 1} of {(len(species_genes)-1)//batch_size + 1}")
        process_gene_batch_for_species(batch, output_dir, total_genes, species_ensembl_format, checkpoint_file, base_url)
        
    print(f"\nAll genes for {species_name} have been processed.")
    return True

# Main function to process gene tree information for species from a text file
def process_all_gene_trees(species_file, force_api=None):
    # Create results directory for API search results
    os.makedirs("api_search_results", exist_ok=True)
    api_results_file = os.path.join("api_search_results", f"species_api_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv")
    
    # Read the list of species from the file
    species_list = read_species_from_file(species_file)
    if not species_list:
        print("No species to process. Exiting.")
        return
    
    # Species-specific API mapping
    species_api_mapping = {
        "Ciona savignyi": "Metazoa",
        # Add other specific mappings if needed
    }
    
    # Track species API info
    api_results = []
    
    # First pass: Search for each species in Ensembl APIs and save results
    print("\n=== Finding correct Ensembl API and dataset for each species ===\n")
    for species_name in species_list:
        # Check if species has a specific API mapping
        if species_name in species_api_mapping:
            force_api_for_species = species_api_mapping[species_name]
            print(f"Using predefined API {force_api_for_species} for {species_name}")
            api_key = force_api_for_species
            api_results.append({
                'species': species_name,
                'api_key': api_key,
                'rest_url': ENSEMBL_APIS[api_key]['rest'],
                'mart_url': ENSEMBL_APIS[api_key]['mart'],
                'dataset': 'forced',
                'score': 100,
                'found': True  # Changed to True to ensure processing
            })
            continue
            
        # Skip processing if using global force_api option
        if force_api:
            api_key = force_api
            print(f"Forcing use of {api_key} API for {species_name} as specified")
            # Create dummy entry for this species
            api_results.append({
                'species': species_name,
                'api_key': api_key,
                'rest_url': ENSEMBL_APIS[api_key]['rest'],
                'mart_url': ENSEMBL_APIS[api_key]['mart'],
                'dataset': 'forced',
                'score': 100,
                'found': True  # Changed to True to ensure processing
            })
            continue
        
        # Find the correct API and dataset for this species
        species_api_info = search_species_dataset(species_name)
        
        if species_api_info:
            print(f"Found {species_name} in {species_api_info['api_key']} with dataset {species_api_info['dataset']}")
            api_results.append({
                'species': species_name,
                'api_key': species_api_info['api_key'],
                'rest_url': species_api_info['rest_url'],
                'mart_url': species_api_info['mart_url'],
                'dataset': species_api_info['dataset'],
                'score': species_api_info['score'],
                'found': True
            })
        else:
            print(f"Could not find {species_name} in any Ensembl API")
            api_results.append({
                'species': species_name,
                'api_key': 'Not Found',
                'rest_url': '',
                'mart_url': '',
                'dataset': '',
                'score': 0,
                'found': False
            })
    
    # Save API search results to CSV
    with open(api_results_file, 'w', newline='') as csvfile:
        fieldnames = ['species', 'api_key', 'dataset', 'score', 'found', 'rest_url', 'mart_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for result in api_results:
            writer.writerow(result)
    
    print(f"\nAPI search results saved to {api_results_file}")
    
    # Second pass: Process each species with the correct API
    print("\n=== Processing gene trees for each species ===\n")
    for result in api_results:
        species_name = result['species']
        
        if not result['found'] and not force_api:
            print(f"\n{'='*50}")
            print(f"Skipping {species_name} - not found in any Ensembl API")
            print(f"{'='*50}")
            continue
        
        api_key = result['api_key']
        species_api_info = {
            'api_key': api_key,
            'rest_url': result['rest_url'],
            'mart_url': result['mart_url'],
            'dataset': result['dataset']
        }
        
        if force_api or species_name in species_api_mapping:
            # Get the correct dataset name by querying the API directly
            mart_name, virtual_schema, datasets = get_registry_info(api_key)
            if datasets:
                dataset_match, score = find_dataset_for_species(species_name, datasets)
                if dataset_match:
                    species_api_info['dataset'] = dataset_match
                    species_api_info['mart_name'] = mart_name
                    species_api_info['virtual_schema'] = virtual_schema
                else:
                    print(f"Could not find dataset for {species_name} in {api_key}")
                    continue
            else:
                print(f"Could not get datasets for {api_key}")
                continue
        else:
            # Add mart_name and virtual_schema to species_api_info
            mart_name, virtual_schema, _ = get_registry_info(api_key)
            species_api_info['mart_name'] = mart_name
            species_api_info['virtual_schema'] = virtual_schema
        
        print(f"\n{'='*50}")
        print(f"Processing species: {species_name}")
        print(f"Using API: {api_key}")
        print(f"Dataset: {species_api_info['dataset']}")
        print(f"{'='*50}")
        
        # Create a directory for this species
        species_dir = f"{species_name.replace(' ', '_')}_gene_tree_files_{api_key.lower()}"
        os.makedirs(species_dir, exist_ok=True)
        
        # Check if gene CSV file exists, if not, fetch genes from BioMart
        gene_csv_file = f"{species_name.replace(' ', '_')}_protein-coding_genes.csv"
        
        if not os.path.exists(gene_csv_file):
            print(f"Gene list file {gene_csv_file} not found for {species_name}")
            print(f"Fetching genes from BioMart...")
            genes = fetch_genes_from_biomart(species_api_info)
            if genes:
                gene_csv_file = save_genes_to_csv(genes, species_name)
            else:
                print(f"Failed to fetch genes for {species_name}")
                continue
        else:
            print(f"Using existing gene list file: {gene_csv_file}")
            
        # Process the genes for this species
        success = process_species_genes(species_name, species_api_info, gene_csv_file, species_dir)
        if success:
            print(f"Successfully processed all genes for {species_name} using {api_key}")
        else:
            print(f"Failed to process genes for {species_name}")

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description="Fetch gene trees from Ensembl APIs with automatic dataset detection")
    parser.add_argument("species_file", help="Text file containing species names (one per line)")
    parser.add_argument("--force", choices=['Ensembl', 'Metazoa', 'Plants', 'Fungi', 'Protists'], 
                        help="Force use of a specific Ensembl API instead of auto-detection")
    return parser.parse_args()

# Run the main function
if __name__ == "__main__":
    # Set up signal handler
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Parse command line arguments
    args = parse_arguments()
    
    try:
        process_all_gene_trees(args.species_file, args.force)
        print("\nAll species have been processed successfully.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        logging.exception("Fatal error")
        if 'current_checkpoint_file' in globals():
            print("Saving checkpoint before exiting...")
            save_checkpoint(processed_genes, current_checkpoint_file)
        print("You can resume later by running the script again.")
