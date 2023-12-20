import boto3
import json
import traceback

ecs = boto3.client("ecs", region_name="us-east-1")

def lambda_handler(event, context):

    try:
        spot_ecs(event, context)

        return "Completed"

    except Exception as e:
            displayException(e)
            traceback.print_exc()

def spot_ecs(event, context):

        # Get action parameter from event
        action = event.get('action')
        service_type = event.get('service_type')
        capacity_spot = event.get('capacity_spot')

        if action is None:
            action = ''

    # Check action
        if action.lower() not in ['active']:
            print ("action was neither active. spot_ecs() aborted.")

        else:

            try:

                clusters = ecs.list_clusters()

                cluster_arn = clusters['clusterArns']
                x = len(cluster_arn)
                for i in range(x):
                    cluster_arn = clusters['clusterArns'][i]

                    print ("ARN Cluster " + cluster_arn + " that can be active")
                    _,r = cluster_arn.split("/")
                    print ("Sprit var arn cluster " + r)
                    s = r.split()

                    for cluster_name in s:

                        if capacity_spot == "80":

                            result = ecs.update_service(
                                cluster=cluster_name,
                                service=cluster_name + "-" + service_type,
                                capacityProviderStrategy=[
                                    {
                                        'capacityProvider': 'FARGATE',
                                        'weight': 2,
                                        'base': 1
                                    },
                                    {
                                        'capacityProvider': 'FARGATE_SPOT',
                                        'weight': 8
                                    },
                                ],
                                forceNewDeployment = True,
                            )

                            print("Number of tasks FARGATE_SPOT = 8 and FARGATE = 2")
                            print ("\n")

                        elif capacity_spot == "50":

                            result = ecs.update_service(
                                cluster=cluster_name,
                                service=cluster_name + "-" + service_type,
                                capacityProviderStrategy=[
                                    {
                                        'capacityProvider': 'FARGATE',
                                        'weight': 5,
                                        'base': 1
                                    },
                                    {
                                        'capacityProvider': 'FARGATE_SPOT',
                                        'weight': 5
                                    },
                                ],
                                forceNewDeployment = True,
                            )

                            print("Number of tasks FARGATE_SPOT = 5 and FARGATE = 5")
                            print ("\n")

                        elif capacity_spot == "20":

                            result = ecs.update_service(
                                cluster=cluster_name,
                                service=cluster_name + "-" + service_type,
                                capacityProviderStrategy=[
                                    {
                                        'capacityProvider': 'FARGATE',
                                        'weight': 8,
                                        'base': 1
                                    },
                                    {
                                        'capacityProvider': 'FARGATE_SPOT',
                                        'weight': 2
                                    },
                                ],
                                forceNewDeployment = True,
                            )

                            print("Number of tasks FARGATE_SPOT = 2 and FARGATE = 8")
                            print ("\n")

                        elif capacity_spot == "0":

                            result = ecs.update_service(
                                cluster=cluster_name,
                                service=cluster_name + "-" + service_type,
                                capacityProviderStrategy=[
                                    {
                                        'capacityProvider': 'FARGATE',
                                        'weight': 1,
                                        'base': 1
                                    },
                                    {
                                        'capacityProvider': 'FARGATE_SPOT',
                                        'weight': 0
                                    },
                                ],
                                forceNewDeployment = True,
                            )

                            print("Number of tasks FARGATE_SPOT = 0 and FARGATE = 1")
                            print ("\n")

                        else:

                            print("There is no such value in capacity_spot")
                            print ("\n")

                        print ("Name Service " + cluster_name + "-" + service_type + " that can be active")
                        print ("\n")
                        #print(json.dumps(result, indent=4, default=str))

            except Exception as e:
                displayException(e)

def displayException(exception):
    exception_type = exception.__class__.__name__
    exception_message = str(exception)

    print("Exception type: %s; Exception message: %s;" % (exception_type, exception_message))
