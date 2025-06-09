FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y git mariadb-client redis-server nodejs npm curl cron \
    && npm install -g yarn@1.22.19 \
    && useradd -ms /bin/bash frappe

COPY bootstrap.sh /bootstrap.sh
COPY ferum_customs /app/ferum_customs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /bootstrap.sh /entrypoint.sh

USER frappe
WORKDIR /home/frappe

RUN pip install --user frappe-bench \
    && ~/.local/bin/bench init frappe-bench --frappe-branch version-15 --skip-assets

ENV PATH="/home/frappe/.local/bin:$PATH"
ENTRYPOINT ["/entrypoint.sh"]
