# Web image: build the interface, then serve it with nginx (non-root, port 8080).
# docker-compose service name: `web`; it expects the API service to be reachable as `api` on port 8000
# (see nginx.conf). Build context: this directory.
# Not built on the machine that wrote it (Docker was not installed there); the steps are the ones that
# `npm ci` and `vite build` ran by hand. Pin the image tags below to digests when you publish.

FROM node:24.22.1-alpine AS build
WORKDIR /app
COPY package.json package-lock.json .npmrc ./
RUN npm ci
# vite.config.ts imports mock/ and csp.ts at load time, so they are part of the build context;
# the mock is only used when VITE_MOCK=1, which this build never sets.
COPY index.html tsconfig.json vite.config.ts csp.ts ./
COPY mock ./mock
COPY src ./src
RUN npx vite build

FROM nginxinc/nginx-unprivileged:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1
