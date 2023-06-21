# Kubernetes Manifests for ARM64

![Kubernetes Manifests for ARM64 Logo](https://i0.wp.com/www.donaldsimpson.co.uk/wp-content/uploads/sites/6/2019/05/minikube.png?w=344&ssl=1)

Welcome to the extraordinary world of Kubernetes Manifests for ARM64! 🚀

This repository houses an impressive collection of mind-blowing Kubernetes manifests specially designed to unleash the full potential of your ARM64 infrastructure. Experience seamless deployments, scalable configurations, and unparalleled reliability like never before.

## Infrastructure Details

These manifests have been meticulously built, deployed, and tested on the following infrastructure (adjust as needed):

- 4-node Proxmox cluster consisting of ARM64 Raspberry Pi 4 Model B 8GB devices.
- 5-node high-availability Kubernetes k3s cluster. The cluster is built on 5 different virtual machines running Ubuntu Cloud Image (Jammy 22.04), leveraging etcd, KubeVIP, and MetalLB.
- The cluster was deployed using Ansible, following Techno Tim's deployment method as demonstrated in this YouTube video: [Kubernetes Deployment by Techno Tim](https://youtu.be/CbkEWcUZ7zM).
- Additionally, an NFS share is utilized, which is deployed on a separate Raspberry Pi 4 Model B 4GB running OMV (OpenMediaVault) with a 1TB USB hard drive.

Please note that at this time, we are not utilizing any storage solution other than local PV (persistent volume). Although Longhorn was initially tested, it proved to be too resource-intensive for a Pi Proxmox cluster and would crash without extensive fine-tuning.

For those interested in Rancher, you can explore Techno Tim's deployment or refer to Network Chuck's video guide on how to set it up. Stay tuned for my upcoming comprehensive setup blog, where I will provide detailed insights into my entire configuration.

## What Makes Kubernetes Manifests for ARM64 Special?

Kubernetes Manifests for ARM64 is your ultimate secret weapon for harnessing the true power of Kubernetes on ARM64 architecture. Dive into a realm of cutting-edge deployments and unlock the endless possibilities of your ARM64-based Kubernetes clusters.

## Key Features

🌟 Effortless Deployments: Embark on a journey of effortless deployments tailored specifically for ARM64 architecture. Kubernetes Manifests for ARM64 provides optimized YAML configurations that simplify your deployment process, ensuring a smooth and hassle-free experience.

🚀 Scalable Configurations: Unleash the full potential of scalability on your ARM64 infrastructure. Take advantage of horizontal pod autoscaling, replica sets, and stateful applications meticulously optimized for ARM64. Elevate your cluster's performance to new heights.

🔒 Rock-Solid Reliability: Build a rock-solid foundation for your applications on ARM64. Kubernetes Manifests for ARM64 enables fault-tolerant setups, seamless utilization of persistent storage, and guarantees high availability for your ARM64-based Kubernetes clusters.

## Getting Started

1. Kubernetes Installation: Set up a Kubernetes cluster on your ARM64 infrastructure. If you're new to Kubernetes on ARM64, refer to the official documentation for detailed instructions.

2. Clone the Repository: Clone this repository to your local machine using the following command:

git clone https://github.com/SeanRiggs/kubernetes-manifests-arm64.git


3. Explore the Manifests: Delve into our awe-inspiring collection of manifests located in the `manifests/` directory. Discover the limitless potential and select the ones specifically optimized for ARM64 architecture that perfectly align with your project.

4. Customize and Apply: Tailor the manifests to meet your application's requirements on ARM64 architecture. Unleash your creativity and fine-tune the configurations to perfection. Once ready, apply the manifests to your ARM64-based Kubernetes cluster using the `kubectl apply` command.

## Contribution Guidelines

We believe that collaboration fuels innovation. If you have any mind-bending manifest creations or improvements to share for ARM64 architecture, we welcome your contributions. To contribute to Kubernetes Manifests for ARM64, please follow the guidelines outlined in [CONTRIBUTING.md](https://github.com/SeanRiggs/kubernetes-manifests-arm64/blob/main/CONTRIBUTING.md).

Let's unlock the true potential of Kubernetes on ARM64 together!

## Support

If you have any questions, ideas, or need assistance with Kubernetes Manifests for ARM64, don't hesitate to reach out to our stellar support team at [support@kubernetes-manifests-arm64.com](mailto:support@kubernetes-manifests-arm64.com). (COMING SOON)

Get ready to conquer the ARM64 universe with Kubernetes Manifests for ARM64! 🎉
