from pathlib import Path
import fitz  # this is the pymupdf package, imported under its old name

PDF_PATH = Path("data/docs/nimbusflow_q3_report.pdf")
IMAGES_OUT_DIR = Path("data/extracted_images")
IMAGES_OUT_DIR.mkdir(parents=True, exist_ok=True)

doc = fitz.open(PDF_PATH)

for page_number, page in enumerate(doc, start=1):
    text = page.get_text()
    print(f"\n=== Page {page_number} text ===")
    print(text)

    images = page.get_images(full=True)
    print(f"\n=== Page {page_number}: {len(images)} embedded image(s) ===")

    for image_index, image_info in enumerate(images, start=1):
        xref = image_info[0]  # the image's internal reference number in the PDF
        base_image = doc.extract_image(xref)
        image_bytes = base_image["image"]
        extension = base_image["ext"]  # e.g. "png", "jpeg"

        out_path = IMAGES_OUT_DIR / f"page{page_number}_img{image_index}.{extension}"
        out_path.write_bytes(image_bytes)
        print(f"Saved: {out_path}")

doc.close()
