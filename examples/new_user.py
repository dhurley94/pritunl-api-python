#!/usr/bin/python3
from config import pritunl as pri


def get_user_by_name(users, name):
    for user in users:
        if user["name"] == name:
            return user
    return None


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-n", "--name", required=True)
    parser.add_argument("-e", "--email", required=True)
    parser.add_argument("-p", "--pin", required=True)
    parser.add_argument("-y", "--yubikey_id", required=False)
    parser.add_argument("-f", "--force", required=False, action='store_true',
                        help="Recreate the user in case it already exists")
    args = parser.parse_args()

    # Ping host
    if pri.ping():

        # View all orgs
        x = pri.organization.get()

        # for org in x:
        #     if 'development' in org['name']:
        #         pref_org = org
        #     print(org)

        srv = pri.server.get()
        for server in srv:
            print(server)

        log = pri.log.get()
        for l in log:
            print(l)

        org_name = "test_organization"
        # get all organizations
        orgs = pri.organization.get()
        for org in orgs:
            print(f"found: {org}")
            if org_name in org["name"]:
                new_org = org
            #     # delete an organization
            #     print(f"delete: {org}")
            #     print(pri.organization.delete(org["id"]))

        # create an organization
        # new_org = pri.organization.post({"name": org_name, "auth_api": False})

        # exit(0)
        for user in pri.user.get(org_id=new_org['id']):
            if user["name"] == args.name:
                print(user)
                pri.user.delete(org_id=new_org['id'], usr_id=user['id'])

        # if user is not None and args.force is True:
        #     print("delete")
        #     pri.user.delete(org_id=new_org['id'], usr_id=user['id'])
        #     user = None

        if user is None:
            # POST payload
            payload = {
                'name': args.name,
                'email': args.email,
                'pin': args.pin,
                'disabled': False
            }
            # if args.yubikey_id is not None:
            #     # Add yubikey settings to payload
            #     payload["auth_type"] = "yubico"
            #     payload["yubico_id"] = args.yubikey_id[:12]
            # pri
            # Add users to org[0]
            print(payload)
            pri.user.post(org_id=new_org['id'], data=payload)

        # View users id
        q = pri.user.get(org_id=new_org['id'])
        # for user in q:
        #     user_id = user['id']
        # 
        # pri.user.delete(org_id=pref_org['id'], usr_id=user_id)
        # print(q)
        # # Delete users
        # #pri.user.delete(org_id=x[0]['id'], user_id=q[1]['id'])
        #
        # # Get user key download link
        # print(pri.key.get(org_id=x[0]['id'], usr_id=getUserByName(q,args.name)['id']).content.decode('utf-8'))
        #
