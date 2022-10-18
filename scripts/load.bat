docker load < images.docker
docker tag guydo/tmr-backend:dev harbor.arc-devops.sheba.gov.il/tmr/backcend:dev
docker tag guydo/tmr-frontend:dev harbor.arc-devops.sheba.gov.il/tmr/frontend:dev
docker tag guydo/tmr-dal:dev harbor.arc-devops.sheba.gov.il/tmr/dal:dev
docker tag guydo/tmr-sheba-digest:dev harbor.arc-devops.sheba.gov.il/tmr/sheba-digest:dev
docker tag guydo/tmr-sheba-arc:dev harbor.arc-devops.sheba.gov.il/tmr/sheba-arc:dev
docker tag guydo/tmr-sheba-chameleon:dev harbor.arc-devops.sheba.gov.il/tmr/sheba-chameleon:dev
docker tag guydo/tmr-sheba-faker:dev harbor.arc-devops.sheba.gov.il/tmr/sheba-faker:dev

docker tag guydo/tmr-backend:latest harbor.arc-devops.sheba.gov.il/tmr/backcend:latest
docker tag guydo/tmr-frontend:latest harbor.arc-devops.sheba.gov.il/tmr/frontend:latest
docker tag guydo/tmr-dal:latest harbor.arc-devops.sheba.gov.il/tmr/dal:latest
docker tag guydo/tmr-sheba-digest:latest harbor.arc-devops.sheba.gov.il/tmr/sheba-digest:latest


docker push harbor.arc-devops.sheba.gov.il/tmr/backcend:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/frontend:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/dal:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/sheba-digest:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/sheba-arc:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/sheba-chameleon:dev
docker push harbor.arc-devops.sheba.gov.il/tmr/sheba-faker:dev

docker push harbor.arc-devops.sheba.gov.il/tmr/backcend:latest
docker push harbor.arc-devops.sheba.gov.il/tmr/frontend:latest
docker push harbor.arc-devops.sheba.gov.il/tmr/dal:latest
docker push harbor.arc-devops.sheba.gov.il/tmr/sheba-digest:latest