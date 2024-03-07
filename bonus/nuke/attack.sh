#!/bin/sh

# Wait for the target to be ready
sleep 10

# Attempt to SSH into the target and read the confidential file
if sshpass -p "pass" ssh -o StrictHostKeyChecking=no root@target "cat /root/confidential.txt"; then
  echo "SUCCESS"
  # If the SSH command was successful, exit with status code 0
  exit 0
else
  # If the SSH command failed, exit with a non-zero status code
  exit 1
fi
