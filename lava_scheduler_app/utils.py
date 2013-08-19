# Copyright (C) 2013 Linaro Limited
#
# Author: Neil Williams <neil.williams@linaro.org>
#         Senthil Kumaran <senthil.kumaran@linaro.org>
#
# This file is part of LAVA Scheduler.
#
# LAVA Scheduler is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License version 3 as
# published by the Free Software Foundation
#
# LAVA Scheduler is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with LAVA Scheduler.  If not, see <http://www.gnu.org/licenses/>.

import re
import copy
import socket
import urlparse
import simplejson


def split_multi_job(json_jobdata, target_group):
    node_json = {}
    all_nodes = {}
    node_actions = {}
    port = 3079
    if "device_group" in json_jobdata:
        # multinode node stage 1
        for actions in json_jobdata["actions"]:
            if "parameters" not in actions \
                    or 'role' not in actions["parameters"]:
                continue
            role = str(actions["parameters"]["role"])
            node_actions[role] = []

        position = 0
        for actions in json_jobdata["actions"]:
            if "parameters" not in actions \
                    or 'role' not in actions["parameters"]:
                # add to each node, e.g. submit_results
                if actions["command"] == "submit_results_on_host" \
                        or actions["command"] == "submit_results":
                    # If submit_result or submit_results_to_host has server
                    # hostname value as localhost/127.0.0.*, change it to the
                    # actual server FQDN.
                    # See https://cards.linaro.org/browse/LAVA-611
                    result_url = actions["parameters"]["server"]
                    host = urlparse.urlparse(result_url).netloc
                    if host == "localhost":
                        actions["parameters"]["server"] = result_url.replace(
                            "localhost", socket.getfqdn())
                    elif host.startswith("127.0.0"):
                        ip_pat = r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}'
                        actions["parameters"]["server"] = re.sub(
                            ip_pat, socket.getfqdn(), result_url)
                all_nodes[position] = actions
                position += 1
                continue
            role = str(actions["parameters"]["role"])
            actions["parameters"].pop('role', None)
            node_actions[role].append({"command": actions["command"],
                                       "parameters": actions["parameters"]})
        group_count = 0
        for clients in json_jobdata["device_group"]:
            group_count += int(clients["count"])
        for clients in json_jobdata["device_group"]:
            role = str(clients["role"])
            count = int(clients["count"])
            node_json[role] = []
            for c in range(0, count):
                node_json[role].append({})
                node_json[role][c]["timeout"] = json_jobdata["timeout"]
                node_json[role][c]["job_name"] = json_jobdata["job_name"]
                node_json[role][c]["tags"] = clients["tags"]
                node_json[role][c]["group_size"] = group_count
                node_json[role][c]["target_group"] = target_group
                if node_actions.get(role):
                    node_json[role][c]["actions"] = copy.deepcopy(
                        node_actions[role])
                all_nodes_action_positions = all_nodes.keys()
                all_nodes_action_positions.sort()
                for key in all_nodes_action_positions:
                    if node_json[role][c].get("actions"):
                        node_json[role][c]["actions"].append(all_nodes[key])
                    else:
                        node_json[role][c]["actions"] = [all_nodes[key]]

                node_json[role][c]["role"] = role
                # multinode node stage 2
                node_json[role][c]["logging_level"] = "DEBUG"
                node_json[role][c]["port"] = port
                node_json[role][c]["device_type"] = clients["device_type"]

        return node_json

    return 0


def requested_device_count(json_data):
    """Utility function check the requested number of devices for each
    device_type in a multinode job.

    JSON_DATA is the job definition string.

    Returns requested_device which is a dictionary of the following format:

    {'kvm': 1, 'qemu': 3, 'panda': 1}

    If the job is not a multinode job, then return None.
    """
    job_data = simplejson.loads(json_data)
    if 'device_group' in job_data:
        requested_devices = {}
        for device_group in job_data['device_group']:
            device_type = device_group['device_type']
            count = device_group['count']
            requested_devices[device_type] = count
        return requested_devices
    else:
        # TODO: Put logic to check whether we have requested devices attached
        #       to this lava-server, even if it is a single node job?
        return None
