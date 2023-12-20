import boto3
import traceback

rds = boto3.client('rds')
sts = boto3.client('sts')
AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]

def lambda_handler(event, context):
    try:
        add_tag_rds_instances(event, context)
        return "Completed"

    except Exception as e:
            displayException(e)
            traceback.print_exc()

def add_tag_rds_instances(event, context):
    tag_key = event.get('tag_key') #"application-autoscaling:resourceId"
    cluster_rds = event.get('cluster_rds') #smartsystem-prd-qa-cluster

    instances_rds = rds.describe_db_instances().get('DBInstances', [])
    for instance_rds in instances_rds:
        try:
            if 'aurora' in instance_rds['Engine']:
                instanceState = instance_rds['DBInstanceStatus']
                tags = rds.list_tags_for_resource(ResourceName = instance_rds['DBInstanceArn']).get('TagList',[])
                if instanceState == 'available':
                    for tag in tags:
                        if tag['Key'] == tag_key:
                            if tag['Value'] == ("cluster:" + cluster_rds):
                                tags_cluster = rds.list_tags_for_resource(ResourceName ="arn:aws:rds:us-east-1:" + AWS_ACCOUNT_ID + ":cluster:" + cluster_rds)
                                print ("INFO - NAME CLUSTER RDS ADD TAG %s" % cluster_rds)
                                print ("INFO - ARN INSTANCE RDS ADD TAG %s" % instance_rds['DBInstanceArn'])
                                # print ("INFO - NAME INSTANCE RDS ADD TAG %s" % instance_rds['DBInstanceIdentifier'])
                                print (tags_cluster['TagList'])
                                responte = rds.add_tags_to_resource(
                                    ResourceName=instance_rds['DBInstanceArn'],
                                    Tags=tags_cluster['TagList'],
                                )
                                print ("INFO - ADD TAG %s" % responte)
                            else:
                                print ("INFO - NOT ADD TAG  %s is %s. " % (instance_rds['DBInstanceIdentifier'], instanceState))

        except Exception as e:
            displayException(e)
            traceback.print_exc()

def displayException(exception):
    exception_type = exception.__class__.__name__
    exception_message = str(exception)

    print("Exception type: %s; Exception message: %s;" % (exception_type, exception_message))
