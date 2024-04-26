# To read/write json content 
import json

# To access aws resource
import boto3

# Handles GET /groups request
def getgroups_handler(event, context):
    # Get dynamodb resource
	dynamodb = boto3.resource('dynamodb')
    
    # Get Groups table
	tableGroups = dynamodb.Table('Groups')

    # Scan the table for records
	response = tableGroups.scan()	
    
    # Return success with all the Groups records 
	return	{
		'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body':  json.dumps(response['Items'])
	}

# Handles GET /groups/{id}
def getgroup_handler(event, context):
    # Get dynamodb resource
	dynamodb = boto3.resource('dynamodb')
    
    # Get Groups table
	tableGroups = dynamodb.Table('Groups')

    # Get query parameters
	pathParameters = event['pathParameters']
    
	try:
        # Get the group from Groups table for the specified id 
		response = tableGroups.get_item(Key={'id': pathParameters['id']})	
        # Return success with the found group record
		return {
			'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body':  json.dumps(response['Item'])
		}
	except Exception as error:
        # Return failure
		return {
			'statusCode': 404,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Error getting the group')
		}
		
# Handles DELETE /groups/{id}
def deletegroup_handler(event, context):
    # Get dynamodb resource
	dynamodb = boto3.resource('dynamodb')
    
    # Get Groups table
	tableGroups = dynamodb.Table('Groups')

    # Get query parameters
	pathParameters = event['pathParameters']  
    
	try:
        # Delete the group from Groups table for the specified id  
		tableGroups.delete_item(
			Key={
				'id': pathParameters['id']
			}
		)

        # Return success 
		return {
			'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Successfully deleted the Group informaton!')
		}
	except Exception as error:
		# Return failure
		return {
			'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Error deleting the group')
		}

# Handles PUT /groups/{id}	
def updategroup_handler(event, context):
    # Get dynamodb resource
	dynamodb = boto3.resource('dynamodb')
    
    # Get Groups table
	tableGroups = dynamodb.Table('Groups')

    # Get query parameters
	pathParameters = event['pathParameters']  
 
    # Get payload
	body = json.loads(event['body'])
    
	try:
        # Update the group from Groups table for the specified id  
		tableGroups.update_item(
			Key={'id': pathParameters['id']},
            UpdateExpression="set #name = :n",
            ExpressionAttributeNames={
                "#name": "name"
            },
            ExpressionAttributeValues={
                ":n": body['name']
            }
		)

        # Return success
		return {
			'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Successfully updated the Group informaton!')
		}
	except Exception as error:
		# Return failure
		return {
			'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Error updating the group')
		}

# Handles POST /groups
def addgroup_handler(event, context):
    # Get dynamodb resource
	dynamodb = boto3.resource('dynamodb')
    
    # Get Groups table
	tableGroups = dynamodb.Table('Groups')
 
    # Get payload
	body = json.loads(event['body'])
	
	try:
        # Insert a group into Groups table
		tableGroups.put_item(
			Item={
				'id': body['id'],
				'name': body['name']
			}
		)

        # Return success
		return {
			'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Successfully inserted the Group informaton!')
		}
	except Exception as error:
        # Return failure
		return {
			'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json'
            },
			'body': json.dumps('Error saving the group')
		}
