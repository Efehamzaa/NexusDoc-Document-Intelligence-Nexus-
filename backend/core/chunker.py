from llama_index.core import Document
from llama_index.core.node_parser import SentenceSplitter
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..')))
from backend.services.parser import extract_text_from_pdf

def get_text_chunks(text):
    if not text:
        raise ValueError("Metin boş olamaz.")
    
    doc=Document(text=text)
    parser= SentenceSplitter(chunk_size=512 , chunk_overlap=50)
    nodes=parser.get_nodes_from_documents([doc])
    return nodes

if __name__=="__main__":
    pdf_file="data/ornek.pdf"
    print("1. PDF Okunuyor...")
    raw_text=extract_text_from_pdf(pdf_file)

    if raw_text:
        print("2. Metin Parcalara Bolunuyor... ")
        chunks= get_text_chunks(raw_text)

        print(f"İslem Başarili! Toplam {len(chunks)} adet anlamli parça (node) oluşturuldu.")

        if len(chunks)>0:
            print("\n --- İlk Parca Ozeti ---")
            print(chunks[0].text[:150] + "...")

            