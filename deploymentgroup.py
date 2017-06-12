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
        eventsArray = event['ResourceProperties']['EventsArray']
        alarmsArn = event['ResourceProperties']['Alarms']
        ignoreContinuePoll = event['ResourceProperties']['IgnoreContinue']
        if ignoreContinuePoll == 'True':
                              ignoreCont = True
        elif ignoreContinuePoll == 'False':
                              ignoreCont = False
        else:
             raise ValueError # Tell me something went wrong

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
                'enabled': 'True',
                'ignorePollAlarmFailure': ignoreCont,
                'alarms': [
                     {
                         'name': alarmsArn
                     },
                ]

           }
)
        print ("Received event:" + json.dumps(updateResponse,indent=2))
        return cfnresponse.send(event, context, 'SUCCESS', 'UPDATE HOOK COMPLETED', responseData)
