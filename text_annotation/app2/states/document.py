from .base import Base
import reflex as rx

from io import BytesIO
from docx import Document


class DocumentState(Base):

    counter: int = 0
    content: list[list[str]]
    filename: str

    upload_ui: str = "flex"
    document_ui: str = "none"

    async def get_document(self, files: list[rx.UploadFile]):
        self.upload_ui, self.document_ui = "none", "flex"

        for file in files:
            upload_data = await file.read()

            # Create a BytesIO object from the uploaded data
            file_stream = BytesIO(upload_data)

            # Load the document using python-docx
            doc = Document(file_stream)

            # Read and print the content of the document
            for paragraph in doc.paragraphs:
                words = paragraph.text.split()

                for word in words:
                    self.content.append([word, self.counter, "transparent"])
                    self.counter += 1

    def highlight_text(self, text: list[str]):
        text[2] = self.selected_category

        self.content = [item if item[1] != text[1] else text for item in self.content]
