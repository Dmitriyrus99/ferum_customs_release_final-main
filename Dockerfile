FROM python:3.10-slim

RUN apt-get update \
    && apt-get purge -y fakeroot \
    && apt-get autoremove -y \
    && apt-get install -y git mariadb-client nodejs npm curl cron \
    && npm install -g yarn@1.22.19 \
    && useradd -ms /bin/bash frappe
RUN pip install --no-cache-dir pytest pytest-cov

COPY bench_setup.sh /bench_setup.sh
COPY bootstrap.sh /bootstrap.sh
COPY ferum_customs /app/ferum_customs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /bootstrap.sh /bench_setup.sh /entrypoint.sh

USER frappe
WORKDIR /home/frappe

RUN pip install --no-cache-dir --user frappe-bench
ENV PATH=$PATH:/home/frappe/.local/bin
RUN bench --version
RUN yarn config set registry https://registry.npmjs.org \
 && yarn config set network-timeout 600000
RUN bench init frappe-bench --frappe-branch version-15 --skip-assets && \
    cd frappe-bench && \
    bench get-app erpnext --branch version-15

ENTRYPOINT ["/entrypoint.sh"]
