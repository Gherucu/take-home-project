import pytest
import sys
from pathlib import Path
from unittest.mock import MagicMock, call

# Assuming the structure of main.py uses docker.from_env() as shown:
# import docker
# client = docker.from_env()

# Calculate the absolute path to the project root
project_root = Path(__file__).parent.parent.absolute()

# Add the project root to sys.path
sys.path.insert(0, str(project_root))

@pytest.fixture
def mock_docker_client(mocker):
    # Patch the docker.from_env() method globally
    mocker.patch('docker.from_env', return_value=MagicMock())
    from main import client
    return client

@pytest.fixture
def setup_networks_mock(mock_docker_client, mocker):
    # Mock the networks.create method
    mock_docker_client.networks.create = MagicMock()

@pytest.fixture
def setup_containers_mock(mock_docker_client, mocker):
    # Mock the containers.run method
    mock_docker_client.containers.run = MagicMock()

@pytest.fixture
def setup_cleanup_mocks(mock_docker_client, mocker):
    # Mock the get methods for containers and networks
    mock_docker_client.containers.get = MagicMock(side_effect=lambda name: MagicMock(name=name))
    mock_docker_client.networks.get = MagicMock()

def test_create_network(mock_docker_client, mocker):
    mock_networks_create = mock_docker_client.networks.create
    network_name = "hack-net"
    
    # Import the function after the fixture setup to ensure it uses the mocked docker client
    from main import create_network
    create_network(network_name)
    
    mock_networks_create.assert_called_once_with(network_name, driver="bridge")

def test_create_container_with_existing_network(mock_docker_client, mocker):
    network_name = "hack-net"
    image = "alpine"
    name = "attacker"
    hostname = "attacker"
    
    mocker.patch.object(mock_docker_client.networks, 'list', return_value=[MagicMock(name=network_name)])
    mock_containers_run = mock_docker_client.containers.run
    
    from main import create_container
    create_container(image, name, network_name, hostname)
    
    mock_containers_run.assert_called_once_with(image, name=name, hostname=hostname, detach=True, network=network_name, command="tail -f /dev/null")

def test_cleanup(mock_docker_client, mocker):
    containers = ["attacker", "target-0"]
    network_name = "hack-net"
    
    mocker.patch.object(mock_docker_client.containers, 'get', side_effect=lambda name: MagicMock(name=name))
    mocker.patch.object(mock_docker_client.networks, 'get', return_value=MagicMock(name=network_name))
    
    from main import cleanup
    cleanup(containers, network_name)
    
    mock_docker_client.containers.get.assert_has_calls([call(name) for name in containers], any_order=True)
    network_mock = mock_docker_client.networks.get.return_value
    network_mock.remove.assert_called_once()