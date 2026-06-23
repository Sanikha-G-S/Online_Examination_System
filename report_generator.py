from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import getSampleStyleSheet


def generate_result_pdf(
        username,
        exam_id,
        score,
        total):

    filename = (
        f"{username}_result.pdf"
    )

    doc = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "ONLINE EXAMINATION RESULT",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Student : {username}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Exam ID : {exam_id}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Score : {score}/{total}",
            styles["Normal"]
        )
    )

    percentage = round(
        (score / total) * 100,
        2
    )

    content.append(
        Paragraph(
            f"Percentage : {percentage}%",
            styles["Normal"]
        )
    )

    doc.build(content)

    return filename