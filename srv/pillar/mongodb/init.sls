mongodb:
  use_repo: True
  version: 3.2
  repo_component: multiverse
  mongodb_package: mongodb-org
  mongo_directory: /mongodb
  replica_set:
    name: shard1RS
  config_svr: False
  shard_svr: True
  storage_engine: wiredTiger
  db_path: /mongodb/data
  log_path: /mongodb/log
  log_append: True
  conf_path: /etc/mongod.conf
  rest: True
  set_parameter:
    textSearchEnabled: 'true'
  settings:
    bind_ip: 127.0.0.1
    port: 27017

mongodb-config:
  use_repo: True
  version: 3.2
  repo_component: multiverse
  mongodb_package: mongodb-org
  mongo_directory: /mongodb
  replica_set:
    name: csReplSet
  config_svr: True
  shard_svr: False
  storage_engine: wiredTiger
  db_path: /mongodb/data
  log_path: /mongodb/log
  log_append: True
  conf_path: /etc/mongod.conf
  rest: True
  set_parameter:
    textSearchEnabled: 'true'
  settings:
    bind_ip: 127.0.0.1
    port: 27017
  
mongos:
  use_repo: True
  version: 3.2
  port: 27017
  repo_component: multiverse
  mongos_package: mongodb-org-mongos
  log_file: /mongodb/log/mongos.log
  config_svrs_repSet: "csReplSet/172.16.1.106:27017"
  conf_path: /etc/mongos.conf
