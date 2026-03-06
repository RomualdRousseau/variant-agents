ARG NODE_VERSION=25
ARG NPM_VERSON=11.8.0

# Stage 1: Install dependencies
FROM node:${NODE_VERSION}-alpine AS deps
WORKDIR /app

RUN apk add --no-cache libc6-compat
RUN npm install -g npm@${NPM_VERSION}

COPY package.json package-lock.json* yarn.lock* pnpm-lock.yaml* ./
RUN \
  if [ -f package-lock.json ]; then npm ci; \
  elif [ -f yarn.lock ]; then yarn --frozen-lockfile; \
  elif [ -f pnpm-lock.yaml ]; then corepack enable pnpm && pnpm i --frozen-lockfile; \
  else npm install; \
  fi

# Stage 2: Build the app
FROM node:${NODE_VERSION}-alpine AS builder
WORKDIR /app

RUN npm install -g npm@${NPM_VERSION}

COPY --from=deps /app/node_modules ./node_modules
COPY . .

ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV="production"
ENV NEXT_PUBLIC_ENABLE_ANALYTICS="PLACEHOLDER_NEXT_PUBLIC_ENABLE_ANALYTICS"
ENV NEXT_PUBLIC_API_URL="https://PLACEHOLDER_NEXT_PUBLIC_API_HOST_AND_PORT"
ENV NEXT_PUBLIC_APP_URL="https://PLACEHOLDER_NEXT_PUBLIC_APP_HOST_AND_POST"
ENV NEXT_PUBLIC_FIREBASE_API_KEY="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_API_KEY"
ENV NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN"
ENV NEXT_PUBLIC_FIREBASE_PROJECT_ID="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_PROJECT_ID"
ENV NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET"
ENV NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID"
ENV NEXT_PUBLIC_FIREBASE_APP_ID="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_APP_ID"
ENV NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID="PLACEHOLDER_NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID"
ENV NEXT_PUBLIC_ALLOWED_DOMAINS="PLACEHOLDER_NEXT_PUBLIC_ALLOWED_DOMAINS"

RUN npm run build

# Stage 3: Runner
FROM node:${NODE_VERSION}-alpine AS runner
WORKDIR /app

RUN npm install -g npm@${NPM_VERSION}

ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

COPY --from=builder /app/entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/entrypoint.sh

EXPOSE 3000

ENTRYPOINT ["entrypoint.sh"]
CMD ["npm", "start"]

