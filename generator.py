from PIL import Image, ImageDraw, ImageFont
import os
import re


def sanitize_name_for_file(name):
    """Convert participant name into a safe filename.
    
    Examples:
        "Boomathi P" → "boomathi_p"
        "Boomathi @ KGiSL" → "boomathi_kgisl"
    """
    name = name.strip().lower()
    # Keep only lowercase letters, numbers, spaces, and underscores.
    name = re.sub(r'[^a-z0-9_\s]', '', name)
    # Normalize whitespace and repeated underscores into single underscores.
    name = re.sub(r'[\s_]+', '_', name)
    # Remove leading/trailing underscores.
    name = name.strip('_')
    return name or "participant"


def format_name(name):
    """Format participant name with proper title casing and clean spacing.
    
    Examples:
        "boomathi p" → "Boomathi P"
        "JOHN DOE" → "John Doe"
    """
    if not name:
        return ""
    words = name.strip().split()
    formatted_words = []
    for w in words:
        if len(w) == 1:
            formatted_words.append(w.upper())
        elif w.islower() or w.isupper():
            formatted_words.append(w.capitalize())
        else:
            formatted_words.append(w)
    return " ".join(formatted_words)


def format_college(college):
    """Format college name with clean title casing and spacing.
    
    Examples:
        "kgisl institute of technology" → "KGiSL Institute of Technology"
    """
    if not college:
        return ""
    words = college.strip().split()
    formatted_words = []
    lowercase_words = {"of", "and", "in", "for", "the", "at", "to", "on"}
    for i, w in enumerate(words):
        w_lower = w.lower()
        if w_lower == "kgisl":
            formatted_words.append("KGiSL")
        elif len(w) <= 3 and w.isupper():
            formatted_words.append(w)
        elif i > 0 and w_lower in lowercase_words:
            formatted_words.append(w_lower)
        elif w.islower() or w.isupper():
            formatted_words.append(w.capitalize())
        else:
            formatted_words.append(w)
    return " ".join(formatted_words)


def generate_certificate(
    template_path,
    output_path,
    participant_name,
    college_name,
    participant_photo_path=None,
    qr_data=None,
    font_path=None,
):
    """Generate a certificate PDF for Summit'26 without photo or QR code.
    
    Participant Name and College Name are beautifully formatted, centered,
    and placed relative to the template's central line accent.
    """
    # Validate template exists
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Certificate template not found: {template_path}")
    
    img = Image.open(template_path).convert("RGB")
    draw = ImageDraw.Draw(img)
    img_width, img_height = img.size

    # Construct font paths from the static directory
    static_dir = os.path.dirname(template_path)
    fonts_dir = os.path.join(static_dir, "fonts")
    
    if not os.path.exists(fonts_dir):
        raise FileNotFoundError(f"Fonts directory not found: {fonts_dir}")
    
    name_font_path = os.path.join(fonts_dir, "PlayfairDisplay-Bold.ttf")
    desc_font_path = os.path.join(fonts_dir, "PlayfairDisplay-Regular.ttf")
    
    for font_file in [name_font_path, desc_font_path]:
        if not os.path.exists(font_file):
            raise FileNotFoundError(f"Font file not found: {font_file}")

    # Format text inputs
    formatted_participant_name = format_name(participant_name)
    formatted_college_name = format_college(college_name)

    # Base font sizes & scaling bounds
    name_font_size = max(56, int(img_height * 0.053))
    desc_font_size = max(30, int(img_height * 0.028))

    name_font = ImageFont.truetype(name_font_path, name_font_size)
    desc_font = ImageFont.truetype(desc_font_path, desc_font_size)

    # Color theme: dark forest green matching Summit'26 template accents
    text_color = "#052c1e"

    # Max available horizontal width (75% of total width)
    max_text_width = int(img_width * 0.75)

    # =============================
    # PARTICIPANT NAME
    # =============================
    while True:
        bbox = draw.textbbox((0, 0), formatted_participant_name, font=name_font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width or name_font_size <= 32:
            break
        name_font_size -= 2
        name_font = ImageFont.truetype(name_font_path, name_font_size)

    bbox_name = draw.textbbox((0, 0), formatted_participant_name, font=name_font)
    name_w = bbox_name[2] - bbox_name[0]
    name_x = (img_width - name_w) // 2
    name_y = 398  # Centered above green horizontal line (line is at Y=482)

    draw.text((name_x, name_y), formatted_participant_name, fill=text_color, font=name_font)

    # =============================
    # COLLEGE NAME
    # =============================
    if formatted_college_name:
        while True:
            bbox = draw.textbbox((0, 0), formatted_college_name, font=desc_font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_text_width or desc_font_size <= 20:
                break
            desc_font_size -= 2
            desc_font = ImageFont.truetype(desc_font_path, desc_font_size)

        bbox_desc = draw.textbbox((0, 0), formatted_college_name, font=desc_font)
        desc_w = bbox_desc[2] - bbox_desc[0]
        desc_x = (img_width - desc_w) // 2
        desc_y = 515  # Centered below green horizontal line

        draw.text((desc_x, desc_y), formatted_college_name, fill=text_color, font=desc_font)

    # =============================
    # SAVE AS PDF
    # =============================
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PDF")