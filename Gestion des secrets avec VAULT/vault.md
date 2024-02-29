1)

# vault operator init
................................................................................
 vault operator init
Unseal Key 1: 0lcVTO8wMjInnbh3mdddlhGq6M2t34lprKoOJtUdL+Ol
Unseal Key 2: Rf5rz6+UYGB9U4Er9gjgibh8sm4DyR+vP8sP1PSAsbja
Unseal Key 3: wmrBjhVES9b5ZsV7c1KqOXn+bLkgTROVBKm/EohBmpD1
Unseal Key 4: eL2QewQNVeNc3eCcfi9BCOgNFolHvnv3421+LFNrvuv0
Unseal Key 5: DVxTC3fW0LPnvvZyhDSeRP8670pKIDmFLTX7VydQoJ6o

Initial Root Token: hvs.lyNJZCHqqKalkyPSVPnthzht
.....................................................................................

2) unseal à faire 3 fois en ajouter une clé différente à chaque fois

# vault operator unseal 

3) verifier le status 

# vault status

4) authentifier en utilisant le token

# vault login 

5) Activer le moteur de secrets Kubernetes dans Vault:

# vault auth enable kubernetes
# vault auth list

6) configure auth

# vault write auth/kubernetes/config \
kubernetes_host=https://$KUBERNETES_SERVICE_HOST:$KUBERNETES_SERVICE_PORT \
kubernetes_ca_cert=@/var/run/secrets/kubernetes.io/serviceaccount/ca.crt \
token_reviewer_jwt=@/var/run/secrets/kubernetes.io/serviceaccount/token

7) Création des politiques et des rôles d'accès
* policy

vault policy write my-policy - <<EOF
path "secret/mongo-secret/*" {
capabilities = ["read", "list"]
}
EOF 

* role
# vault write auth/kubernetes/role/my-role \
    bound_service_account_names=default \                                                 # à créer
    bound_service_account_namespaces=default \                                            # à créer
    policies=my-policy \                                                                  # à créer
    ttl=24h

8) créer un secret de type kv

# vault secrets enable -path secret kv
# vault kv put secret/mongo-secret MONGO_INITDB_ROOT_USERNAME=mongouser MONGO_INITDB_ROOT_PASSWORD=mongopassword

9) uilisation du secret par notre app

# patch-basic-annotations.yaml
spec:
  template:
    metadata:
      annotations:
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-secret-mongo-secret: "secret/mongo-secret"
        vault.hashicorp.com/role: "my-role"