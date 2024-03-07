import docker
import argparse
from typing import List

client = docker.from_env()

def create_network(network_name: str):
    """Create a Docker network."""
    existing_networks = client.networks.list(names=[network_name])
    if existing_networks:
        print(f"Network '{network_name}' already exists. Removing existing network.")
        existing_networks[0].remove()
    return client.networks.create(network_name, driver="bridge")

def create_container(image: str, name: str, network_name: str, hostname: str = None):
    """Create and start a Docker container."""
    container = client.containers.run(image, 
                                      name=name, 
                                      hostname=hostname, 
                                      detach=True, 
                                      network=network_name, 
                                      command="tail -f /dev/null") # Keep the container running
    return container

def test_ping(from_container, target_name: str) -> bool:
    """Test ping from one container to another."""
    try:
        exit_code, output = from_container.exec_run(cmd=f"ping -c 3 {target_name}", stdout=True, stderr=True)
        return exit_code == 0
    except docker.errors.APIError as e:
        print(f"Error executing ping: {e}")
        return False

def cleanup(containers: List[str], network_name: str):
    """Remove containers and network."""
    for container_name in containers:
        container = client.containers.get(container_name)
        container.stop()
        container.remove()
    network = client.networks.get(network_name)
    network.remove()

def main(targets: int):
    network_name = "hack-net"
    attacker_name = "attacker"
    target_base_name = "target-"

    # Create network
    network = create_network(network_name)

    # Create attacker container
    attacker = create_container("alpine", attacker_name, network_name, hostname=attacker_name)

    # Create target containers
    targets_containers = []
    for i in range(targets):
        target_name = f"{target_base_name}{i}"
        target = create_container("alpine", target_name, network_name, hostname=target_name)
        targets_containers.append(target)

    # Test ping
    for target in targets_containers:
        if not test_ping(attacker, target.name):
            print(f"Ping to {target.name} failed.")
        else:
            print(f"Ping to {target.name} succeeded.")

    # Cleanup
    container_names = [attacker.name] + [target.name for target in targets_containers]
    cleanup(container_names, network_name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Provision Docker containers on a network.")
    parser.add_argument("--targets", type=int, help="Number of target containers to create", required=True)
    args = parser.parse_args()
    main(args.targets)
