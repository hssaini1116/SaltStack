base:
  'role:mongo-config':
    - match: grain
    - mongodb
  'role:mongo-shard':
    - match: grain
    - mongodb
  'role:node-server':
    - match: grain
    - mongodb
