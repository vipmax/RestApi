get current config:
curl -i http://localhost:5000/rest/vms/status

update config:
curl -i -H "Content-Type: application/json" -X PUT -d '{"machine_count": "5","cpus": "2","ram": "4096"}' http://localhost:5000/rest/vms/update

apply current config:
curl -i http://localhost:5000/rest/vms/apply

update and apply config:
curl -i -H "Content-Type: application/json" -X PUT -d '{"machine_count": "5","cpus": "2","ram": "4096"}' http://localhost:5000/rest/vms/updateAndApply