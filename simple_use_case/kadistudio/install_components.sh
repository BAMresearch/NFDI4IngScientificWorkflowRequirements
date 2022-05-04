#!/bin/bash

apt-get install -y git
python3 -m pip install git+https://gitlab.com/lars153/workflow-nodes.git@b1241467786a861919b73efb74763df130567644
wget https://gitlab.com/iam-cms/workflows/process-engine/-/jobs/1764662488/artifacts/download -O process_engine.zip
unzip process_engine.zip
sudo apt-get install --yes ./build/*.deb
rm build/*.deb
