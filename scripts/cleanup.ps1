# Removes only the resources created by this lab.
kubectl delete -f manifests/cronjob-app.yaml --ignore-not-found
kubectl delete -f manifests/job-app.yaml --ignore-not-found
kubectl delete -f manifests/job-app-fail.yaml --ignore-not-found
kubectl get pods
