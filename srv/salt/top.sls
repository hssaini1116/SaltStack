base:
  'role:mongo-config':
    - match: grain
    - packages
    - mongodb.mongodbconfig

  'role:mongo-shard':
    - match: grain
    - packages
    - mongodb.mongodbshard

  'role:node-server':
    - match: grain
    - packages
    - mongodb.mongos
