def row_to_text(row) -> str:
    return f"""
    Name: {row.get('Full Name', '')}
    Email: {row.get('Email', '')}
    Country: {row.get('Country', '')}
    Phone: {row.get('Phone', '')}
    Gender: {row.get('Gender', '')}
    """
