# 5. Viva Questions and Answers

*Navigation: [README](../README.md) · [Fundamentals](01-kubernetes-fundamentals.md) · [Jobs & CronJobs](02-jobs-and-cronjobs-theory.md) · [Procedure](03-procedure.md) · [Results](04-observations-and-results.md) · **Viva***

## A. Kubernetes basics

1. **What is Kubernetes?**
   An open-source container orchestration platform that automatically runs, heals and scales containers across a group of machines.

2. **What is the difference between the control plane and a worker node?**
   The control plane stores the cluster state and decides what should happen; worker nodes run the applications inside Pods.

3. **Which component chooses the node for a new Pod?**
   The Scheduler (filter → score → bind).

4. **Where is the state of the cluster stored?**
   In etcd; only the API Server talks to etcd.

5. **What is a Pod?**
   The smallest deployable unit; it wraps one or more containers that share network and storage.

6. **Pods already have IP addresses, so why is a Service needed?**
   Pods are replaced often and each new Pod gets a new IP. A Service provides one stable name/IP and spreads traffic across matching Pods.

7. **A node has 1.5 CPU unreserved. Can a Pod requesting 2 CPU be placed there?**
   No; the Scheduler reserves requests, so it would choose another node.

8. **What happens if a container exceeds its memory limit?**
   It is stopped and restarted. Exceeding the CPU limit only throttles it.

9. **You asked for 3 replicas and one Pod crashes. What happens?**
   The controller notices 2 of 3 are running and creates a replacement Pod, which the Scheduler places on a node.

10. **Why is a cluster preferred over a single machine?**
    Higher capacity, self-healing if a node fails, and one stable address for users.

## B. Jobs and CronJobs

11. **What is a Job?**
    A Kubernetes object that runs Pods until a specified number complete successfully, then stops.

12. **How does a Job differ from a Deployment?**
    A Deployment keeps Pods running continuously and restarts them when they exit; a Job runs to completion and then stops.

13. **What do `completions` and `parallelism` mean?**
    `completions` is the number of successful Pod runs required; `parallelism` is how many Pods may run at the same time.

14. **What is `backoffLimit`?**
    The maximum number of retries before the Job is marked Failed. With `backoffLimit: 3`, up to 4 Pods are created.

15. **Why can a Job use only `restartPolicy: Never` or `OnFailure`?**
    `Always` would restart a finished container forever, which contradicts run-to-completion.

16. **What is exponential back-off?**
    The delay between retries grows (about 10 s, 20 s, 40 s …) so a failing task does not overload the cluster. In our run the observed gaps were 12 s, 21 s and 41 s.

17. **What is a CronJob?**
    An object that creates Jobs on a repeating schedule written in cron syntax.

18. **What does `*/1 * * * *` mean?**
    Run every minute.

19. **What do `successfulJobsHistoryLimit` and `failedJobsHistoryLimit` do?**
    They set how many finished successful/failed Jobs are kept; older ones are deleted automatically.

20. **Name two real-world uses of Jobs and CronJobs.**
    Report generation, database backups, data migration, log clean-up.

## C. Experiment-specific

21. **Why did we use `imagePullPolicy: IfNotPresent`?**
    The image exists only in the local cluster; this policy tells Kubernetes not to try to pull it from a remote registry.

22. **How did you simulate a failure?**
    By passing `FAIL=true` as an environment variable, which makes `app.py` exit with status 1.

23. **What does `BackoffLimitExceeded` mean?**
    The Job controller reached the retry limit and stopped creating Pods; the Job is marked Failed.

24. **How did you view the output of a finished Pod?**
    With `kubectl logs <pod>` or `kubectl logs job/<job-name>`. Completed Pods keep their logs until they are deleted.
