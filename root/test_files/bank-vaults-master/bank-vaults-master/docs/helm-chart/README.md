# Helm Charts

We have some fully fledged, production ready Helm charts for deploying [Vault](https://github.com/banzaicloud/bank-vaults/tree/master/charts/vault) using `bank-vaults` and the [Vault Operator](https://github.com/banzaicloud/bank-vaults/tree/master/charts/vault-operator) and also the [Vault Secrets Webhook](https://github.com/banzaicloud/bank-vaults/tree/master/charts/vault-secrets-webhook). With the help of this chart you can run a HA Vault instance with automatic initialization, unsealing and external configuration which used to be a tedious manual operation. Also secrets from Vault can be injected into your Pods directly as environment variables (without using Kubernetes Secrets). These charts can be used easily for development purposes as well.