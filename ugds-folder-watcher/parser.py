"""
Parser for legacy hospital folder tracker file format.
Format example:
'MR-1A-A1-1'K/13 5622'SINTIM'YABBEY'YSINT12011964-1'0273920899 0549554089'KASOA'ESTHER SARBENG'
"""

import re
from typing import Optional, List, Dict, Any

# Valid 2-digit network prefixes after '233'
GHANA_MOBILE_PREFIXES = {
    # MTN
    "24", "54", "55", "59",
    # Telecel (Vodafone)
    "20", "50",
    # AT (AirtelTigo)
    "27", "57", "26", "56",
    # Glo
    "28"
}

def clean_phone_number(raw_phone: str) -> Optional[str]:
    """
    Normalizes a single phone number into E.164 without plus: 233XXXXXXXXX.
    Returns None if not a valid Ghanaian mobile number.
    """
    # Remove all non-digits
    digits = re.sub(r"\D", "", raw_phone)
    if not digits:
        return None

    # Handle prefixes
    if digits.startswith("233"):
        normalized = digits
    elif digits.startswith("0") and len(digits) == 10:
        normalized = "233" + digits[1:]
    elif len(digits) == 9:
        normalized = "233" + digits
    else:
        return None

    # Must be exactly 12 digits: 233 + 9 digits
    if len(normalized) != 12:
        return None

    # Check network prefix (digits 3 and 4)
    net_prefix = normalized[3:5]
    if net_prefix not in GHANA_MOBILE_PREFIXES:
        # Rejects landlines (030...), foreign, or invalid ranges
        return None

    return normalized

def extract_valid_mobiles(phone_field: str) -> List[str]:
    """
    Splits field that may contain multiple numbers (separated by space, slash, comma)
    and returns a list of cleaned, valid mobile numbers.
    """
    if not phone_field:
        return []

    # Split on space, comma, slash, semicolon, or dash
    tokens = re.split(r"[\s,;/|]+", phone_field.strip())
    valid_mobiles = []

    for token in tokens:
        cleaned = clean_phone_number(token)
        if cleaned and cleaned not in valid_mobiles:
            valid_mobiles.append(cleaned)

    return valid_mobiles

def parse_tracker_line(line: str) -> Optional[Dict[str, Any]]:
    """
    Robustly parses a single line from the folder tracker file.
    Handles variable single/double quotes, titles (DR, REV, etc.),
    multiple phone numbers, landline vs mobile separation, and patient code matching.
    """
    line = line.strip()
    if not line:
        return None

    # Filter out empty parts resulting from consecutive quotes ('')
    raw_parts = [p.strip() for p in line.strip('\'"').split("'")]
    parts = [p for p in raw_parts if p]
    if len(parts) < 3:
        return None

    movement_id = parts[0]
    folder_number = parts[1]

    # Find patient code (pattern: ends with -digit, preceded by date or letters, e.g. YSINT12011964-1)
    code_idx = -1
    for i in range(2, len(parts)):
        if re.search(r"\d{4,8}-\d$", parts[i]):
            code_idx = i
            break

    if code_idx != -1:
        name_tokens = parts[2:code_idx]
        patient_code = parts[code_idx]
        remaining = parts[code_idx + 1:]
    else:
        # Fallback if no code pattern found
        name_tokens = parts[2:4]
        patient_code = ""
        remaining = parts[4:]

    # Clean name tokens, ignoring salutations/titles in the name field
    clean_names = [t.capitalize() for t in name_tokens if t.upper() not in ["DR", "MR", "MRS", "MAD", "REV", "HON"]]
    full_name = " ".join(clean_names) if clean_names else " ".join([t.capitalize() for t in name_tokens])
    first_name = clean_names[-1] if clean_names else "Patient"
    surname = clean_names[0] if len(clean_names) > 1 else ""

    # Find mobile numbers and area in remaining fields
    mobiles: List[str] = []
    area = ""
    phone_field = ""
    staff_name = ""

    for r in remaining:
        tokens = re.split(r"[\s,;/|]+", r)
        found_nums = [clean_phone_number(t) for t in tokens if clean_phone_number(t)]
        if found_nums:
            phone_field = r
            for num in found_nums:
                if num not in mobiles:
                    mobiles.append(num)
        elif not area and len(r) > 2 and not any(c.isdigit() for c in r):
            area = r
        elif not staff_name and len(r) > 2 and not any(c.isdigit() for c in r):
            staff_name = r

    primary_mobile = mobiles[0] if mobiles else None

    return {
        "movement_id": movement_id,
        "folder_number": folder_number.strip(),
        "full_name": full_name or "Patient",
        "first_name": first_name,
        "surname": surname,
        "patient_code": patient_code,
        "raw_phone": phone_field,
        "mobiles": mobiles,
        "primary_mobile": primary_mobile,
        "area": area.title() if area else "",
        "staff_name": staff_name,
        "raw_line": line
    }

