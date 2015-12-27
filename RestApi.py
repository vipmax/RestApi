#!/home/max/anaconda2/bin/python
import subprocess

from flask import Flask, jsonify, abort, request
from jinja2 import Template

app = Flask(__name__, static_url_path="")

vms = {
    'ram': '8192',
    'cpus': '4',
    'machine_count': '5'
}

template = Template("""---
{% for id in range(1, machine_count+1) %}
- name: {{ my_host_name }}{{ id }}
  ram: {{my_ram}}
  cpus: {{my_cpus}}
  ip: {{ my_base_ip_for_vms }}{{ id }}

{% endfor %}

""")

result = template.render(machine_count=int(vms['machine_count']), my_ram=vms['ram'], my_cpus=vms['cpus'],
                         my_host_name='{{my_host_name}}', my_base_ip_for_vms='{{my_base_ip_for_vms}}')


@app.route('/rest/vms/status', methods=['GET'])
def getStatus():
    print result
    return result


@app.route('/rest/vms/apply', methods=['GET'])
def applyConf():
    result = template.render(machine_count=int(vms['machine_count']), my_ram=vms['ram'], my_cpus=vms['cpus'],
                             my_host_name='{{my_host_name}}', my_base_ip_for_vms='{{my_base_ip_for_vms}}')
    print result


    import os
    os.chdir('/home/max/IdeaProjects/ansible-bdas/ansible-bdas')

    with open('templates/result.yml', 'w') as file:
        file.write(result)

    subprocess.call(["ansible-playbook", "deploy-cluster.yml"])


    return result


@app.route('/rest/vms/update', methods=['PUT'])
def updateConf():
    if not request.json:
        abort(400)

    vms['ram'] = request.json.get('ram')
    vms['cpus'] = request.json.get('cpus')
    vms['machine_count'] = request.json.get('machine_count')

    print('Updated! Current vms = ' + str(vms))

    return jsonify({'changed': 'true', 'vms': vms})

@app.route('/rest/vms/updateAndApply', methods=['PUT'])
def updateAndApplyConf():
    if not request.json:
        abort(400)

    vms['ram'] = request.json.get('ram')
    vms['cpus'] = request.json.get('cpus')
    vms['machine_count'] = request.json.get('machine_count')

    print('Updated! Current vms = ' + str(vms))

    applyConf()

    return jsonify({'changed': 'true', 'vms': vms})


if __name__ == '__main__':
    app.run(debug=True)
