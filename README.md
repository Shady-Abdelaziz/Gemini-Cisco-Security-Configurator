# LLM-Based Cisco Security Configurator

## Overview
The LLM-Based Cisco Security Configurator is a Streamlit-powered application that uses large language models to assess and remediate Cisco device configurations in line with STIG (Security Technical Implementation Guide) standards. It integrates vector-based retrieval with LLM analysis to deliver expert security insights and automated configuration fixes.

## Features
- **Smart Configuration Analysis:** Upload Cisco configuration files to automatically detect security compliance issues.
- **STIG Data Integration:** Leverages a CSV-based STIG database (or embedded data) to retrieve relevant security requirements.
- **LLM-Powered Recommendations:** Uses a large language model to provide detailed analysis and generate automated remediation strategies.
- **LLDP Data Support:** Optionally processes LLDP information to enhance network topology insights.
- **Automated Remediation:** Generates a fixed configuration with inline comments explaining the security adjustments.
- **Comparison Visualization:** Offers unified diff and side-by-side comparison views to clearly highlight changes.
- **Report Generation:** Enables downloading of both the remediated configuration and a comprehensive security report.

## Requirements
- Python 3.7+
- Libraries: pandas, streamlit, pickle, langchain, difflib, re
- A valid Google API key for Gemini integration (configured via st.secrets or environment variables)

## Setup and Usage
1. **Clone the Repository:**  
   `git clone https://github.com/yourusername/llm-based-cisco-security-configurator.git`  
   `cd llm-based-cisco-security-configurator`

2. **Install Dependencies:**  
   Install the required libraries using pip with the provided requirements file.

3. **Configure API Key:**  
   Set your Google API key in st.secrets or as an environment variable.

4. **Run the Application:**  
   Launch the Streamlit app by executing the app file.

5. **Using the Tool:**  
   - Upload your Cisco configuration file (and optionally LLDP info).  
   - Provide a STIG CSV file if available (or use the embedded STIG data).  
   - Review the automated security analysis, fixed configuration, and change comparisons.  
   - Download the generated reports for documentation and review.

## License
This project is licensed under the MIT License.
