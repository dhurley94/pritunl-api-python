#!/bin/bash

from config import pritunl as pri

# Ping host
if pri.ping():
    # Create server
    pri.server.post(data={'name': 'EXAMPLE_SERVER'})

    # Create org
    pri.organization.post(data={'name': 'EXAMPLE_ORG'})

    # View all orgs
    x = pri.organization.get()

    # View all servers
    s = pri.server.get()

    # Attach org[0] to server[0]
    pri.server.put(srv_id=s[0]['id'], org_id=x[0]['id'])

    # Start server
    pri.server.put(srv_id=s[0]['id'], operation='start')
    pri.server.put(srv_id=s[0]['id'], operation='stop')

    s = pri.server.get()

    # Create a custom route
    pri.route.post(srv_id=s[0]['id'], data={
        "network": "192.168.1.0/24",
        "comment": "Testing comments",
        "metric": 2,
        "nat": True,
        "nat_interface": "",  # optional
        "nat_netmap": "",  # map two pritunl servers
        "advertise": False,
        # "vpc_region": "",
        # "vpc_id": "",
        "net_gateway": False
    })

    pri.server.put(srv_id=s[0]['id'], operation='start')

    # Add users to org[0]
    pri.user.post(org_id=x[0]['id'], data={'name': 'EXAMPLE_USER'})
    pri.user.post(org_id=x[0]['id'], data={'name': 'TO_BE_DELETED'})

    # View users id
    q = pri.user.get(org_id=x[0]['id'])

    # Delete users
    pri.user.delete(org_id=x[0]['id'], usr_id=q[1]['id'])

    # Get user key download link
    z = pri.key.get(org_id=x[0]['id'], usr_id=q[0]['id'])
    print(z)

    # Delete key
    pri.user.delete(org_id=x[0]['id'], usr_id=q[0]['id'])

    # Delete server
    pri.server.delete(srv_id=s[0]['id'])

    # Delete organization
    pri.organization.delete(org_id=x[0]['id'])
