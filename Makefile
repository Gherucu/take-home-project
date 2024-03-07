# Define variables for use in the Makefile
target_base_name = target-
attacker_name = attacker
network_name = hack-net
image_name = alpine

# Default action if no specific target is called
all: run

# Run the application with n targets
run:
	@echo "Running application with $(n) targets..."
	@poetry run python3 src/main.py --targets $(n)

# Install dependencies using poetry
install:
	@echo "Installing dependencies..."
	@poetry install --no-root

# Run the test suite
test:
	@echo "Running tests..."
	@poetry run pytest src/tests/test_main_pytest.py

# Clean up Docker containers and network
clean:
	@echo "Cleaning up containers and network..."
	@docker container ls -a --format '{{.Names}}' | grep -E '^($(target_base_name)|$(attacker_name))' | xargs -r docker container rm -f
	@docker network ls --format '{{.Name}}' | grep '^$(network_name)$$' | xargs -r docker network rm


################################################
#
#	BONUS Section
#

# Run the docker-compose file for nuke test
nuke:
	@echo "Testing the nuke launch code retrieval..."
	@docker-compose -f bonus/nuke/docker-compose.yml up --build --exit-code-from attacker --abort-on-container-exit

# Run the docker-compose file for ai-takeover
ai-takeover:
	@echo "Testing the ai-takeover code retrieval..."
	@docker-compose -f bonus/ai-takeover/docker-compose.yml up --build --exit-code-from attacker --abort-on-container-exit


.PHONY: all run install clean
