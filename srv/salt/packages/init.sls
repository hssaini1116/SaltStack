random_packages:
  pkg.installed:
    - pkgs:
      - unzip
      - python-pip
      - gcc
      - python-dev
      - htop
      - supervisor
      - iotop
      - git
      - ntp
    
{% if grains['role']  == 'node-server' %}
random_packages_mongos:
  pkg.installed:
    - pkgs:
      - mongodb-org-shell
      - mongodb-org-tools

boto:
  pip.installed    
slacker:
  pip.installed
pymongo:
  pip.installed
{% endif %}

