composer archive create -a dist/crowdinfo-sandbox.bna --sourceType dir --sourceName .
composer network deploy -a dist/crowdinfo-sandbox.bna -p hlfv1 -i PeerAdmin -s randomString -A admin -S
