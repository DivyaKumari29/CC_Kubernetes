# 3. Procedure

*Navigation: [README](../README.md) · [Fundamentals](01-kubernetes-fundamentals.md) · [Jobs & CronJobs](02-jobs-and-cronjobs-theory.md) · **Procedure** · [Results](04-observations-and-results.md) · [Viva](05-viva-questions.md)*

All commands were executed in **Windows PowerShell** from the repository root. Commands for macOS/Linux are identical except for the PowerShell-specific scripts.

---

## Phase A: Environment setup

### A.1 Install the tools

1. **Docker Desktop** (https://www.docker.com/products/docker-desktop): install, start it and wait until it reports *Engine running*.
2. **kubectl** and **minikube**:

```powershell
winget install Kubernetes.kubectl
winget install Kubernetes.minikube
```

3. Open a **new** terminal and verify:

```powershell
docker --version
kubectl version --client
minikube version
```

### A.2 Start the cluster

```powershell
minikube start --driver=docker
kubectl get nodes
kubectl config current-context
```

**Expected:** one node with `STATUS` = `Ready`, and the current context is `minikube`.

> **Note:** if the machine has other clusters (e.g. Docker Desktop's Kubernetes), always confirm that the current context is `minikube`, otherwise images built for minikube will not be found.

---

## Phase B: Build the application image

### B.1 Review the application

[`app/app.py`](../app/app.py) simulates a daily sales report. It generates 1000 random orders, prints the total, average and largest order, then exits. If the environment variable `FAIL=true` is set it exits with status `1` to simulate a failing task.

### B.2 Build the image and load it into minikube

```powershell
docker build -t batch-app:1.0 ./app
minikube image load batch-app:1.0
minikube image ls
```

**Expected:** `docker.io/library/batch-app:1.0` appears in the list.

> Manifests use `imagePullPolicy: IfNotPresent` so that Kubernetes uses this local image instead of trying to download it from a registry.

---

## Phase C: Experiment 1: Job (one-time batch task)

```powershell
kubectl apply -f manifests/job-app.yaml
kubectl get jobs --watch
```

Wait until `COMPLETIONS` shows `3/3` and the status is `Complete`; press `Ctrl+C`. Then:

```powershell
kubectl get pods
kubectl logs job/report-job
kubectl describe job report-job
```

**Expected:** three Pods in `Completed` state (one after another, because `parallelism: 1`) and the generated sales report in the log.

---

## Phase D: Experiment 2: CronJob (scheduled task)

```powershell
kubectl apply -f manifests/cronjob-app.yaml
kubectl get cronjob
```

Wait **3 to 4 minutes**, then:

```powershell
kubectl get jobs
kubectl get pods
kubectl logs <name-of-a-cronjob-pod>
```

**Expected:** a new Job `report-cronjob-<number>` appears every minute. Wait several more minutes and repeat `kubectl get jobs`: only the latest **3** successful runs remain (`successfulJobsHistoryLimit: 3`).

---

## Phase E: Experiment 3: Failing Job (retry behaviour)

```powershell
kubectl apply -f manifests/job-app-fail.yaml
kubectl get pods --watch
```

New Pods appear with status `Error`, with growing gaps between them. After about two minutes press `Ctrl+C` and run:

```powershell
kubectl get job report-fail-job
kubectl describe job report-fail-job
kubectl logs job/report-fail-job
```

**Expected:** `Pods Statuses: 0 Active / 0 Succeeded / 4 Failed`, a `Warning BackoffLimitExceeded` event, and the log line `ERROR: simulated failure`.

---

## Phase F: Collect the evidence

Either run the commands individually or use the helper script, which prints six labelled sections on one screen:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\show-results.ps1
```

| Item to demonstrate | Source |
|---|---|
| Job completion status | `kubectl get jobs` (Phase C) |
| Retry attempts | `kubectl get pods`, `kubectl describe job report-fail-job` (Phase E) |
| CronJob run history | `kubectl get jobs` after several minutes (Phase D) |
| Logs of finished Pods | `kubectl logs …` (Phases C, D, E) |

---

## Phase G: Clean-up

Take all screenshots **before** cleaning up. The CronJob keeps creating Pods every minute until it is deleted.

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\cleanup.ps1
minikube stop
```

---

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `ErrImagePull` / `ImagePullBackOff` | The image is not available inside the cluster's runtime | Build with `docker build`, then `minikube image load batch-app:1.0`; recreate the Job (`kubectl delete job …` then `apply`). Make sure `imagePullPolicy: IfNotPresent` is set. |
| Image visible in `minikube image ls` but Pod still cannot pull it | Image created with `minikube image build` was not visible to the runtime in this environment | Use the `docker build` + `minikube image load` method above |
| `docker: error during connect` | Docker Desktop is not running | Start Docker Desktop and wait for *Engine running* |
| `error parsing … yaml` | Tabs or wrong indentation | YAML allows spaces only; re-copy the file exactly |
| `'xyz' is not recognized as a command` flood | The **output** of a previous command was pasted into the terminal | Paste only commands, never output; run `cls` to clear |
| `running scripts is disabled` | PowerShell execution policy | `powershell -ExecutionPolicy Bypass -File .\scripts\show-results.ps1` |
| Cannot find `show-results.ps1` | Wrong folder or saved with `.txt` extension | Run `dir`; rename if necessary |

> Do **not** delete unrelated workloads that may already exist on the cluster; only the resources created by this lab are removed by `scripts/cleanup.ps1`.
