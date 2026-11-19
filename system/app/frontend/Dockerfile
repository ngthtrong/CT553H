# syntax=docker/dockerfile:1
# Web image. Build context: this directory (system/app/frontend).
#
# Targets
#   runtime (default)  build the interface, then serve it with nginx (non-root, port 8080). nginx proxies /v1 and
#                      /healthz to the compose service `api` on port 8000 (nginx.conf), so the browser talks to one origin.
#   dev                Vite dev server with hot reload; the source is a bind mount (compose.dev.yml) and node_modules
#                      lives in a named volume, because the musl binaries of esbuild/rollup differ from the host's.
FROM node:24.22.1-alpine AS deps
USER node
WORKDIR /app
COPY --chown=node:node package.json package-lock.json .npmrc ./
RUN npm ci --no-audit

# ---------------------------------------------------------------------------------------------------- dev
FROM deps AS dev
ENV API_TARGET=http://api:8000
EXPOSE 5173
# Reinstall only when the lock file is newer than the installed tree (a fresh named volume copies the image's tree).
CMD ["sh", "-c", "[ package-lock.json -nt node_modules/.package-lock.json ] && npm ci --no-audit; exec npx vite --host 0.0.0.0"]

# ---------------------------------------------------------------------------------------------------- build
FROM deps AS build
# vite.config.ts imports mock/ and csp.ts at load time, so they are part of the build context;
# the mock is only used when VITE_MOCK=1, which this build never sets.
COPY --chown=node:node index.html tsconfig.json vite.config.ts csp.ts ./
COPY --chown=node:node mock ./mock
COPY --chown=node:node src ./src
RUN npx tsc --noEmit && npx vite build

# ---------------------------------------------------------------------------------------------------- runtime
FROM nginxinc/nginx-unprivileged:1.27-alpine AS runtime
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s CMD wget -q -O /dev/null http://127.0.0.1:8080/ || exit 1
