Dynamic provisioning with NFS



1) installer et configurer NFS server:
...................................
apt-get install nfs-server,
mkdir /k8_storage_prod,
mkdir /k8_storage_preprod,
chmod 777 -R /k8_storage_prod,
chmod 777 -R /k8_storage_preprod,
nano /etc/exports
    /k8s_storage_prod *(rw,sync,no_subtree_check)
    /k8s_storage_preprod *(rw,sync,no_subtree_check)
systemctl enable nfs-kernel-server,
systemctl start nfs-kernel-server

2) installer et configurer NFS client:
   ...................................
apt-get install nfs-common
mount -t nfs4 192.168.2.27:/k8_storage_prod /mnt/                  ---> pour le cluster prod
mount -t nfs4 192.168.2.27:/k8_storage_preprod /mnt/                  ---> pour le cluster preprod
umount /mnt/

3) Dynamic provisioning configuration:

helm repo add nfs-subdir-external-provisioner https://kubernetes-sigs.github.io/nfs-subdir-external-provisioner/
helm install nfs-subdir-external-provisioner nfs-subdir-external-provisioner/nfs-subdir-external-provisioner \
    --set nfs.server=192.168.2.27 \
    --set nfs.path=/k8_storage_prod

kubectl patch storageclass nfs-client -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"true"}}}'

............................................................................................
