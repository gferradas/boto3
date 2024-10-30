import boto3
import os

# Obtener las credenciales de las variables de entorno
#aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
#aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')

# Crear una sesión de boto3 con las credenciales de AWS
#session = boto3.Session(
    #aws_access_key_id=aws_access_key_id,
   # aws_secret_access_key=aws_secret_access_key,
 #   region_name='us-east-1'
#)

# Crear un cliente de EC2
ec2_client = boto3.client('ec2')

# Definir los parámetros para la instancia EC2
instance_params = {
    'ImageId': 'ami-06b21ccaeff8cd686',  
#'InstanceType': 't2.micro',
    'MinCount': 1,
    'MaxCount': 1,
    'SubnetId': 'subnet-0042388b5e53acc4e',
}

# Crear la instancia EC2
response = ec2_client.run_instances(**instance_params)

# Imprimir la información de la instancia creada
for instance in response['Instances']:
    print(f"Instancia creada con ID: {instance['InstanceId']}")