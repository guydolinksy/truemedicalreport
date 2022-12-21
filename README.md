# True Medical Report
TMR, or True Medical Report, is aimed at optimizing hospital staff's ability to manage their departments.

Recommended: 
1. Install Docker-Desktop, 
2. Enable Kubernetes,
3. Add NGINX Ingress Controller 
   - `helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace`
   - use `--set controller.service.ports.http=<port>` &  `--set controller.service.ports.https=<port>` for parallel docker nginx & k8s ingress
4. Install chart and access at ingress' ports.