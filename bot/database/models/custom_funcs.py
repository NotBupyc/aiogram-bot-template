from sqlalchemy import text

check_datetime = text(
    """
CREATE OR REPLACE FUNCTION check_datetime(time_param TIMESTAMP)
RETURNS BOOLEAN AS $$
BEGIN
    IF time_param IS NULL THEN
        RETURN TRUE;
    END IF;

    IF time_param > NOW() THEN
        RETURN TRUE;
    END IF;

    RETURN FALSE;
END;
$$ LANGUAGE plpgsql;
"""
)

all_functions = (check_datetime,)
