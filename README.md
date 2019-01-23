# MigrarionTool 
(Name is not offically decided yet.

VMs migration tool to Openstack

This tool helps on migrating existing workload from traditional virtualization technologies (VMware and Hyper-v) to Openstack cloud.

The tool helps on automating the required steps and processes to complete the migrations.

Features:
1. Migrated from VMware and Hyper-v
2. Allow VMs Discovery and selection
3. Allow migration pause and resume
4. Migration reports.

Features:
 - Migrated from VMware and Hyper-v
 - Allow VMs Discovery and selection
 - Allow migration pause and resume
 - Migration reports.
 - VM disks are converted to the desired target format 
 - Auto include for systems drivers are added where appropriate during the process
 - Auto include for cloudbase-init & cloud-init tools are added where appropriate during the process

Support:
 - Standalone VMs

To be supported:
 - MS SQL Cluster
 - Exchange

Source:
 - VMware (vSphere)
 - Hyper-v (SCVMM)

Workload:
 - Windows (2k8R2, 2K12, 2K12R2)
 - Linux (Redhat, CentOS, SUSE, Ubuntu)
 - Physical (Ubuntu)

Export VM resources:
 - Virtual Machine
 - Templates
 - Storages
 - Networking Configuration

Authentication and Endpoint Discovery Management on Openstack:
 - Based on Keystone X-Auth-Token
 - Used to integrate with other Openstack component like: Horizon console
 - The same token is passed to other components along the pipeline
 - Importing virtual machines and other resources to the same OpenStack infrastructure doesn’t require further authentication

Authentication to virtualisation solutions (vSphere, SCVMM):
 - Used to export virtual machine resources
 - Require authentication that can be saved to avoid the need to pass secrets directly to the API (Openstack barbican is considered as a solution)

Migration Tasks:
- Export task (Monitor and log)
- Executor 
- Import task (Monitor and log)



