
# returns SQL string case filtering of a jsons array column
def case_insensitive_json_array_filter(column_name: str, value: str) -> str:
    return f"""
        LOWER('{value}') = ANY (
            SELECT LOWER(value::text)
            FROM jsonb_array_elements_text({column_name}::jsonb) AS value
        )
    """
