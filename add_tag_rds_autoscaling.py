import boto3
import traceback
import os

rds = boto3.client('rds')
sts = boto3.client('sts')
AWS_ACCOUNT_ID = sts.get_caller_identity()["Account"]
AWS_REGION = os.environ['AWS_REGION']

def lambda_handler(event, context):
    try:
        add_tag_rds_instances(event, context)
        return "Completed"

    except Exception as e:
            displayException(e)
            traceback.print_exc()

def add_tag_rds_instances(event, context):
    tag_key = event.get('tag_key') #"application-autoscaling:resourceId"

    instances_rds = rds.describe_db_instances().get('DBInstances', [])
    for instance_rds in instances_rds:
        try:
            if 'aurora' in instance_rds['Engine']:
                instanceState = instance_rds['DBInstanceStatus']
                tags = rds.list_tags_for_resource(ResourceName = instance_rds['DBInstanceArn']).get('TagList',[])
                if instanceState == 'available':
                    for tag in tags:
                        if tag['Key'] == tag_key:
                            if tag['Value'] == ("cluster:" + instance_rds['DBClusterIdentifier']):
                                tags_cluster = rds.list_tags_for_resource(ResourceName ="arn:aws:rds:" + AWS_REGION + ":" + AWS_ACCOUNT_ID + ":cluster:" + instance_rds['DBClusterIdentifier'])
                                print ("INFO - ARN INSTANCE RDS ADD TAG %s" % instance_rds['DBInstanceArn'])
                                print ("INFO - ARN CLUSTER RDS ADD TAG %s" % instance_rds['DBClusterIdentifier'])
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
