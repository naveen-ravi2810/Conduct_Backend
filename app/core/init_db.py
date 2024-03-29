from app.curd.curd_skills import add_main_skills
from app.core.db import async_session


additional_skills = [
    "Python",
    "Java",
    "JavaScript",
    "C++",
    "C#",
    "Swift",
    "Ruby",
    "Go (Golang)",
    "PHP",
    "TypeScript",
    "Django (Python)",
    "Flask (Python)",
    "Ruby on Rails (Ruby)",
    "Sinatra (Ruby)",
    "Express.js (JavaScript)",
    "AngularJS (JavaScript)",
    "React.js (JavaScript)",
    "Vue.js (JavaScript)",
    "Laravel (PHP)",
    "Symfony (PHP)",
    "CodeIgniter (PHP)",
    "ASP.NET (C#)",
    "Spring Boot (Java)",
    "Play Framework (Java)",
    "Meteor (JavaScript)",
    "NestJS (TypeScript)",
    "Ember.js (JavaScript)",
    "Next.js (JavaScript)",
    "FastAPI (Python)",
    "MERN Stack",
    "Full Stack",
    "Machine Learning",
    "TensorFlow (Python)",
    "PyTorch (Python)",
    "Scikit-learn (Python)",
    "Keras (Python)",
    "Theano (Python)",
    "Caffe (C++)",
    "MXNet (Python)",
    "Microsoft Cognitive Toolkit (CNTK) (C++)",
    "Apache Spark MLlib (Java, Scala)",
    "Weka (Java)",
    "RapidMiner (Java)",
    "H2O.ai (Java, Python)",
    "ML.NET (C#, F#)",
    "UI/UX",
    "Blender",
    "Unity",
    "VLSI Design",
    "ASIC Design (Application-Specific Integrated Circuit)",
    "EDA Tools (Electronic Design Automation)",
    "System-on-Chip (SoC) Design",
    "RTL Design (Register Transfer Level)",
    "Verification and Validation",
    "Hardware Description Languages (Verilog, VHDL)",
    "Physical Design and Layout",
    "Embedded Systems",
    "IoT (Internet of Things)",
    "Microcontroller Programming",
    "Wireless Communication Protocols (Bluetooth, Wi-Fi, LoRa)",
    "Sensor Integration",
    "RTOS (Real-Time Operating Systems)",
    "Satellite Communication Systems",
    "Antenna Design",
    "Radiation Effects and Hardening",
    "RF (Radio Frequency) Engineering",
    "Power Systems for Satellites" "Drone Design",
    "Drone Navigation Systems",
    "Flight Control Algorithms",
    "Drone Propulsion Systems",
    "Sense and Avoid Systems",
    "Marketing",
    "Finance",
    "Accounting",
    "Business Strategy",
    "Operations Management",
    "Supply Chain Management",
    "Human Resource Management",
    "Entrepreneurship",
    "Business Analytics",
    "Market Research",
    "Sales Management",
    "Corporate Law",
    "Business Communication",
    "Project Management",
    "Product Management",
    "Strategic Management",
    "Leadership Development",
    "Organizational Behavior",
    "Risk Management",
    "International Business",
    "Economics",
    "Business Ethics",
    "Business Intelligence",
    "Customer Relationship Management (CRM)",
    "Lean Six Sigma",
    "Quality Management",
    "Data Analysis",
    "Decision Making",
    "Business Development",
    "Change Management",
    "Algorithms",
    "Data Structures",
    "Programming Languages",
    "Operating Systems",
    "Computer Architecture",
    "Software Engineering",
    "Database Management Systems",
    "Computer Networks",
    "Web Development",
    "Mobile Development",
    "Artificial Intelligence",
    "Machine Learning",
    "Data Science",
    "Cybersecurity",
    "Cloud Computing",
    "Big Data",
    "Computer Graphics",
    "Human-Computer Interaction",
    "Embedded Systems",
    "Internet of Things (IoT)",
    "Blockchain Technology",
    "Natural Language Processing",
    "Computer Vision",
    "Robotics",
    "Parallel Computing",
    "Distributed Systems",
    "Game Development",
    "Quantum Computing",
    "Bioinformatics",
    "Compiler Design",
    "Mechanics",
    "Thermodynamics",
    "Fluid Mechanics",
    "Heat Transfer",
    "Materials Science",
    "Mechanical Design",
    "Manufacturing Processes",
    "Engineering Drawing",
    "Machine Design",
    "Engineering Mechanics",
    "Automotive Engineering",
    "Aeronautical Engineering",
    "Renewable Energy",
    "Control Systems",
    "Robotics",
    "Structural Analysis",
    "Vibration Analysis",
    "Finite Element Analysis",
    "CAD/CAM",
    "Industrial Engineering",
    "Circuit Theory",
    "Electromagnetic Field Theory",
    "Analog Electronics",
    "Digital Electronics",
    "Power Systems",
    "Control Systems",
    "Signal Processing",
    "Electric Machines",
    "Power Electronics",
    "Renewable Energy Systems",
    "Microelectronics",
    "Integrated Circuits",
    "Instrumentation",
    "Communication Systems",
    "Embedded Systems",
    "Electrical Drives",
    "Renewable Energy Sources",
    "High Voltage Engineering",
    "Electric Power Distribution",
    "Electrical Measurements",
    "Network Security",
    "Information Security",
    "Cryptography",
    "Ethical Hacking",
    "Firewall Management",
    "Virtual Private Networks (VPNs)",
    "Intrusion Detection and Prevention Systems (IDPS)",
    "Wireless Security",
    "TCP/IP Protocols",
    "Network Monitoring",
    "Amazon Web Services (AWS)",
    "Microsoft Azure",
    "Google Cloud Platform (GCP)",
    "Docker",
    "Kubernetes (K8s)",
    "Jenkins",
    "Ansible",
    "Terraform",
    "GitHub Actions",
    "Prometheus",
    "Git (Version Control)",
    "Continuous Integration (CI)",
    "Continuous Deployment (CD)",
    "Container Orchestration",
    "Infrastructure as Code (IaC)",
    "Configuration Management",
    "Microservices Architecture",
    "Serverless Computing",
    "Monitoring and Logging",
    "Deployment Automation",
    "Continuous Delivery",
    "Blue-Green Deployment",
    "Canary Deployment",
    "Feature Toggles",
    "Immutable Infrastructure",
    "GitOps",
    "Chaos Engineering",
    "Site Reliability Engineering (SRE)",
    "Dependency Management",
    "Performance Optimization",
]


original_final = []

hm = {}
for i in additional_skills:
    if i in hm:
        hm[i] += 1
    else:
        original_final.append(i)
        hm[i] = 1


async def init_db_fun():
    async with async_session() as session:
        await add_main_skills(session=session, skills=original_final)
