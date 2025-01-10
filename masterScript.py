import xml.etree.ElementTree as ET

def extract_issues(xml_input_path, critical_output_path):
    """
    1. Parse the input XML containing <Scan> <Issues> ... </Issues> data.
    2. Extract all <Issue> blocks and count them.
    3. Extract only <Issue> blocks whose <Severity> is "4".
    4. Write the critical issues into a separate XML file.
    
    :param xml_input_path: Path to the input XML file.
    :param critical_output_path: Path to the output XML file for critical (severity=4) issues.
    """
    # 1. Parse the XML file
    tree = ET.parse(xml_input_path)
    root = tree.getroot()
    
    # 2. Find all <Issue> elements under <Issues> (no matter how deep they are)
    #    Using XPath .//Issues/Issue or we can do:
    issues = root.findall(".//Issues/Issue")
    total_issues_count = len(issues)
    
    print(f"Total number of <Issue> blocks found: {total_issues_count}")
    
    # 3. Filter issues that have <Severity> == "4"
    critical_issues = []
    for issue in issues:
        severity_elem = issue.find("Severity")
        if severity_elem is not None and severity_elem.text.strip() == "4":
            critical_issues.append(issue)
    
    critical_count = len(critical_issues)
    print(f"Number of critical (Severity=4) issues found: {critical_count}")

    # 4. Write the critical issues into a separate XML file.
    #    We'll create a small XML structure with a root <CriticalIssues> for clarity.
    #    Then we copy over each <Issue> node and append it to this new root.
    critical_root = ET.Element("CriticalIssues")
    for ci in critical_issues:
        # We want to _clone_ each Issue node. 
        # Easiest approach: use .deepcopy(ci)
        import copy
        ci_copy = copy.deepcopy(ci)
        critical_root.append(ci_copy)
    
    # Build an ElementTree from critical_root
    critical_tree = ET.ElementTree(critical_root)
    
    # Write pretty-printed XML (if you want it pretty, consider using minidom or lxml)
    critical_tree.write(critical_output_path, encoding="utf-8", xml_declaration=True)
    
    print(f"Critical issues (Severity=4) have been saved to: {critical_output_path}")


if __name__ == "__main__":
    # Example usage:
    # Suppose your XML dump is saved as "scanresults.xml"
    # and you want to save critical severity=4 issues to "critical_issues.xml"
    input_xml = "a.xml"
    output_xml = "critical_issues.xml"
    
    extract_issues(input_xml, output_xml)
