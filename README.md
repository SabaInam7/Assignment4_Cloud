# Assignment 4 – Cloud Computing
## Kubernetes-Based Web Application Deployment and Autoscaling

### 1. Project Overview

This project demonstrates the deployment, monitoring, performance evaluation, and horizontal autoscaling of a web application using Kubernetes and Minikube.

The application is deployed inside a Kubernetes cluster using Deployments and Services. Horizontal Pod Autoscaler (HPA) is configured to automatically scale the number of application replicas based on CPU utilization.

The project also includes performance experiments to evaluate response time, CPU utilization, request handling, and autoscaling behavior under different workloads.

### 2. Technologies Used

- Kubernetes
- Minikube
- Docker
- kubectl
- Node.js
- JavaScript
- Bash Shell Scripts
- CSV for experimental results
- Python / Matplotlib for graphs

### 3. Repository Structure

The repository is organized as follows:

```text
Assignment4_Cloud/
│
├── app/
│   ├── server.js
│   ├── package.json
│   ├── package-lock.json
│   └── public/
│       ├── index.html
│       └── script.js
│
├── k8s/
│   ├── Kubernetes deployment files
│   ├── Service configuration
│   ├── HPA configuration
│   └── Supporting configuration files
│
├── scripts/
│   ├── Experiment and deployment scripts
│   └── Testing and monitoring scripts
│
├── results/
│   ├── Experimental CSV files
│   └── Performance graphs
│
└── README.md
```

### 4. Prerequisites

Install the following tools before running the project:

- Docker
- Minikube
- kubectl
- Git

Verify the installations:

```bash
docker --version
minikube version
kubectl version --client
git --version
```

### 5. Running the Project on a Fresh Minikube Cluster

Follow these steps to deploy the complete system.

**Step 1: Clone the Repository**

```bash
git clone https://github.com/SabaInam7/Assignment4_Cloud.git
cd Assignment4_Cloud
```

**Step 2: Start Minikube**

```bash
minikube start --driver=docker
```

Verify that the cluster is running:

```bash
kubectl get nodes
```

**Step 3: Enable Metrics Server**

CPU-based autoscaling requires the Kubernetes Metrics Server.

```bash
minikube addons enable metrics-server
```

Wait for the metrics server to become ready.

**Step 4: Deploy the Complete Kubernetes System**

Apply all Kubernetes configuration files:

```bash
kubectl apply -f k8s/
```

This command applies the Kubernetes resources defined in the `k8s/` directory, including the application deployment, service, and autoscaling configuration.

**Step 5: Verify Deployment**

Check the Kubernetes resources:

```bash
kubectl get all -n emi
```

Check application pods:

```bash
kubectl get pods -n emi
```

Check deployment status:

```bash
kubectl get deployments -n emi
```

Check the service:

```bash
kubectl get services -n emi
```

Check Horizontal Pod Autoscaler:

```bash
kubectl get hpa -n emi
```

**Step 6: Access the Web Application**

Use the following command to access the application:

```bash
minikube service emi-web -n emi
```

Minikube will provide access to the deployed web application.

### 6. Monitoring and Autoscaling

The project uses Horizontal Pod Autoscaler (HPA) to adjust the number of application replicas according to CPU utilization.

Monitor the autoscaler:

```bash
kubectl get hpa -n emi -w
```

Monitor application pods:

```bash
kubectl get pods -n emi -w
```

Monitor CPU and memory utilization:

```bash
kubectl top pods -n emi
```

The number of replicas can increase or decrease automatically depending on the workload and configured scaling thresholds.

### 7. Performance Experiments

Multiple performance experiments were conducted to evaluate the application under different workloads and replica configurations.

The experiments include:

- Testing different request rates.
- Measuring average response time.
- Comparing performance with 1, 2, and 3 web replicas.
- Monitoring CPU utilization of individual pods.
- Evaluating request success rates.
- Observing automatic scaling behavior under increased workloads.

Experimental measurements are stored in the `results/` directory in CSV format.

### 8. Performance Graphs

The experimental results are used to generate the following graphs:

**Graph 1: Response Time vs Request Rate**

Compares average response time at different request rates using 1, 2, and 3 web replicas.

**Graph 2: CPU Utilization Over Time**

Shows CPU utilization of individual application pods during the 100 requests/second experiment with 3 replicas.

**Graph 3: Autoscaling Behavior**

Shows request rate, average CPU utilization, and number of web replicas over a 10-minute autoscaling experiment.

### 9. Repository Contents

| Directory | Description |
|---|---|
| `app/` | Web application source code |
| `k8s/` | Kubernetes deployment, service, and autoscaling configurations |
| `scripts/` | Automation, deployment, testing, and monitoring scripts |
| `results/` | Experimental CSV files and performance graphs |
| `README.md` | Project documentation and deployment instructions |

### 10. Stopping the Project

To stop the Minikube cluster:

```bash
minikube stop
```

To delete the Minikube cluster:

```bash
minikube delete
```

### 11. GitHub Repository

**Repository Name:** Assignment4_Cloud

**GitHub Link:**

https://github.com/SabaInam7/Assignment4_Cloud

### 12. Conclusion

This assignment demonstrates how a web application can be deployed and managed using Kubernetes on a Minikube cluster. It covers containerized application deployment, Kubernetes Services, horizontal pod autoscaling, workload testing, performance monitoring, and experimental analysis.

The project provides practical experience with cloud-native application deployment and resource management using Kubernetes.
