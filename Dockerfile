# Tiny static server. Railway builds this automatically.
FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY public /srv
