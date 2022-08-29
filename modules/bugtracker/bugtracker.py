import json

from core.elements import Url, ErrorMessage
from core.utils import get_url


async def bugtracker_get(mojiraId: str):
    data = {}
    id_ = mojiraId.upper()
    json_url = f'https://bugs.mojang.com/rest/api/2/issue/{id_}'
    get_json = await get_url(json_url, 200)
    get_spx = await get_url('https://bugs.guangyaostore.com/translations', 200)
    if get_spx:
        spx = json.loads(get_spx)
        if id_ in spx:
            data["translation"] = spx[id_]
    if not get_json:
        return ErrorMessage('获取Json失败。')
    load_json = json.loads(get_json)
    errmsg = ''
    if 'errorMessages' in load_json:
        for msg in load_json['errorMessages']:
            errmsg += '\n' + msg
    else:
        if 'key' in load_json:
            data["title"] = f'[{load_json["key"]}] '
        if 'fields' in load_json:
            fields = load_json['fields']
            if 'summary' in fields:
                data["title"] = data["title"] + \
                                fields['summary'] + (
                                    f' ({data["translation"]})' if data.get("translation", False) else '')
            if 'issuetype' in fields:
                data["type"] = fields['issuetype']['name']
            if 'status' in fields:
                data["status"] = fields['status']['name']
            if 'project' in fields:
                data["project"] = fields['project']['name']
            if 'resolution' in fields:
                data["resolution"] = fields['resolution']['name'] if fields[
                                                                         'resolution'] is not None else 'Unresolved'
            if 'versions' in load_json['fields']:
                Versions = fields['versions']
                verlist = [item['name'] for item in Versions[:]]
                data['version'] = (
                    f"Version: {verlist[0]}"
                    if verlist[0] == verlist[-1]
                    else "Versions: " + verlist[0] + " ~ " + verlist[-1]
                )

            data["link"] = f'https://bugs.mojang.com/browse/{id_}'
            if 'customfield_12200' in fields and fields['customfield_12200']:
                data["priority"] = "Mojang Priority: " + \
                                   fields['customfield_12200']['value']
            if 'priority' in fields and fields['priority']:
                data["priority"] = "Priority: " + fields['priority']['name']
            if (
                'fixVersions' in fields
                and data["status"] == 'Resolved'
                and fields['fixVersions']
            ):
                data["fixversion"] = fields['fixVersions'][0]['name']
    msglist = []
    if errmsg != '':
        msglist.append(errmsg)
    else:
        if title := data.get("title", False):
            msglist.append(title)
        if type_ := data.get("type", False):
            type_ = f'Type: {type_}'
            if status_ := data.get("status", False):
                if status_ in ['Open', 'Resolved']:
                    Type = f'{type_} | Status: {status_}'
            msglist.append(type_)
        if project := data.get("project", False):
            project = f'Project: {project}'
            msglist.append(project)
        if status_ := data.get("status", False):
            if status_ not in ['Open', 'Resolved']:
                status_ = f'Status: {status_}'
                msglist.append(status_)
        if priority := data.get("priority", False):
            msglist.append(priority)
        if resolution := data.get("resolution", False):
            resolution = f"Resolution: {resolution}"
            msglist.append(resolution)
        if fixversion := data.get("fixversion", False):
            msglist.append(f"Fixed Version: {fixversion}")
        if version := data.get("version", False):
            msglist.append(version)
        if link := data.get("link", False):
            msglist.append(str(Url(link)))
    msg = '\n'.join(msglist)
    return msg
