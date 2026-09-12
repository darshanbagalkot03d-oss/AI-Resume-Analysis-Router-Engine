# config/jds.py
"""
Standardized Job Descriptions mapped to each target domain folder in test_corpus/.
These represent high-density industry benchmark job descriptions for ATS and Cover Letter alignment.
"""

AI_DATA_SCIENCE_JD = """
Position: Senior AI & Machine Learning Engineer (CV / Edge AI)
Target Domain: AI_DataScience

Role Overview:
We are seeking an AI/ML Engineer to build, optimize, and deploy high-performance computer vision and generative models. You will design end-to-end ML pipelines from data ingestion to edge hardware deployment.

Core Technical Requirements:
- 3+ years experience with Python, PyTorch, TensorFlow, and OpenCV.
- Proven expertise in object detection and segmentation architectures (YOLOv8/YOLO11, RT-DETR).
- Edge deployment experience on embedded platforms (Raspberry Pi, NVIDIA Jetson, ONNX Runtime, TensorRT).
- Hands-on experience with LLMs, RAG framework development (LangChain, LlamaIndex), and Vector DBs.
- Proficiency in model evaluation, metric validation, and containerized serving (FastAPI, Docker).
"""

CLOUD_DEVOPS_JD = """
Position: Principal Cloud & DevOps Infrastructure Architect
Target Domain: Cloud_DevOps

Role Overview:
We are looking for a Cloud & DevOps Architect to manage infrastructure-as-code, CI/CD automation, and cloud-native security across multi-cloud environments (AWS/Azure/GCP).

Core Technical Requirements:
- Extensive experience with Terraform, Ansible, and CloudFormation for Infrastructure as Code (IaC).
- Deep expertise in Kubernetes (EKS/GKE), Docker container orchestration, and microservices networking.
- Building robust CI/CD pipelines using GitHub Actions, GitLab CI, or Jenkins.
- Monitoring and observability using Prometheus, Grafana, ELK stack, and OpenTelemetry.
- Strong grounding in SRE principles, disaster recovery, and cloud cost/performance optimization.
"""

CYBERSECURITY_JD = """
Position: Senior Cybersecurity & SOC Operations Specialist
Target Domain: Cybersecurity

Role Overview:
We are hiring a Cybersecurity Specialist to oversee threat detection, incident response, SIEM engineering, and vulnerability assessments across enterprise environments.

Core Technical Requirements:
- Hands-on experience with SIEM platforms (Splunk, Sentinel, QRadar) and EDR tooling.
- Expertise in threat hunting, log analysis, packet capture (Wireshark), and exploit chain analysis.
- Vulnerability management and penetration testing using Metasploit, Nmap, and Burp Suite.
- Strong understanding of Identity and Access Management (IAM), Zero-Trust Architecture, and ISO 27001/NIST compliance.
- Proficiency in scripting (Python, Bash, PowerShell) for automated threat mitigation.
"""

SOFTWARE_EMBEDDED_JD = """
Position: Embedded Systems & IoT Integration Engineer
Target Domain: Software_Embedded

Role Overview:
We are seeking an Embedded Systems Engineer to design low-level firmware, IoT edge connectivity, and real-time middleware applications.

Core Technical Requirements:
- Expert-level proficiency in C, C++, and Python for hardware/firmware development.
- Hands-on experience with Microcontrollers (ESP32, STM32, ARM Cortex-M) and RTOS (FreeRTOS).
- Deep understanding of hardware communication protocols: SPI, I2C, UART, CAN bus, and Modbus.
- Experience building RESTful APIs, MQTT telemetry pipelines, and Linux system-level utilities.
- Familiarity with hardware debugging tools (Oscilloscopes, Logic Analyzers, JTAG/SWD).
"""

# Mapping dictionary linking test_corpus folder names directly to matching JDs
DOMAIN_JD_MAP = {
    "AI_DataScience": AI_DATA_SCIENCE_JD,
    "Cloud_DevOps": CLOUD_DEVOPS_JD,
    "Cybersecurity": CYBERSECURITY_JD,
    "Software_Embedded": SOFTWARE_EMBEDDED_JD,
}

DEFAULT_JD = AI_DATA_SCIENCE_JD