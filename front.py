#!/usr/bin/env python

import altair as alt
import pandas as pd
import streamlit as st
import requests

st.set_page_config(page_title="Analizador de texto Física", layout="centered"   )

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
API_URL = "http://localhost:8000/analizador"   # <-- Ajusta tu endpoint aquí


def call_api(text:str):
    """Llama a la API del analizador de texto"""
    headers = {"Content-Type": "application/json"}
    resp = requests.post(API_URL, json={"text": text}, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def app():
    st.title("Analizador de Texto — Física ")

    with st.form(key='Search'):
        text_query = st.text_area("Introduce el texto a analizar:", height=230)
        submit_button = st.form_submit_button("Analizar")

    if submit_button:
        if not text_query.strip():
            st.warning("Escribe un texto primero.")
            return
        
        with st.spinner("Analizando texto..."):
            try:
                result = call_api(text_query)
            except Exception as e:
                st.error(f"Error al llamar a la API: {e}")
                return

        st.success("¡Análisis completo! ")

        # Mostrar resultados principales
        tema = result.get("tema", "(desconocido)")
        score = result.get("score", 0)

        st.write(f"###  Tema detectado: **{tema}**")
        st.write(f"###  Porcentaje total: **{score}%**")

        # Si la API devuelve coincidencias detalladas:
        detalles = result.get("detalles")

        if detalles:
            st.markdown("---")
            st.subheader("Coincidencias encontradas:")

            df = pd.DataFrame(detalles)
            st.table(df)

            # Barplot opcional
            bar = alt.Chart(df).mark_bar().encode(
                x="score:Q",
                y=alt.Y("palabra:N", sort='-x'),
                tooltip=["palabra", "score"]
            ).properties(
                width=600,
                height=400
            )

            st.altair_chart(bar)


if __name__ == '__main__':
    app()
