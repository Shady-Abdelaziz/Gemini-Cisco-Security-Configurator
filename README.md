# Gemini Cisco Security Configurator

## Overview
The Gemini Cisco Security Configurator is a Streamlit-based application that leverages large language models and Gemini integration to assess and remediate Cisco device configurations in accordance with STIG (Security Technical Implementation Guide) standards. This tool combines vector-based retrieval with advanced LLM analysis to deliver expert security insights and automated configuration fixes.

## Features
- **Intelligent Configuration Analysis:** Upload Cisco configuration files to automatically identify security compliance issues.
- **STIG Data Integration:** Utilizes a CSV-based STIG database (or embedded data) to retrieve and apply relevant security requirements.
- **Gemini-Powered Recommendations:** Employs a large language model via Gemini to generate detailed analysis and remediation strategies.
- **Optional LLDP Processing:** Supports LLDP data to enhance network topology insights.
- **Automated Remediation:** Produces a fixed configuration with inline comments that explain each security adjustment.
- **Comparison Visualization:** Offers unified diff and side-by-side views to clearly highlight configuration changes.
- **Report Generation:** Enables downloading of both the remediated configuration and a comprehensive security report.

## Requirements
- Python 3.7+
- Libraries: pandas, streamlit, pickle, langchain, difflib, re
- A valid Google API key for Gemini integration (set via st.secrets or environment variables)

## Setup and Usage
1. **Clone the Repository:**  
   `git clone https://github.com/Gemini-Cisco-Security-Configurator.git`  
   `cd gemini-cisco-security-configurator`

2. **Install Dependencies:**  
   Install the required libraries using pip with the provided requirements file.

3. **Configure API Key:**  
   Set your Google API key in st.secrets or as an environment variable.

4. **Run the Application:**  
   Launch the Streamlit app by running the application file.

5. **Using the Tool:**  
   - Upload your Cisco configuration file (and optionally LLDP info).  
   - Provide a STIG CSV file if available (or use the embedded STIG data).  
   - Review the automated security analysis, fixed configuration, and change comparisons.  
   - Download the generated reports for documentation and further review.

## License
This project is licensed under the MIT License.
