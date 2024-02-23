# Dynamic provisioning with NFS


# 1) installer et configurer NFS server:

 apt-get install nfs-server
 nano /etc/exports
    /k8_storage + autorisation

# 2) installer et configurer NFS client:

 apt-get install nfs-common



# 3) Dynamic provisioning configuration:

helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=10.3.130.127 \
    --set nfs.path=/k8_storage

kubectl patch storageclass nfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

............................................................................................

