# Tunnel docker container network traffic via VPN

Scenario: You wish that you could you supply an argument to your docker run file that would take all the traffic in the container and tunnel it via a VPN.

Solution: Run an additional container with a VPN client inside and then on the original container use the argument `--net=container:vpnClientContainerId` which will effectively take the container's traffic and route it through the VPN client container.
