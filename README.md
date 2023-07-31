# Cloud-Computing-3031-Ex1
## How to use the parking app:
1. Configure AWS CLI in your local machine, create IAM user and get key and secret.
2. Download deploy-parking-app.sh and execute it.
3. Get the public IP from the output.

## Testing:
Use the following two POST methods to test the parking app:
1. http://{{publicIP}}:5000/entry?plate=122-123-123&parkingLot=381- will return a ticket id
2. http://{{publicIP}}:5000/exit?ticketId={{ticketId}}- will return the parking details: plate, parked time (in minutes), the parking lot and the charge.
3. Enjoy!
