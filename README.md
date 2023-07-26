# True Medical Report
TMR, or True Medical Report, is aimed at optimizing hospital staff's ability to manage their departments.

Setup using kubernetes: 
1. Install Docker-Desktop, 
2. Enable Kubernetes,
3. Add NGINX Ingress Controller 
   - `helm upgrade --install ingress-nginx ingress-nginx --repo https://kubernetes.github.io/ingress-nginx --namespace ingress-nginx --create-namespace`
   - use `--set controller.service.ports.http=<port>` &  `--set controller.service.ports.https=<port>` for parallel docker nginx & k8s ingress
4. Install chart and access at ingress' ports.

Setup using IDE:
To run the program we will need to run mongodb(docker), redis(docker), dal(python), digest(python), backend(python), frontend(npm).
1. Installations
   * Install docker-desktop
      * Enable kubernetes in settings
      * Pull images of mongodb (bitnami/mongodb) and redis (bitnami/redis)
   * Git clone the project and open in your IDE
      * Run pip install -e on the following packages under truemedicalreport/src: dev, backend, dal, sheba/digest
      * Run npm install in src/frontend/frontend
2. Configurations
   * Add environment variables in your IDE holding configurations’ requirements (each python package has congif.py requiring environment variables - you need to add the variables that don’t have default value)
   * Add proxy to src/frontend/frontend/package.json redirecting to chosen backend service (adding “proxy”: “ip/port” to the json )
   * If running without SQL connection for digest, add ‘“”’ as default value for digest’s config.py
3. Run
   * Run dockers using -p to choose the relevant port (21707 for mongo, 6379 for redis)
   * Run dal then digest and backend with python - wait for “Application startup complete”
   * Run frontend using npm
