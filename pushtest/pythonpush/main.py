from pyfcm import FCMNotification

push_service = FCMNotification(api_key="AAAAOYtUnXk:APA91bGSzC-3SOeVbEgiu3uV_udbcGYk2vzKW9UpCdEghFsMrQBzoePYinKJBrU9HHWeL0EvMRhdarnXcE3rHxtQWqJt5z4EAKJecSCtVL1rHMNTDKQQq1eM3XbZZrEgLHDkx36p3wT2")


push_service = FCMNotification(api_key="AAAAOYtUnXk:APA91bGSzC-3SOeVbEgiu3uV_udbcGYk2vzKW9UpCdEghFsMrQBzoePYinKJBrU9HHWeL0EvMRhdarnXcE3rHxtQWqJt5z4EAKJecSCtVL1rHMNTDKQQq1eM3XbZZrEgLHDkx36p3wT2")

# Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

registration_id = "eBAOp5UUQxiuA6F9NsKc5T:APA91bGomx0X63bpVmgoeLlVSfN-YJ4U6EeW_xlnVow0QrtuZQGuaOScLzXcmrRDo8n8ItoRMgn-T48ntTINPRIc8le20IIV_9GQY_-jlibIGHwblXiQ4Vx5Htu2YaehJLJt4e3CHTcQ"
message_title = "상황 발생 !!"
message_body = "상황 발생 !!"
result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

print (result)