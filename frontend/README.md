# Genomics Agent Frontend

This is the frontend for the Genomics Agent application, a Next.js project designed to provide a user interface for genomic data analysis and interaction with the backend services.

## Prerequisites

Before you begin, ensure you have the following tools installed on your system:

-   [Node.js](https://nodejs.org/) (v25 or later recommended)
-   [npm](https://www.npmjs.com/) (v11.8.0 or later recommended)
-   [just](https://github.com/casey/just)
-   [Google Cloud SDK (`gcloud`)](https://cloud.google.com/sdk/docs/install)
-   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)
-   [Docker](https://docs.docker.com/get-docker/)

## Getting Started

### 1. Clone the Repository

```bash
git clone <repository-url>
cd frontend
```

### 2. Install Dependencies

Install the project dependencies using npm:

```bash
npm install
```

### 3. Configure Environment Variables

Create a `.env` file by copying the example file:

```bash
cp .env.example .env
```

Now, open the `.env` file and replace the placeholder values with your actual configuration for Firebase, API endpoints, and other settings.

The following variables are available:

-   `GOOGLE_CLOUD_PROJECT`: Your Google Cloud project ID.
-   `GOOGLE_CLOUD_LOCATION`: The Google Cloud region for your resources (e.g., `europe-west1`).
-   `NEXT_PUBLIC_FIREBASE_API_KEY`: Your Firebase project's API key.
-   `NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID`: Your Firebase messaging sender ID.
-   `NEXT_PUBLIC_FIREBASE_APP_ID`: Your Firebase web app ID.
-   `NEXT_PUBLIC_FIREBASE_MEASUREMENT_ID`: Your Firebase measurement ID for Google Analytics.
-   `NEXT_PUBLIC_API_HOST_AND_PORT`: The full URL for your backend API.
-   `NEXT_PUBLIC_APP_HOST_AND_PORT`: The public URL of this frontend application.
-   `NEXT_PUBLIC_ALLOWED_DOMAINS`: A comma-separated list of email domains allowed to sign up (e.g., `google.com,your-company.com`).
-   `NEXT_PUBLIC_ENABLE_ANALYTICS`: Set to `true` to enable analytics.
-   `NEXT_PUBLIC_ENABLE_EMAIL_VERIFICATION`: Set to `true` to require email verification for new users.

### 4. Run the Development Server

Start the local development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the application.

## Deployment

This project uses `just` for orchestrating build and deployment tasks to Google Kubernetes Engine (GKE).

### Build and Push the Image

The following command will build the frontend Docker image and push it to your configured Google Artifact Registry. Ensure your `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` environment variables are set correctly in your shell or `.env` file.

```bash
just build
```

### Deploy to GKE

This command applies the Kubernetes deployment configuration. It uses `envsubst` to substitute environment variables from `gke/genomics-deployment.yaml` and then applies it, followed by a rolling restart of the deployment.

```bash
just deploy
```
