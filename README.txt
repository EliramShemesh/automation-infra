# 🧪 Automation Infra

A modular Python-based automation infrastructure designed for API and UI testing using `pytest`. This framework emphasizes scalability, maintainability, and logging clarity.

---

## 📁 Project Structure

```
automation-infra/
├── api_helper.py          # Helper functions for API testing
├── driver_setup.py        # Driver setup for UI automation
├── loguru_config.py       # Centralized logging using Loguru
├── pytest.ini             # Pytest configuration
├── requirements.txt       # Python dependencies
├── utils.py               # Utility functions
├── tests/
│   ├── conftest.py        # Pytest fixtures
│   └── test_dummy.py      # Sample test case
└── README.txt             # Project documentation
```

---

## 🚀 Features

- ✅ API test helpers
- 🖥️ UI automation hooks
- 🧪 Pytest with fixtures
- 📋 Logging with `loguru`
- 📂 Structured and clean directory layout
- 📦 Easy dependency management via `requirements.txt`

---

## 🛠️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/your-username/automation-infra.git
cd automation-infra

# 2. Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt
```

---

## 🧪 Running Tests

Run all tests:
```bash
pytest
```

Run a specific test:
```bash
pytest tests/test_dummy.py
```

Enable verbose and logging output:
```bash
pytest -v --capture=tee-sys
```

---

## 📦 Dependencies

Key Python packages used:
- `pytest`
- `loguru`
- Any others listed in `requirements.txt`

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
