#!/usr/bin/env python3
"""
Ensembl Species Dataset Finder

This script takes a list of species names in "Genus species" format and searches
across all Ensembl APIs to find the corresponding dataset name and API endpoint.

Usage:
  python ensembl_dataset_finder.py species_list.txt
  python ensembl_dataset_finder.py --interactive
"""

import requests
import xml.etree.ElementTree as ET
import argparse
import os
import time
import sys
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    filename=f'ensembl_dataset_search_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Define Ensembl API endpoints
ENSEMBL_APIS = {
    'Ensembl': 'https://www.ensembl.org',
    'Metazoa': 'https://metazoa.ensembl.org',
    'Plants': 'https://plants.ensembl.org',
    'Fungi': 'https://fungi.ensembl.org',
    'Protists': 'https://protists.ensembl.org',
    'Bacteria': 'https://bacteria.ensembl.org'
}

def get_registry_info(api_base):
    """
    Get BioMart registry information for a specific Ensembl API
    """
    api_name = next((name for name, url in ENSEMBL_APIS.items() if url == api_base), "Unknown API")
    registry_url = f"{api_base}/biomart/martservice?type=registry"
    
    try:
        response = requests.get(registry_url)
        response.raise_for_status()
        
        # Parse the XML registry
        registry_xml = response.text
        root = ET.fromstring(registry_xml)
        
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
            logging.warning(f"No marts found in registry for {api_name}")
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
            logging.warning(f"No suitable mart found in {api_name}")
            return None, None, []
        
        logging.info(f"Found mart in {api_name}: {gene_mart['displayName']} ({gene_mart['name']})")
        
        # Get datasets for this mart
        datasets_url = f"{api_base}/biomart/martservice?type=datasets&mart={gene_mart['name']}"
        
        response = requests.get(datasets_url)
        response.raise_for_status()
        
        # Parse the datasets
        datasets = []
        for line in response.text.strip().split("\n"):
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
        
        logging.info(f"Found {len(datasets)} datasets in {api_name}")
        return gene_mart['name'], gene_mart['virtualSchema'], datasets
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching registry from {api_name}: {e}")
        if 'response' in locals():
            logging.error(f"Response status code: {response.status_code}")
        return None, None, []
    except ET.ParseError as e:
        logging.error(f"Error parsing XML from {api_name}: {e}")
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
        
        # Weaker matches (score: 70)
        {'pattern': f"{genus[0:3]}", 'where': 'name', 'score': 70},
        {'pattern': f"{species[0:3]}", 'where': 'name', 'score': 70}
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
                # Higher score for dataset name that's closer to just the pattern
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

def search_species_across_apis(species_name):
    """
    Search for a species across all Ensembl APIs
    Returns a list of matches with API name, dataset name, and match score
    """
    matches = []
    
    for api_name, api_base in ENSEMBL_APIS.items():
        print(f"Searching for {species_name} in {api_name}...")
        
        # Get registry information
        mart_name, virtual_schema, datasets = get_registry_info(api_base)
        
        if datasets:
            # Find matching dataset
            dataset_match, score = find_dataset_for_species(species_name, datasets)
            
            if dataset_match and score > 0:
                matches.append({
                    'api_name': api_name,
                    'api_url': api_base,
                    'dataset': dataset_match,
                    'score': score,
                    'virtual_schema': virtual_schema,
                    'mart_name': mart_name
                })
    
    # Sort by score (descending)
    return sorted(matches, key=lambda x: x['score'], reverse=True)

def read_species_from_file(filename):
    """
    Read a list of species from a text file
    """
    species_list = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                species = line.strip()
                if species and not species.startswith('#'):
                    species_list.append(species)
        
        if species_list:
            print(f"Read {len(species_list)} species from {filename}")
        else:
            print(f"Warning: No valid species found in file {filename}")
            
        return species_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except Exception as e:
        print(f"Error reading species file: {e}")
        return None

def save_results_to_csv(results, filename=None):
    """
    Save search results to a CSV file
    """
    if not filename:
        filename = f"ensembl_datasets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    import csv
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['species', 'api_name', 'dataset', 'score', 'api_url', 'mart_name', 'virtual_schema']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for species, matches in results.items():
            if matches:
                for match in matches:
                    writer.writerow({
                        'species': species,
                        'api_name': match['api_name'],
                        'dataset': match['dataset'],
                        'score': match['score'],
                        'api_url': match['api_url'],
                        'mart_name': match['mart_name'],
                        'virtual_schema': match['virtual_schema']
                    })
            else:
                writer.writerow({
                    'species': species,
                    'api_name': 'Not Found',
                    'dataset': 'Not Found',
                    'score': 0,
                    'api_url': '',
                    'mart_name': '',
                    'virtual_schema': ''
                })
    
    print(f"Results saved to {filename}")
    return filename

def format_results_table(results):
    """
    Format results as a text table
    """
    lines = []
    lines.append("=" * 100)
    lines.append(f"{'Species':<30} {'API':<15} {'Dataset':<30} {'Match Score':<10} {'Virtual Schema'}")
    lines.append("=" * 100)
    
    for species, matches in results.items():
        if matches:
            for match in matches:
                lines.append(f"{species:<30} {match['api_name']:<15} {match['dataset']:<30} {match['score']:<10.1f} {match['virtual_schema']}")
        else:
            lines.append(f"{species:<30} {'Not Found':<15} {'Not Found':<30} {0:<10} {'N/A'}")
        lines.append("-" * 100)
    
    return "\n".join(lines)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Search for species datasets across all Ensembl APIs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument("species_file", nargs="?", 
                      help="File containing species names (one per line)")
    
    parser.add_argument("--interactive", "-i", action="store_true",
                      help="Enter species interactively")
                      
    parser.add_argument("--output", "-o",
                      help="Output CSV file name")
    
    return parser.parse_args()

def main():
    """Main function"""
    args = parse_arguments()
    
    # Get species list
    species_list = []
    
    if args.interactive:
        # Interactive mode
        print("Enter species names in 'Genus species' format (one per line).")
        print("Enter a blank line when finished:")
        
        while True:
            species = input()
            if not species:
                break
            species_list.append(species)
    elif args.species_file:
        # Read from file
        species_list = read_species_from_file(args.species_file)
    else:
        # No input specified, show help
        print("Please specify a species file or use --interactive mode.")
        print("Example: python ensembl_dataset_finder.py species_list.txt")
        print("Example: python ensembl_dataset_finder.py --interactive")
        return
    
    if not species_list:
        print("No species to process. Exiting.")
        return
    
    # Process each species
    results = {}
    
    for species in species_list:
        print(f"\nSearching for {species} across Ensembl APIs...")
        matches = search_species_across_apis(species)
        results[species] = matches
        
        if matches:
            print(f"Found {len(matches)} potential datasets for {species}:")
            for i, match in enumerate(matches, 1):
                print(f"  {i}. {match['api_name']} - {match['dataset']} (score: {match['score']:.1f})")
        else:
            print(f"No matching datasets found for {species}")
        
        # Add a small delay to avoid overwhelming APIs
        time.sleep(0.5)
    
    # Save and display results
    if args.output:
        csv_file = save_results_to_csv(results, args.output)
    else:
        csv_file = save_results_to_csv(results)
    
    # Print formatted table
    print("\nResults Summary:")
    print(format_results_table(results))
    
    print(f"\nDetailed results have been saved to {csv_file}")

if __name__ == "__main__":
    main()