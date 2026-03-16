def row_to_text(row) -> str:
    return f"""
    Name: {row.get('Full Name', '')}
    Email: {row.get('Email', '')}
    Company: {row.get('Company', '')}
    Job Title: {row.get('Job Title', '')}
    Country: {row.get('Country', '')}
    Phone: {row.get('Phone', '')}
    Course: {row.get('Course', '')}
    Gender: {row.get('Gender', '')}
    Sector: {row.get('Sector', '')}
    Supervisor: {row.get("Supervisor's Name", '')}
    Supervisor Email: {row.get("Supervisor's Email", '')}
    IT Background: {row.get('IT/Cybersecurity bckgrd (Yes/No)', '')}
    Experience: {row.get('IT/Cybersecurity work exp (yrs)', '')}
    """