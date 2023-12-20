import boto3
import json
import traceback

ecs = boto3.client("ecs", region_name="us-east-1")

def lambda_handler(event, context):

    try:
        start_ecs(event, context)
        return "Completed"

    except Exception as e:
            displayException(e)
            traceback.print_exc()

def start_ecs(event, context):

        # Get action parameter from event
        action = event.get('action')
        num_container = int(event.get('num_container'))
        #sum_container = int(event.get('sum_container'))
        cluster_name = event.get('cluster_name')
        name_service = event.get('name_service')

        if action is None:
            action = ''

        # if sum_container not in None:

        #     num_container = (sum_container + )
        # else:
        #     print ("Não Existe Soma")

        if action.lower() not in ['start']:
            print ("action was neither start. start_ecs() aborted.")

        else:

            try:
                #cluster_name = "bioritmo-smart-system-production"
                print("ARN Cluster " + cluster_name + " that can be start")
                #name_service = "bioritmo-smart-system-production-console"

                ecs.update_service(cluster=cluster_name,
                                    service=name_service,
                                    desiredCount = num_container
                                )

                print("Name Service " + name_service + " that can be start")
                print("Quantidades de conteiners para iniciar", (num_container))
                #print(json.dumps(result, indent=4, default=str))

            except Exception as e:
                displayException(e)

def displayException(exception):
    exception_type = exception.__class__.__name__
    exception_message = str(exception)

    print("Exception type: %s; Exception message: %s;" % (exception_type, exception_message))
