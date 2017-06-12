import json
import cfnresponse
import boto3

responseData = {}
codeDeploy = boto3.client('codedeploy')

def lambda_handler(event,context):

    if event['RequestType'] == 'Delete':
        return cfnresponse.send(event, context, 'SUCCESS', 'DELETE RECEIVED', responseData)

    if event['RequestType'] == 'Create':
        print ("Received event:" + json.dumps(event,indent=2))
        deploymentGroup = event['ResourceProperties']['UpdateDeploymentGroup']
        appName = event['ResourceProperties']['ApplicationName']
        deploymenttriggerName = event['ResourceProperties']['DeploymentTriggerName']
        deploymenttargetArn = event['ResourceProperties']['TargetArn']
        alarmsArn = event['ResourceProperties']['Alarms']
        ignoreContinuePoll = event['ResourceProperties']['IgnoreContinue']
        eventsArray = event['ResourceProperties']['EventsArray']
        updateResponse = codeDeploy.update_deployment_group(
            applicationName = appName,
            currentDeploymentGroupName = deploymentGroup,
            triggerConfigurations = [
                {
                    'triggerName': deploymenttriggerName,
                    'triggerTargetArn': deploymenttargetArn,
                    'triggerEvents': eventsArray,
                },
            ],
            alarmConfiguration = {
                'enabled': True,
                'ignorePollAlarmFailure': ignoreContinuePoll,
                'alarms': [
                     {
                         'name': alarmsArn
                     },
                ]

           }
)
        print ("Received event:" + json.dumps(updateResponse,indent=2))
        return cfnresponse.send(event, context, 'SUCCESS', 'UPDATE HOOK COMPLETED', responseData)
