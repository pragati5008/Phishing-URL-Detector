# 🛡️ Machine Learning Based Phishing URL Detection System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-1.3.0-orange)
![Random Forest](https://img.shields.io/badge/Model-Random%20Forest-success)
![Accuracy](https://img.shields.io/badge/Accuracy-96%25-brightgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)
![PRs](https://img.shields.io/badge/PRs-welcome-brightgreen)

**A powerful machine learning web application that detects phishing websites with 96% accuracy by analyzing URL patterns and characteristics.**

[🌐 Live Demo](https://your-app.onrender.com) • 
[📖 Documentation](#) • 
[🐛 Report Bug](https://github.com/yourusername/phishing-url-detection/issues) • 
[✨ Request Feature](https://github.com/yourusername/phishing-url-detection/issues)

</div>

---

## 📋 Table of Contents

- [About The Project](#-about-the-project)
- [Key Features](#-key-features)
- [System Architecture](#-system-architecture)
- [Tech Stack](#-tech-stack)
- [Dataset & Model](#-dataset--model)
- [Installation](#-installation)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Project Structure](#-project-structure)
- [Screenshots](#-screenshots)
- [Performance Metrics](#-performance-metrics)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 About The Project

Phishing attacks are one of the most prevalent cybersecurity threats where attackers create deceptive websites mimicking legitimate ones to steal sensitive information such as passwords, banking credentials, and personal data.

This **Machine Learning Based Phishing URL Detection System** provides a robust solution by:
- Analyzing URL structures in real-time
- Extracting 35+ critical features from each URL
- Using a trained Random Forest model with 96% accuracy
- Providing instant feedback with confidence scores
- Educating users about potential cyber threats

### Purpose
The purpose of this project is to help users identify potentially malicious URLs before visiting them, making the internet a safer place.

### Scope
The system allows users to enter a website URL and determine whether the URL is safe or phishing using a machine learning model trained on comprehensive phishing datasets.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time Analysis** | Instant URL scanning and classification |
| 🤖 **ML-Powered** | Random Forest model with 96% accuracy |
| 📊 **35+ Features** | Comprehensive URL characteristic analysis |
| 🎨 **Modern UI** | Clean, responsive, user-friendly interface |
| 📜 **Search History** | Track and review past URL checks |
| 📱 **Mobile Ready** | Fully responsive across all devices |
| 🔒 **Secure** | Input validation and protection against injections |
| 📈 **Confidence Score** | Probability-based result confidence |
| 🌐 **REST API** | Programmatic access for developers |
| ⚡ **Fast Response** | Results within seconds |
| 🛡️ **Safety Tips** | Actionable recommendations for users |

---

## 🏗 System Architecture

The system follows a three-tier architecture:
```bash
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│ Presentation │────▶│ Application │────▶│ ML │
│ Layer │ │ Layer │ │ Engine │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ HTML/CSS/JS │ │ Flask/Python │ │ Random Forest │
│ Font Awesome │ │ REST API │ │ Scikit-learn │
│ Responsive │ │ Session Mgmt │ │ Feature Ext. │
└─────────────────┘ └─────────────────┘ └─────────────────┘
│ │ │
▼ ▼ ▼
```
 User Interface Business Logic ML Detection
 ```bash
┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
│ User │────▶│ URL │────▶│Feature │────▶│ ML │────▶│ Result │
│ Enters │ │ Analysis│ │Extract │ │ Predict │ │ Display │
│ URL │ │ │ │ │ │ │ │ │
└─────────┘ └─────────┘ └─────────┘ └─────────┘ └─────────┘
```

### Workflow
1. **User enters URL** in the web interface
2. **Flask backend** receives the request
3. **Feature extraction** module analyzes URL (23 features)
4. **ML model** processes features and predicts
5. **Result displayed** with confidence score and recommendations
6. **History stored** in session for future reference

---

## 💻 Tech Stack

### Frontend
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Font Awesome](https://img.shields.io/badge/Font_Awesome-339AF0?style=for-the-badge&logo=fontawesome&logoColor=white)

### Backend
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Gunicorn](https://img.shields.io/badge/Gunicorn-499848?style=for-the-badge&logo=gunicorn&logoColor=white)

### Machine Learning
![Scikit-learn](https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-013243?style=for-the-badge&logo=numpy&logoColor=white)
![Pickle](https://img.shields.io/badge/Pickle-FF6F00?style=for-the-badge&logo=python&logoColor=white)

### Deployment
![Render](https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)

---

## 📊 Dataset & Model

### Dataset Statistics
| Attribute | Value |
|-----------|-------|
| **Total URLs** | 11,430 |
| **Classes** | Balanced (50% phishing, 50% legitimate) |
| **Total Features** | 87 extracted features |
| **Selected Features** | 23 for final model |
| **Source** | Web Page Phishing Detection Dataset |

### Feature Categories

┌─────────────────────────────────────┐
│ 23 SELECTED FEATURES │
├─────────────────────────────────────┤
│ 📏 URL Length & Structure │
│ 🔣 Special Character Counts │
│ 🌐 IP Address Presence │
│ 🔒 HTTPS Usage │
│ 🔢 Digit Ratios │
│ 🏷️ TLD Analysis │
│ ⚠️ Phishing Keywords │
│ 🌍 Domain Characteristics │
│ 📝 Word Length Statistics │
│ 📊 Google Index Status │
│ 📈 Page Rank │
└─────────────────────────────────────┘
### Model Specifications

| Parameter | Value |
|-----------|-------|
| **Algorithm** | Random Forest Classifier |
| **Accuracy** | 96% |
| **Precision** | 96% |
| **Recall** | 96% |
| **F1-Score** | 96% |
| **AUC-ROC** | 0.98 |
| **Training Features** | 23 selected features |
| **Cross-validation** | 5-fold |
| **Best Parameters** | `max_depth: 20, n_estimators: 200` |


### Feature Importance
| Feature | Importance |
|---------|------------|
| google_index | 0.18 |
| page_rank | 0.15 |
| nb_www | 0.12 |
| ratio_digits_url | 0.10 |
| phish_hints | 0.09 |
| domain_age | 0.08 |
| ... | ... |

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional)
- Virtual environment (recommended)

### Step-by-Step Setup

1. **Project Structure**
```bash
phishing-url-detection/
├── 📄 app.py                          # Main Flask application
├── 📄 requirements.txt                # Project dependencies
├── 📄 README.md                       # Project documentation
├── 📄 phishing_model.pkl               # Trained ML model
├── 📄 scaler.pkl                       # Feature scaler (optional)
├── 📄 Procfile                         # Render deployment config
├── 📄 runtime.txt                      # Python version
├── 📄 .gitignore                       # Git ignore file
├── 📄 LICENSE                          # MIT License
├── 📁 utils/
│   ├── 📄 __init__.py
│   ├── 📄 feature_extractor.py         # URL feature extraction
│   └── 📄 model_loader.py              # Model loading utilities
├── 📁 templates/
│   ├── 📄 index.html                    # Home page
│   ├── 📄 about.html                     # About page
│   ├── 📄 result.html                    # Results page
│   ├── 📄 history.html                   # History page
│   ├── 📄 error.html                     # Error page
│   ├── 📄 404.html                        # 404 error page
│   └── 📄 500.html                        # 500 error page
├── 📁 static/
│   └── 📁 css/
│       └── 📄 style.css                  # Main stylesheet
├── 📁 logs/
│   └── 📄 app.log                        # Application logs
└── 📁 notebooks/
    └── 📄 phishing-url-detection-96-accuracy.ipynb  # Training notebook
```
## 📄 License
MIT License

Copyright (c) 2024 Ayush Kumar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


---

## 📞 Contact

**Ayush Kumar**

| | |
|---------|-------------|
| 🎓 **Roll No** | 2308390100018 |
| 🏫 **Department** | Computer Science and Engineering |
| 📧 **Email** | ayush.kumar@example.com |
| 🔗 **GitHub** | [@ayushkumar](https://github.com/yourusername) |
| 💼 **LinkedIn** | [Ayush Kumar](https://linkedin.com/in/yourprofile) |


### Project Links

| | |
|---------|-------------|
| 📦 **GitHub Repository** | [https://github.com/yourusername/phishing-url-detection](https://github.com/yourusername/phishing-url-detection) |
| 🌐 **Live Demo** | [https://phishing-url-detection.onrender.com](https://phishing-url-detection.onrender.com) |
| 📓 **Jupyter Notebook** | [View on Kaggle](https://kaggle.com/yourusername/phishing-detection) |

---

## 🙏 Acknowledgments

### Resources

| Resource | Purpose |
|----------|---------|
| [Web Page Phishing Detection Dataset](https://www.kaggle.com/datasets/dataset) | Training data for the model |
| [Scikit-learn](https://scikit-learn.org/) | Machine learning tools and algorithms |
| [Flask](https://flask.palletsprojects.com/) | Web framework for the application |
| [Font Awesome](https://fontawesome.com/) | Icons and UI elements |
| [Render](https://render.com/) | Free hosting and deployment |
| [GitHub](https://github.com/) | Code hosting and version control |

### Inspirations

- **OWASP**: For cybersecurity guidelines and best practices
- **Google Safe Browsing**: For phishing detection inspiration
- **PhishTank**: For community-driven phishing data

### Special Thanks

- **Department of Computer Science and Engineering** - For academic support
- **Project Guide and Mentors** - For guidance and feedback
- **Open Source Community** - For tools and libraries
- **All Contributors and Supporters** - For helping improve this project

---

<div align="center">

### ⭐ Show your support

If you found this project helpful, please give it a **star** on GitHub!

[![GitHub stars](https://img.shields.io/github/stars/yourusername/phishing-url-detection?style=social)](https://github.com/yourusername/phishing-url-detection/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/yourusername/phishing-url-detection?style=social)](https://github.com/yourusername/phishing-url-detection/network/members)
[![GitHub watchers](https://img.shields.io/github/watchers/yourusername/phishing-url-detection?style=social)](https://github.com/yourusername/phishing-url-detection/watchers)

---

**Made with ❤️ by Ayush Kumar**

© 2026 Machine Learning Based Phishing URL Detection System. All Rights Reserved.

---

[⬆ Back to Top](#-machine-learning-based-phishing-url-detection-system)

</div>
