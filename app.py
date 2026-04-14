import streamlit as st
import pdfplumber
import re

st.title("🏢 Analisador de Propostas Imobiliárias")

pdf = st.file_uploader("Envie um PDF", type="pdf")

def extrair_texto(file):
    texto = ""
    try:
        with pdfplumber.open(file) as pdf_file:
            for pagina in pdf_file.pages:
                conteudo = pagina.extract_text()
                if conteudo:
                    texto += conteudo + "\n"
    except:
        st.error("Erro ao ler PDF")
    return texto

if pdf:
    texto = extrair_texto(pdf)

    st.subheader("📄 Texto do PDF")
    st.text_area("", texto, height=200)

    valores = re.findall(r'\d+[.,]\d+', texto.replace(",", "."))
    valores = [float(v) for v in valores]

    st.subheader("💰 Valores encontrados")
    st.write(valores)

    if valores:
        entrada = valores[0]
        valor_final = max(valores)
        parcelas = valores[1:-1]

        total = entrada + sum(parcelas)
        lucro = valor_final - total

        st.subheader("📊 Análise")

        st.write(f"💰 Total investido: R$ {total:,.2f}")
        st.write(f"🏁 Valor final: R$ {valor_final:,.2f}")
        st.write(f"📈 Lucro: R$ {lucro:,.2f}")
