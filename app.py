import os
import pandas as pd
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
import difflib

st.set_page_config(page_title="Cisco Security Compliance Assistant", layout="wide")

st.title("Cisco Security Compliance Assessment")
st.markdown("""
This tool helps you check your Cisco device configuration for security compliance issues.
Upload your configuration file and get recommendations based on STIG standards.
""")

@st.cache_data
def load_stig_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.fillna('')
    return df

@st.cache_resource
def get_llm():
    api_key = st.secrets.get("GOOGLE_API_KEY", os.environ.get("GOOGLE_API_KEY", ""))
    if not api_key:
        st.error("Please set your Google API key in the app secrets or environment variables")
        return None
   
    try:
        llm = ChatGoogleGenerativeAI(
            model="models/gemini-2.0-flash",  
            google_api_key=api_key,
            temperature=0.7,  
            convert_system_message_to_human=True
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None

def analyze_configuration(config_content, stig_df, llm):
    stig_text = ""
    
    columns = stig_df.columns.tolist()
    
    for _, row in stig_df.iterrows():
        for col in columns:
            if pd.notna(row[col]) and row[col]:
                stig_text += f"{col}: {row[col]}\n"
        stig_text += "\n---\n\n"
    
    template = """
    You are a professional Cisco network expert specializing in Cisco IOS XE Switch RTR Security Technical Implementation. Your task is to understand the provided file and fix its issues .
    your task is to fix the given specific protocol configuration , maybe the full configuration or a part of it.

    Cisco IOS XE Switch RTR Security Technical Implementation Guide is :
    {stig_data}
    
    the given file :
    {config}
    
    Please perform the following tasks as a professional cisco network engineer:
    1. ANALYSIS:
       - Carefully examine the original given file and identify any compliance issues as defined in the Cisco IOS XE Switch RTR Security Technical Implementation Guide
       - Explain exactly what's missing or misconfigured and the security implications

    2. FIXED_CONFIG:
       - create the updated given file accoding to the Cisco IOS XE Switch RTR Security Technical Implementation Guide for the given file only.
       - ensure the security compliance while maintaining gven file functionality , dont just disable everything.
       - give priority to high then mdeium then low severity issues.
       - dont create a full new configuration file if the provided is only one protocol a part of configuration file.
       - if the provided file is only protocol , dont implement all configuration just fix the given file.
    
    3. COMPARISON:
       - Create a summary of what changes were made
       - Explain how these changes improve security posture
       - Highlight any trade-offs or potential operational impacts from these changes
  
    Format your response with clear section headers: "ANALYSIS:", "FIXED_CONFIG:", and "COMPARISON:".

    """
    
    prompt = PromptTemplate(
        input_variables=["stig_data", "config"],
        template=template,
    )
    
    formatted_prompt = prompt.format(stig_data=stig_text, config=config_content)
    
    response = llm.invoke(formatted_prompt)
    
    return response.content

def generate_diff(original, fixed):
    diff = difflib.unified_diff(
        original.splitlines(),
        fixed.splitlines(),
        fromfile="original_config.txt",
        tofile="fixed_config.txt",
        lineterm='',
        n=3
    )
    return '\n'.join(diff)

def highlight_diff(original, fixed):
    d = difflib.HtmlDiff()
    return d.make_file(original.splitlines(), fixed.splitlines(),
                       fromdesc="Original Configuration",
                       todesc="Fixed Configuration")

def main():
    st.sidebar.header("STIG Database")
    uploaded_stig = st.sidebar.file_uploader("Upload STIG CSV", type=["csv"])
   
    if uploaded_stig is not None:
        try:
            stig_df = load_stig_csv(uploaded_stig)
            st.sidebar.success(f"Loaded {len(stig_df)} STIG entries")
            st.sidebar.info(f"CSV columns: {', '.join(stig_df.columns.tolist())}")
        except Exception as e:
            st.sidebar.error(f"Error loading STIG CSV: {str(e)}")
            return
    else:
        EMBEDDED_CSV_PATH = r"C:\Users\Dell\Desktop\config llm\Cisco_IOS_XE_Switch_RTR_Security_Technical_Implementation_Guide.csv"
        if os.path.exists(EMBEDDED_CSV_PATH):
            try:
                stig_df = load_stig_csv(EMBEDDED_CSV_PATH)
                st.sidebar.info(f"Using embedded STIG data with {len(stig_df)} entries")
                st.sidebar.info(f"CSV columns: {', '.join(stig_df.columns.tolist())}")
            except Exception as e:
                st.sidebar.error(f"Error loading embedded STIG CSV: {str(e)}")
                return
        else:
            st.sidebar.warning("No STIG data available. Please upload a STIG CSV file.")
            return
   
    llm = get_llm()
    if llm is None:
        st.error("LLM initialization failed. Please check your API key.")
        return
   
    st.sidebar.header("Device Configuration")
    uploaded_config = st.sidebar.file_uploader("Upload Cisco Configuration", type=["txt", "cfg"])
   
    if uploaded_config is not None:
        config_content = uploaded_config.getvalue().decode("utf-8")
       
        with st.expander("Original Configuration", expanded=False):
            st.code(config_content, language="cisco")
       
        with st.spinner("Analyzing configuration and generating recommendations..."):
            try:
                full_response = analyze_configuration(config_content, stig_df, llm)
               
                analysis = ""
                fixed_config = ""
                comparison = ""
               
                if "ANALYSIS:" in full_response:
                    parts = full_response.split("ANALYSIS:")[1].split("FIXED_CONFIG:")
                    analysis = parts[0].strip()
                   
                    if len(parts) > 1:
                        remaining = parts[1]
                        if "COMPARISON:" in remaining:
                            parts = remaining.split("COMPARISON:")
                            fixed_config = parts[0].strip()
                            comparison = parts[1].strip()
                        else:
                            fixed_config = remaining.strip()
                else:
                    lines = full_response.split('\n')
                    mode = None
                    for line in lines:
                        if "ANALYSIS:" in line:
                            mode = "analysis"
                            continue
                        elif "FIXED_CONFIG:" in line:
                            mode = "config"
                            continue
                        elif "COMPARISON:" in line:
                            mode = "comparison"
                            continue
                       
                        if mode == "analysis":
                            analysis += line + "\n"
                        elif mode == "config":
                            fixed_config += line + "\n"
                        elif mode == "comparison":
                            comparison += line + "\n"
               
                st.subheader("Security Analysis")
                st.markdown(analysis)
               
                st.subheader("Fixed Configuration")
                with st.expander("View Complete Fixed Configuration", expanded=True):
                    st.code(fixed_config, language="cisco")
               
                if comparison:
                    st.subheader("Configuration Impact Analysis")
                    st.markdown(comparison)
               
                st.subheader("Configuration Changes")
                diff_text = generate_diff(config_content, fixed_config)
               
                with st.expander("View Changes (Unified Diff)", expanded=True):
                    st.code(diff_text, language="diff")
               
                with st.expander("Side-by-Side Comparison", expanded=False):
                    html_diff = highlight_diff(config_content, fixed_config)
                    st.components.v1.html(html_diff, height=600, scrolling=True)
               
                col1, col2 = st.columns(2)
                with col1:
                    st.download_button(
                        label="Download Fixed Configuration",
                        data=fixed_config,
                        file_name="fixed_cisco_config.txt",
                        mime="text/plain"
                    )
               
                with col2:
                    report = f"""# Cisco Security Compliance Report
## Security Analysis
{analysis}
## Fixed Configuration
```
{fixed_config}
```
## Configuration Impact Analysis
{comparison}
"""
                    st.download_button(
                        label="Download Complete Report",
                        data=report,
                        file_name="cisco_security_report.md",
                        mime="text/markdown"
                    )
               
            except Exception as e:
                st.error(f"Error analyzing configuration: {str(e)}")
    else:
        st.info("Please upload a Cisco configuration file to analyze.")

if __name__ == "__main__":
    main()