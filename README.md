## Live Demo

You can access the deployed version of this project here:

[http://34.135.180.212/](http://34.135.180.212/)

> Hosted on Google Kubernetes Engine (GKE) using Helm and Docker.

## Setup Steps

This project is a full-stack solar optimization tool featuring a React (TypeScript) frontend and a Django (Python) backend. It supports local development with or without Docker, and production deployment via Kubernetes and Helm.

---

### Local

#### 1. Configure Environment Variables

- **Frontend**
  - In the project root, copy `.env.example` and rename it to `.env`.
  - Set the `REACT_APP_Maps_API_KEY` to a valid Google Maps API key.

- **Backend**
  - In the `backend/` directory, copy `.env.example` and rename it to `.env`.
  - Set a secure value for `DJANGO_SECRET_KEY`.

#### 2. Run Locally with Docker

```bash
docker compose build
docker compose up -d
```

> Ensure that ports `80`, `3000`, and `8000` are free on your machine.

Once running, access the application via [http://localhost](http://localhost).

#### 3. Run Locally Without Docker

- **Backend**

```bash
cd backend
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver 0.0.0.0:8000
```

- **Frontend**

```bash
cd frontend
nvm use 22.15.0
npm install
npm start
```

---

### Production Deployment

#### 1. Configure Environment Variables

- **Frontend**
  - In the project root, copy `.env.example` and rename it to `.env`.
  - Set the `REACT_APP_Maps_API_KEY` to a valid Google Maps API key.

#### 2. Build and Tag Docker Images

```bash
docker compose build

docker tag solar-backend:latest <your-backend-repo>:<backend-tag>
docker tag solar-frontend:latest <your-frontend-repo>:<frontend-tag>
```

#### 3. Push Images to Docker Hub

```bash
docker push <your-backend-repo>:<backend-tag>
docker push <your-frontend-repo>:<frontend-tag>
```

#### 4. Prepare Helm Configuration

- In the root directory, copy `values-prod.yaml.example` and rename it to `values-prod.yaml`.
- Update the image repositories, tags, and environment values accordingly.

#### 5. Deploy to Kubernetes (e.g., GKE)

```bash
gcloud container clusters create-auto <cluster-name> \
  --region=<region-name> \
  --project=<project-id>

helm install <instance-name> helm-chart/ -f values-prod.yaml
```

> Ensure that `kubectl`, `gcloud`, and `helm` are installed and properly configured for your cloud environment.

## Architecture Decisions

This project is organized as a modular, scalable full-stack application. It includes a Django REST API backend, a React (TypeScript) frontend, and Kubernetes manifests for deployment via Helm.

---

### Backend Architecture (Django + DRF)

- **Core Design**:
  - The API layer uses Django REST Framework (`APIView`) to handle incoming requests.
  - User input is validated using `serializers`, and passed to a centralized logic module (`SolarCalculator`) for processing.
  - Results are again validated using output serializers before being returned to the frontend.

- **Business Logic**:
  - The core logic is encapsulated in a utility class `SolarCalculator`, acting as a facade/interface to multiple underlying solar models.
  - Models are defined in a dedicated `solar_models` submodule.
  - All models inherit from a common abstract base class, which enforces implementation of a `calculate_optimal_angles()` method.
  - This ensures all models can be called in a unified way by the `SolarCalculator`.

- **Backend Directory Structure**:
  ```
  backend/
  └── solar_calculator/
      ├── views.py                     # API endpoint (DRF APIView)
      ├── serializers.py               # Input/output validation
      └── utils/
          ├── solar_calculator.py      # SolarCalculator interface
          └── solar_models/
              ├── __init__.py          # Abstract model base class
              ├── liu_jordan_model.py  # Liu and Jordan model implementation
              ├── nrel_model.py        # NREL model (placeholder)
              └── pvlib_model.py       # PVLib model (placeholder)
  ```

- **Testing**:
  - Tests are located in: `./backend/solar_calculator/tests/`
  - Run with:  
    ```bash
    python manage.py test
    ```

- **Deployment**:
  - Dockerfile: `./backend/Dockerfile`
  - Uses Python 3.12 and Gunicorn for production WSGI serving.

---

### Frontend Architecture (React + TypeScript)

- **Core Design**:
  - Built with Create React App using TypeScript.
  - Uses controlled components for input forms and integrates Google Maps for geographic coordinate selection.
  - The output of solar panel angle calculations centralized under `types.ts` for consistency and type safety.

- **Frontend Directory Structure**:
  ```
  frontend/
  └── src/
      ├── App.tsx                     # Main application entry
      ├── layouts/
      │   └── Index.tsx              # Page layout wrapper
      ├── components/
      │   ├── Header.tsx             # Simple page header
      │   ├── Form.tsx               # Input form for user data
      │   ├── Map.tsx                # Google Map integration
      │   ├── Calculators.tsx        # Aggregated results view
      │   └── Calculator.tsx         # Individual model result
      ├── types/
      │   └── types.ts               # Shared TypeScript interfaces
      └── __tests__/                 # Frontend unit tests
  ```

- **Testing**:
  - Tests located in: `./frontend/src/__tests__/`
  - Run with:
    ```bash
    npm run test
    ```

- **Deployment**:
  - Dockerfile: `./frontend/Dockerfile`
  - Uses Node.js 22 for build and Nginx to serve production assets.

---

### Kubernetes Deployment (Helm)

- **Helm Chart Location**: `./helm-chart/`
- **Key Files**:
  ```
  helm-chart/
  ├── templates/
  │   ├── backend-configmap.yaml           # Backend environment config
  │   ├── backend-secret.yaml              # Backend secrets (e.g. Django secret key)
  │   ├── backend-deployment.yaml          # Backend deployment spec
  │   ├── frontend-deployment.yaml         # Frontend deployment spec
  │   ├── frontend-nginx-configmap.yaml    # Custom Nginx config for frontend
  ├── nginx.conf                            # Nginx config
  ├── values.yaml                           # Default values (overridden in prod)
  ```

- **Notes**:
  - The Helm chart supports both development and production use cases.
  - Sensitive values (e.g., API keys, secrets) are managed via ConfigMaps and Secrets.
  - `values-prod.yaml` should be created from `values-prod.yaml.example` and customized per environment.

## Assumptions and Known Limitations

1. **Google Maps API Key Exposure in Frontend**  
   The API key is injected at build time due to Create React App (CRA) behavior, which embeds environment variables directly into the compiled code. This means the key is accessible in the browser — not ideal for security.  
   A better approach would be to inject the key at runtime using an `env-config.js` pattern:
   - Serve the key as `window.__env__` via a shell script in the Docker container.
   - Inject this script in `index.html` before the React app mounts.
   - Access the key in the React code via `window.__env__.REACT_APP_Maps_API_KEY`.  
   This runtime config strategy was not implemented due to time constraints.

2. **Google Maps API Key Usage Policy**  
   It is assumed that the provided API key is:
   - Restricted to the correct publick domain or IP.
   - Subject to usage quotas to avoid cost overruns.

3. **Missing Production-Grade Scaling Configuration**  
   The current Helm setup lacks resource limits, requests, and autoscaling rules for frontend and backend services. These should be added in a production environment to ensure stability under load and to avoid overutilization.

4. **Bot Protection Not Implemented**  
   The application is susceptible to automated abuse:
   - Excessive page reloads or map usage could consume quota or incur API costs.
   - ReCAPTCHA and Google Cloud Armor (WAF) can be added to protect both GET (map load) and POST (form submission) endpoints.
   These protections were not implemented due to time constraints.

5. **Partial Implementation of Solar Models**  
   - The Liu–Jordan and NREL models are currently placeholder implementations.
   - They use simplified logic and do not reflect the full modeling capabilities.
   - These should be fully implemented in a production version for accuracy and scientific reliability.

## Solar Modeling Logic and References

### Baseline Rule-of-Thumb Logic

The simplest estimation method implemented in this project follows general rules widely accepted for solar panel installation in North America:

- **Azimuth**:
  - Set to **180° (south-facing)** for locations in the **Northern Hemisphere**.
  - Set to **0° (north-facing)** for locations in the **Southern Hemisphere**.
  - Reference: [EcoFlow – Solar Panel Angle Guide](https://www.ecoflow.com/us/blog/solar-panel-angle-north-america)

- **Pitch (Tilt)**:
  - If an `offset_angle` is provided:  
    → Use `offset_angle` as the panel pitch.
  - If `offset_angle` is not provided:  
    → Use the **latitude** of the location as the pitch.  
  - Reference: [Greenvolt – Solar Panel Orientation](https://next.greenvolt.com/2024/05/27/solar-panel-orientation/)

This rule-of-thumb logic is currently used as the default calculation in the placeholder implementations of the **NREL** and **Liu–Jordan** models.

---

### PVLib-Based Model

The PVLib model is a more advanced and realistic solar geometry estimator. The following steps are applied:

1. **Location Setup**  
   - The geographic location (latitude and longitude) is passed to `pvlib.location.Location`.
   - Timezone and elevation are determined using PVLib utilities.

2. **Solar and Irradiance Data**  
   - **Solar position** and **clear sky irradiance** data are generated at **hourly frequency** for the current year using PVLib’s built-in models.

3. **Initial Estimate**  
   - Initial azimuth and pitch are derived using the rule-of-thumb logic described above.

4. **Optimization Strategy**  
   - If `offset_angle = 0`:  
     → The model searches for the **optimal pitch** by maximizing POA across a range of tilt angles.
   - If `offset_angle > 0`:  
     → The model searches for the **optimal azimuth** that maximizes annual POA irradiance.


---

### Future Improvements

- Complete the implementation of NREL and Liu–Jordan models with accurate solar geometry and irradiance models.
- Introduce terrain and horizon modeling to adjust tilt/azimuth dynamically.
- Incorporate more granular weather and insolation datasets via external APIs (e.g., SolarAnywhere, NREL NSRDB).


