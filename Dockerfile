FROM python:3.10-slim

RUN apt-get update \
    && apt-get purge -y fakeroot \
    && apt-get autoremove -y \
    && apt-get install -y git mariadb-client nodejs npm curl cron \
    && npm install -g yarn@1.22.19 \
    && useradd -ms /bin/bash frappe
# Install Redis before bench init
RUN apt-get update && apt-get install -y redis-server=5:7.0.*
RUN pip install --no-cache-dir pytest pytest-cov

COPY bench_setup.sh /bench_setup.sh
COPY bootstrap.sh /bootstrap.sh
COPY ferum_customs /app/ferum_customs
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /bootstrap.sh /bench_setup.sh /entrypoint.sh

USER frappe
ENV PATH="$HOME/.local/bin:$PATH"
RUN pip install --no-cache-dir frappe-bench==5.20.0
WORKDIR /home/frappe
RUN bench --version
RUN yarn config set registry https://registry.npmjs.org \
 && yarn config set network-timeout 600000
RUN bench init frappe-bench --frappe-branch version-15 --skip-assets && \
    cd frappe-bench && \
    bench get-app erpnext --branch version-15

# Pre-create a Frappe site during the image build so tests can reuse it
ARG SITE_NAME=test_site
ARG ADMIN_PASSWORD=admin
RUN cd frappe-bench && \
    bench get-app /app/ferum_customs && \
    bench new-site "$SITE_NAME" \
        --admin-password "$ADMIN_PASSWORD" \
        --no-mariadb-socket \
        --install-app erpnext \
        --install-app ferum_customs

WORKDIR /workspace

ENTRYPOINT ["/entrypoint.sh"]
