### For Arch:
#### xm2cloud_webui is a powerful and graceful webui component for xm2cloud devops framework.

### For Check:
```json
[
    "and", 
    [
        "<=", 
        {
            "path": "mem.memfree", 
            "func_args": [
                "5m"
            ], 
            "path_args": { }, 
            "func": "avg", 
            "uuid": "{{uuid}}"
        }, 
        512000
    ], 
    [
        ">=", 
        {
            "path": "df.bytes.used.percentage", 
            "func_args": [
                "5m"
            ], 
            "path_args": {
                "device": "sdb", 
                "mount": "/var/lib/docker"
            }, 
            "func": "avg", 
            "uuid": "{{uuid}}"
        }, 
        90
    ]
]
```

### For Webui:
![ui_login](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_login.png)
![ui_profile](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_profile.png)
![ui_security](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_security.png)
![ui_cluster](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_cluster.png)
![ui_cluster_modify](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_cluster_modify.png)
![ui_hostgroup](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_hostgroup.png)
![ui_host](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_host.png)
![ui_host_network](https://raw.githubusercontent.com/xm2cloud/xm2cloud_webui/master/docs/screenshot/ui_host_network.png)
### For Debug:


### For Deploy:
```yaml
version: 0.0
os: linux
files:
  - source: /
    destination: /var/www/html/WordPress
hooks:
  BeforeInstall:
    - location: scripts/install_dependencies.sh
      timeout: 300
      runas: root
  AfterInstall:
    - location: scripts/change_permissions.sh
      timeout: 300
      runas: root
  ApplicationStart:
    - location: scripts/start_server.sh
      timeout: 300
      runas: root
  ApplicationStop:
    - location: scripts/stop_server.sh
      timeout: 300
      runas: root
```
