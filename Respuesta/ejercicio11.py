import boto3

def create_and_check_instance(nroestudiante, nombre, ami_id):
    script = "userdata.sh"
    # Crear instancia EC2
    ec2 = boto3.client('ec2')
    response = ec2.run_instances(
        ImageId=ami_id,
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': nroestudiante
                    }
                ]
            }
        ],
        UserData=open(script).read()
    )

    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instancia creada con ID: {instance_id}")

    # Comprobar con SSM
    ssm = boto3.client('ssm')

    # Comprobar usuario
    command_user = f"getent passwd {nombre}"
    response_user = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [command_user]}
    )
    command_id_user = response_user['Command']['CommandId']

    # Comprobar directorio
    command_dir = f"ls /tmp/{nroestudiante}"
    response_dir = ssm.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': [command_dir]}
    )
    command_id_dir = response_dir['Command']['CommandId']

    # Obtener resultados
    output_user = ssm.get_command_invocation(
        CommandId=command_id_user,
        InstanceId=instance_id
    )
    output_dir = ssm.get_command_invocation(
        CommandId=command_id_dir,
        InstanceId=instance_id
    )

    print(f"Resultado de la comprobación del usuario: {output_user['StandardOutputContent']}")
    print(f"Resultado de la comprobación del directorio: {output_dir['StandardOutputContent']}")

# Ejemplo de uso
create_and_check_instance("12345", "nombre_del_alumno", "ami-0abcdef1234567890")
