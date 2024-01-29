import oci

def locate_comp(identity_client, target_name, compartment_id=None):
    list_compartments_response = identity_client.list_compartments(
        compartment_id if compartment_id else config['tenancy']
    )
    
    for compartment in list_compartments_response.data:
        if compartment.name == target_name:
            return compartment

        child_compartment = locate_comp(identity_client, target_name, compartment.id)
        if child_compartment:
            return child_compartment

    return None

# Set your OCI credentials
config = oci.config.from_file("~/.oci/config")

# Specify the target compartment name
target_compartment_name = "platform-services"

# Initialize the Identity and Compute clients
identity_client = oci.identity.IdentityClient(config)
compute_client = oci.core.ComputeClient(config)

# Retrieve the compartment details using the compartment name
compartment = locate_comp(identity_client, target_compartment_name)

if not compartment:
    print(f"Compartment '{target_compartment_name}' not found.")
else:
    # List instances in the specified compartment
    instances = []
    list_instances_response = compute_client.list_instances(compartment_id=compartment.id)
    instances.extend(list_instances_response.data)

    # Iterate through the instances and print relevant information
    for instance in instances:
        print(f"Instance Name: {instance.display_name}")
        print(f"Instance OCID: {instance.id}")
        print(f"Availability Domain: {instance.availability_domain}")
        print(f"State: {instance.lifecycle_state}")
        print("=" * 30)
