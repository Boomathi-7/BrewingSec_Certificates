from PIL import Image, ImageDraw, ImageFont
import os
import re
from formatter import format_participant_name, format_college_name


def sanitize_name_for_file(name):
    """Convert participant name into a safe filename.
    
    Examples:
        "Varshini S" → "varshini_s"
        "Varshini @ KGiSL" → "varshini_kgisl"
    """
    name = name.strip().lower()
    # Keep only lowercase letters, numbers, spaces, and underscores.
    name = re.sub(r'[^a-z0-9_\s]', '', name)
    # Normalize whitespace and repeated underscores into single underscores.
    name = re.sub(r'[\s_]+', '_', name)
    # Remove leading/trailing underscores.
    name = name.strip('_')
    return name or "participant"


def generate_certificate(
    template_path,
    output_path,
    participant_name,
    college_name,
    participant_photo_path=None,
    qr_data=None,
    font_path=None,
):
    """Generate a certificate PDF for Summit'26.
    
    Participant Name and College Name are beautifully formatted, centered,
    and positioned in the open vertical space below 'PRESENTED TO' and above the accent line.
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

    # Pro UI Formatting
    formatted_participant_name = format_participant_name(participant_name)
    formatted_college_name = format_college_name(college_name)
    if formatted_college_name and not formatted_college_name.lower().startswith("from "):
        formatted_college_name = f"From : {formatted_college_name}"

    # Base font sizes scaled proportionally to template height (1414px)
    name_font_size = max(44, int(img_height * 0.038))
    desc_font_size = max(24, int(img_height * 0.022))

    name_font = ImageFont.truetype(name_font_path, name_font_size)
    desc_font = ImageFont.truetype(desc_font_path, desc_font_size)

    # Color theme: dark forest green matching Summit'26 template accents
    text_color = "#052c1e"

    # Strict bounding box width (68% of total width) to prevent side collision
    max_text_width = int(img_width * 0.68)

    # =============================
    # PARTICIPANT NAME (ABOVE GREEN LINE)
    # =============================
    while True:
        bbox = draw.textbbox((0, 0), formatted_participant_name, font=name_font)
        text_width = bbox[2] - bbox[0]
        if text_width <= max_text_width or name_font_size <= 26:
            break
        name_font_size -= 2
        name_font = ImageFont.truetype(name_font_path, name_font_size)

    bbox_name = draw.textbbox((0, 0), formatted_participant_name, font=name_font)
    name_w = bbox_name[2] - bbox_name[0]
    name_x = (img_width - name_w) // 2
    # Positioned ABOVE the green line (Green line is at Y=644, PRESENTED TO is at Y=465)
    name_y = int(img_height * 0.370)

    draw.text((name_x, name_y), formatted_participant_name, fill=text_color, font=name_font)

    # =============================
    # COLLEGE NAME (BELOW GREEN LINE)
    # =============================
    if formatted_college_name:
        while True:
            bbox = draw.textbbox((0, 0), formatted_college_name, font=desc_font)
            text_width = bbox[2] - bbox[0]
            if text_width <= max_text_width or desc_font_size <= 16:
                break
            desc_font_size -= 2
            desc_font = ImageFont.truetype(desc_font_path, desc_font_size)

        bbox_desc = draw.textbbox((0, 0), formatted_college_name, font=desc_font)
        desc_w = bbox_desc[2] - bbox_desc[0]
        desc_x = (img_width - desc_w) // 2
        # Positioned BELOW the green line (Green line is at Y=644, FOR COMPLETING is at Y=800)
        desc_y = int(img_height * 0.498)

        draw.text((desc_x, desc_y), formatted_college_name, fill=text_color, font=desc_font)


    # =============================
    # SAVE AS PDF
    # =============================
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, "PDF")
