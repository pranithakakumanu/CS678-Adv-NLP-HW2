import PyPDF2
from typing import AnyStr
from googlesearch import search
from gentopia.tools.basetool import *
import io
import requests

class PDFTextSummarizerArgs(BaseModel):
    pdf_path: str = Field(..., description="a summarize pdf existing at pdf_path")


class PDFTextSummarizer(BaseTool):
        name = "pdf_summarizer"
        description = ("A tool that reads a PDF and summarizes it.")
        args_schema: Optional[Type[BaseModel]] = PDFTextSummarizerArgs

        def extract_text(self, pdf_path):
                """Extract text from each page of the PDF."""
                headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}
                response = requests.get(url=pdf_path, headers=headers, timeout=120)
                on_fly_mem_obj = io.BytesIO(response.content)
                pdf = PyPDF2.PdfReader(on_fly_mem_obj)
                text = ''
                for page in pdf.pages:
                        text += page.extract_text() + ' '
                summary = self.basic_summarize(text)
                return summary

        def basic_summarize(self, text):
                """Generate a basic summary of the given text."""
                sentences = text.split('.')
                summary = '. '.join(sentences[:10]) + '.'  # Return the first three sentences as a basic summary
                return summary

        def _run(self, pdf_path: AnyStr) -> str:
                return (self.extract_text(pdf_path))

        async def _arun(self, *args: Any, **kwargs: Any) -> Any:
                raise NotImplementedError

if __name__ == "__main__":
        url = 'https://dataprivacylab.org/dataprivacy/projects/kanonymity/paper3.pdf'
        ans = PDFTextSummarizer()._run(url)
        print(ans)
