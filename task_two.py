
import boto3
import time
import yagmail
import datetime

email_send         = 'email_send'

#------------------------------------------------------------------------------------
to_day             = datetime.datetime.today().strftime("%d-%m-%Y")
db_name            = 'PostgreSQL-' + to_day
db_master_username = 'db_name'
db_master_password = 'db_pass'
db_port            = 5432

#------------------------------------------------------------------------------------
print('Создаём db ' + db_name)

db = boto3.client('rds')

new_db = db.create_db_instance(
	DBInstanceIdentifier=db_name,
	AllocatedStorage=20,
	MaxAllocatedStorage=40,
	DBInstanceClass='db.t2.micro',
	Engine='postgres',
	MasterUsername=db_master_username,
	MasterUserPassword=db_master_password,
	VpcSecurityGroupIds=['sg-8d9243e9'],
	LicenseModel='postgresql-license',
	AvailabilityZone='us-east-2c',
	EngineVersion='11.5',
	BackupRetentionPeriod=7,
	PreferredBackupWindow='00:00-00:30',
	PubliclyAccessible=True,
	Port=db_port
)
time.sleep(1)

#------------------------------------------------------------------------------------
print('Ожидаем готовности db')

db_waiter = db.get_waiter('db_instance_available')
db_waiter.wait(DBInstanceIdentifier=db_name)
time.sleep(1)

#------------------------------------------------------------------------------------
print('Получаем dns подключения')

db_info = db.describe_db_instances(DBInstanceIdentifier=db_name)
db_dns  = db_info['DBInstances'][0]['Endpoint']['Address']
print (db_dns)
time.sleep(1)

#------------------------------------------------------------------------------------
print('Отправляем письмо')

login = 'email_dev'
passw = 'email_pass'

mail = yagmail.SMTP(login, passw)

contents_success = [                                                       
    'Ваша RDS база создана ' + db_name,
    'DNS подключения ' + db_dns + ":" + str(db_port),
    'Ваш Master username: ' + db_master_username,
    'Ваш Master password: ' + db_master_password
    ]

mail.send(email_send, 'Create RDS', contents_success)