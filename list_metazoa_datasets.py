import requests
import xml.etree.ElementTree as ET

def list_metazoa_datasets():
    """Get the correct list of datasets from Ensembl Metazoa"""
    
    print("Fetching BioMart registry from Ensembl Metazoa...")
    
    # First, get the registry to identify the correct configuration
    registry_url = "https://metazoa.ensembl.org/biomart/martservice?type=registry"
    
    try:
        response = requests.get(registry_url)
        response.raise_for_status()
        
        # Parse the XML registry
        registry_xml = response.text
        root = ET.fromstring(registry_xml)
        
        # Find the correct virtual schema and database for metazoa
        marts = []
        for mart in root.findall(".//MartURLLocation"):
            mart_name = mart.get('name')
            virtual_schema = mart.get('serverVirtualSchema')
            mart_display = mart.get('displayName')
            database = mart.get('database')
            
            print(f"Found mart: {mart_display} (name: {mart_name}, schema: {virtual_schema})")
            marts.append({
                'name': mart_name,
                'displayName': mart_display,
                'virtualSchema': virtual_schema,
                'database': database
            })
        
        if not marts:
            print("No marts found in registry!")
            return
        
        # Use the gene mart (usually has "gene" in the name or it's the default mart)
        gene_mart = None
        for mart in marts:
            if 'gene' in mart['name'].lower():
                gene_mart = mart
                break
        
        if not gene_mart:
            gene_mart = marts[0]  # Use first mart if no gene mart found
        
        print(f"\nUsing mart: {gene_mart['displayName']} ({gene_mart['name']})")
        
        # Now get the datasets for this mart
        datasets_url = f"https://metazoa.ensembl.org/biomart/martservice?type=datasets&mart={gene_mart['name']}"
        
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
        
        print(f"\nFound {len(datasets)} datasets in Ensembl Metazoa:")
        for dataset in sorted(datasets, key=lambda x: x['displayName']):
            print(f"  {dataset['name']} - {dataset['displayName']}")
        
        return datasets
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        if 'response' in locals():
            print(f"Response status code: {response.status_code}")
            print(f"Response content: {response.text}")
        return None

if __name__ == "__main__":
    list_metazoa_datasets()
