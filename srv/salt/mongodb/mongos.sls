{% set ms = pillar.get('mongos', {}) -%}

mongos_package:
{% if ms.use_repo %}
  pkgrepo.managed:
    - humanname: MongoDB.org Repo
    - name: deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/{{ ms.version }} {{ ms.repo_component }}
    - file: /etc/apt/sources.list.d/mongodb.list
    - keyid: EA312927
    - keyserver: keyserver.ubuntu.com
{% endif %}
  pkg.installed:
     - name: {{ ms.mongos_package }}

mongos_log_path:
  file.directory:
    - name: /mongodb/log
    - user: root
    - group: root
    - mode: 755
    - makedirs: True

mongos_init:
  file.managed:
    - name: /etc/init/mongos.conf
    - source: salt://mongodb/files/mongos.upstart.conf.jinja
    - template: jinja

mongos_service:
  service.running:
    - name: mongos
    - enable: True
    - watch:
      - file: mongos_configuration

mongos_configuration:
  file.managed:
    - name: {{ ms.conf_path }}
    - user: root
    - group: root
    - mode: 644
    - source: salt://mongodb/files/mongos.conf.jinja
    - template: jinja

mongos_mongo_dump_path::
  file.directory:
    - name: /data/backup
    - user: root
    - group: root
    - mode: 755
    - makedirs: True
