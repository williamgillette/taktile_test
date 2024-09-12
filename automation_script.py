import requests
import json

# Taktile API configuration
API_BASE_URL = 'https://eu-central-1.taktile-org.decide.taktile.com/run/api/v1/flows/'
API_KEY = 'temp_api_key'

# Function to list decision flows
def list_decision_flows():
    url = f"{API_BASE_URL}list-decision-graphs/sandbox/decide"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY
    }
    data = {
        "data": {"organization_name": "NB36"},
        "metadata": {"version": "v1.0", "entity_id": "string"},
        "control": {"execution_mode": "sync"}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to get the decision graph for a specific flow_id
def get_decision_graph(flow_id):
    url = f"{API_BASE_URL}get-decision-graph/sandbox/decide"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY
    }
    data = {
        "data": {"flow_id": flow_id},
        "metadata": {"version": "v1.0", "entity_id": "string"},
        "control": {"execution_mode": "sync"}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to patch a code node with new code
def patch_code_node(flow_id, node_id, new_code):
    url = f"{API_BASE_URL}patch-decision-graph/sandbox/decide"
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'X-Api-Key': API_KEY
    }
    data = {
        "data": {
            "flow_id": flow_id,
            "node_id": node_id,
            "src_code": new_code
        },
        "metadata": {"version": "v1.0", "entity_id": "string"},
        "control": {"execution_mode": "sync"}
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Function to read the content of the Python files to patch the code nodes
def read_code_file(filename):
    with open(filename, 'r') as file:
        return file.read()

# Main automation function to update the code nodes in Taktile
def update_taktile_code():
    # List decision flows
    flows_response = list_decision_flows()
    if 'flows' in flows_response.get('data', {}):
        flow_id = flows_response['data']['flows'][0]['flow_id']

        # Get decision graph for the identified flow
        graph_response = get_decision_graph(flow_id)
        nodes = graph_response.get('data', {}).get('graph', [])

        # Update Multiply code node
        multiply_code = read_code_file('Multiply.py')
        for node in nodes:
            if node['node_name'] == 'Multiply':
                patch_code_node(flow_id, node['node_id'], multiply_code)

        # Update Summarize code node
        summarize_code = read_code_file('Summarize.py')
        for node in nodes:
            if node['node_name'] == 'Summarize':
                patch_code_node(flow_id, node['node_id'], summarize_code)

        print("Code nodes updated successfully.")

# Trigger the update process
if __name__ == "__main__":
    update_taktile_code()
