# # Importing ToolKits
# from time import sleep
# import pandas as pd
# import numpy as np
# import os


# import streamlit as st
# from streamlit.components.v1 import html
# from streamlit_option_menu import option_menu

# import tensorflow as tf

# def run():
#     st.set_page_config(
#         page_title="Forecasting Loan Default Risk",
#         page_icon="💰",
#         layout="wide"
#     )

#     if "the_df" not in st.session_state:
#         st.session_state.the_df = pd.DataFrame()

#     # Function To Load Our Dataset

#     @st.cache_data
#     def load_loan_detection_ann_model(model_path):
#         full_path = os.path.join(os.path.dirname(__file__), "..", "models", model_path)
#         return tf.keras.models.load_model(full_path)

#     @st.cache_data
#     def load_scaler_transformation(model_path):
#         full_path = os.path.join(os.path.dirname(__file__), "..", "models", model_path)
#         return pd.read_pickle(full_path)

#     model = load_loan_detection_ann_model("loan_default_risk_detection_ann_v3.h5")
#     scaler = load_scaler_transformation("model_min_max_scaler.pkl")


#     def check_columns(df, order_columns):
#         columns = df.columns.to_list()
#         columns = list(map(lambda x: x.lower(), columns))
#         order_columns = list(map(lambda x: x.lower(), order_columns))

#         return 1 if columns == order_columns else 0
    
#     style_path = os.path.join(os.path.dirname(__file__), "style.css")
#     with open(style_path, "r") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#     side_bar_options_style = {
#         "container": {"padding": "0!important", "background-color": '#121212', "border-radius": "0"},
#         "icon": {"color": "#fff", "font-size": "20px"},
#         "nav-link": {"color": "#fff", "font-size": "18px", "text-align": "left", "margin": "0px", "margin-bottom": "0px"},
#         "nav-link-selected": {"background-color": "#009378", "font-size": "16px", },
#     }

#     header = st.container()
#     content = st.container()

#     st.write("")

#     with st.sidebar:
#         st.write("")
#         st.title("💸 Lend Secure 💸")
#         st.write("")

#         page = option_menu(
#             menu_title=None,
#             options=['Preidct Value', 'From CSV File'],
#             icons=['robot', 'filetype-csv'],
#             menu_icon="cast",
#             default_index=0,
#             styles=side_bar_options_style
#         )

#         st.write("")
#         # st_lottie(lottie_json, height=350, speed=1)

#         # Home Page
#         if page == "Preidct Value":
#             with header:
#                 st.header("Loan Default Risk Prediction 💰")

#             with content:
#                 col1, col2 = st.columns([8, 4])

#                 with col1:
#                     with st.form("Preidct"):
#                         c1, c2 = st.columns(2)
#                         with c1:
#                             annual_income = st.number_input('**Annual Income**', min_value=10000,
#                                                             max_value=1000000000, value=100000)

#                             applicant_age = st.number_input(
#                                 '**Applicant Age**', min_value=21, max_value=85, value=33)

#                             marital_status = st.selectbox('**Marital Status**', options=[
#                                                           "Married", "Single"], index=0)

#                         house_ownership = st.selectbox('**House Ownership**', options=[
#                             "Rented", "Owned", "No-Rent No-Own"], index=0)

#                         with c2:
#                             work_exp = st.number_input(
#                                 '**Work Experience**', min_value=0, max_value=40, value=4)

#                             years_in_current_employment = st.number_input(
#                                 '**Years In Employment**', min_value=0, max_value=30, value=3)

#                             vehicle_ownership = st.selectbox('**Vehicle Ownership**', options=[
#                                 "Yes", "No"], index=0)

#                         predict_button = st.form_submit_button("**Predict** 🚀")

#                 with col2:
#                     if predict_button:

#                         # marital_status
#                         marital_status_encodded = 0  # Married
#                         if marital_status == "Single":
#                             marital_status_encodded = 1

#                         # house_ownership
#                         house_ownership_encodded = [0, 0]  # No-Rent No-Own

#                         if house_ownership == "Rented":
#                             house_ownership_encodded = [0, 1]  # Rented

#                         elif house_ownership == "Owned":
#                             house_ownership_encodded = [1, 0]  # Owned

#                         # vehicle_ownership
#                         vehicle_ownership_encodded = 1  # Yes

#                         if vehicle_ownership == "No":
#                             vehicle_ownership_encodded = 0  # No

#                         # Create list of all New Data
#                         new_data = [annual_income, applicant_age, work_exp,
#                                     years_in_current_employment, marital_status_encodded]

#                         # Appending All Data
#                         new_data.extend(house_ownership_encodded)
#                         new_data.append(vehicle_ownership_encodded)

#                         scaled_data = scaler.transform([new_data])

#                         with st.spinner(text='Predict The Value..'):

#                             predicted_value_prop = model.predict(
#                                 [scaled_data])[0][0]
#                             predicted_value = (predicted_value_prop > 0.5) * 1

#                             sleep(1.2)

#                             st.subheader("Default Risk")
#                             st.progress(
#                                 value=int(predicted_value_prop*100),)
#                             st.subheader(f"{predicted_value_prop*100:0.2f}%")

#                             if predicted_value == 0:
#                                 st.success("")
#                                 img_path = os.path.join(os.path.dirname(__file__), "imgs", "loan.png")
#                                 st.image(img_path, caption="", width=150)
#                                 st.subheader("Expected No Loan")
#                                 st.subheader(":green[Default Risk]")

#                             else:
#                                 st.error("")
#                                 img_path = os.path.join(os.path.dirname(__file__), "imgs", "speedometer.png")
#                                 st.image(img_path, caption="", width=105)
#                                 st.subheader(f"Expected Loan")
#                                 st.subheader(":red[Default Risk]")

#         # Another Page
#         if page == "From CSV File":
#             df = pd.DataFrame()
#             the_data = st.file_uploader(
#                 "Upload Your Master Data (CSV)📂", type="csv")

#             if the_data is not None:
#                 if the_data.name.split(".")[-1].lower() != "csv":
#                     st.error("Please, Upload CSV FILE ONLY")
#                 else:
#                     st.session_state.the_df = pd.read_csv(the_data)
#                     df = st.session_state.the_df.copy()
#                     df.dropna(inplace=True)

#             with header:
#                 st.header("Prediction From File ")

#             with content:
#                 st.write("")
#                 is_right_data = check_columns(df, ['Annual_Income', 'Applicant_Age', 'Work_Experience', 'Marital_Status',
#                                                    'House_Ownership', 'Vehicle_Ownership',
#                                                    'Years_in_Current_Work'])

#                 if is_right_data:
#                     st.dataframe(df.sample(frac=0.35, random_state=99),
#                                  use_container_width=True, hide_index=True)

#                     if st.button("✨ Predict ✨", type="primary"):
#                         with st.spinner("Predictin New Data..."):
#                             df_encodded = pd.get_dummies(df, columns=['Marital_Status', 'House_Ownership', 'Vehicle_Ownership'],
#                                                          drop_first=True)*1

#                             scaled_data = scaler.transform(df_encodded)

#                             predictions = model.predict(scaled_data)
#                             predictions = (predictions > 0.5) * 1

#                             full_df = df.copy()
#                             full_df["Loan Defualt Predicted"] = predictions

#                             st.dataframe(
#                                 full_df, use_container_width=True, hide_index=True)

#                 else:
#                     st.info(
#                         "Please, Upload The Right Dataset With The Same Columns and Order", icon="🚨")
#                     st.info(
#                         "['Annual_Income', 'Applicant_Age', 'Work_Experience', 'Marital_Status', 'House_Ownership', 'Vehicle_Ownership', 'Years_in_Current_Work']")


# run()

# Importando ferramentas
from time import sleep
import pandas as pd
import numpy as np
import os

import streamlit as st
from streamlit.components.v1 import html
from streamlit_option_menu import option_menu

import tensorflow as tf

def run():
    st.set_page_config(
        page_title="Previsão de Risco de Inadimplência",
        page_icon="💰",
        layout="wide"
    )

    if "the_df" not in st.session_state:
        st.session_state.the_df = pd.DataFrame()

    # Função para carregar modelo

    @st.cache_data
    def load_loan_detection_ann_model(model_path):
        full_path = os.path.join(os.path.dirname(__file__), "..", "models", model_path)
        return tf.keras.models.load_model(full_path)

    @st.cache_data
    def load_scaler_transformation(model_path):
        full_path = os.path.join(os.path.dirname(__file__), "..", "models", model_path)
        return pd.read_pickle(full_path)

    model = load_loan_detection_ann_model("loan_default_risk_detection_ann_v3.h5")
    scaler = load_scaler_transformation("model_min_max_scaler.pkl")


    def check_columns(df, order_columns):
        columns = df.columns.to_list()
        columns = list(map(lambda x: x.lower(), columns))
        order_columns = list(map(lambda x: x.lower(), order_columns))

        return 1 if columns == order_columns else 0
    
    style_path = os.path.join(os.path.dirname(__file__), "style.css")
    with open(style_path, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    side_bar_options_style = {
        "container": {"padding": "0!important", "background-color": '#121212', "border-radius": "0"},
        "icon": {"color": "#fff", "font-size": "20px"},
        "nav-link": {"color": "#fff", "font-size": "18px", "text-align": "left", "margin": "0px", "margin-bottom": "0px"},
        "nav-link-selected": {"background-color": "#009378", "font-size": "16px", },
    }

    header = st.container()
    content = st.container()

    st.write("")

    with st.sidebar:
        st.write("")
        st.title("💸 Empréstimo Seguro 💸")
        st.write("")

        page = option_menu(
            menu_title=None,
            options=['Prever Valor', 'Do Arquivo CSV'],
            icons=['robot', 'filetype-csv'],
            menu_icon="cast",
            default_index=0,
            styles=side_bar_options_style
        )

        st.write("")
        # st_lottie(lottie_json, height=350, speed=1)

        # Página Principal
        if page == "Prever Valor":
            with header:
                st.header("Previsão de Risco de Inadimplência 💰")

            with content:
                col1, col2 = st.columns([8, 4])

                with col1:
                    with st.form("Prever"):
                        c1, c2 = st.columns(2)
                        with c1:
                            annual_income = st.number_input('**Renda Anual**', min_value=10000,
                                                            max_value=1000000000, value=100000)

                            applicant_age = st.number_input(
                                '**Idade do Solicitante**', min_value=21, max_value=85, value=33)

                            marital_status = st.selectbox('**Estado Civil**', options=[
                                                          "Casado", "Solteiro"], index=0)

                        house_ownership = st.selectbox('**Possui Imóvel**', options=[
                            "Alugado", "Próprio", "Nem Alugado Nem Próprio"], index=0)

                        with c2:
                            work_exp = st.number_input(
                                '**Experiência Profissional (anos)**', min_value=0, max_value=40, value=4)

                            years_in_current_employment = st.number_input(
                                '**Anos no Emprego Atual**', min_value=0, max_value=30, value=3)

                            vehicle_ownership = st.selectbox('**Possui Veículo**', options=[
                                "Sim", "Não"], index=0)

                        predict_button = st.form_submit_button("**Prever** 🚀")

                with col2:
                    if predict_button:

                        # Estado civil
                        marital_status_encodded = 0  # Casado
                        if marital_status == "Solteiro":
                            marital_status_encodded = 1

                        # Possui imóvel
                        house_ownership_encodded = [0, 0]  # Nem Alugado Nem Próprio

                        if house_ownership == "Alugado":
                            house_ownership_encodded = [0, 1]  # Alugado

                        elif house_ownership == "Próprio":
                            house_ownership_encodded = [1, 0]  # Próprio

                        # Possui veículo
                        vehicle_ownership_encodded = 1  # Sim

                        if vehicle_ownership == "Não":
                            vehicle_ownership_encodded = 0  # Não

                        # Criar lista com todos os dados novos
                        new_data = [annual_income, applicant_age, work_exp,
                                    years_in_current_employment, marital_status_encodded]

                        # Acrescentar todos os dados
                        new_data.extend(house_ownership_encodded)
                        new_data.append(vehicle_ownership_encodded)

                        scaled_data = scaler.transform([new_data])

                        with st.spinner(text='Realizando a Previsão...'):

                            predicted_value_prop = model.predict(
                                [scaled_data])[0][0]
                            predicted_value = (predicted_value_prop > 0.5) * 1

                            sleep(1.2)

                            st.subheader("Risco de Inadimplência")
                            st.progress(
                                value=int(predicted_value_prop*100),)
                            st.subheader(f"{predicted_value_prop*100:0.2f}%")

                            if predicted_value == 0:
                                st.success("")
                                img_path = os.path.join(os.path.dirname(__file__), "imgs", "loan.png")
                                st.image(img_path, caption="", width=150)
                                st.subheader("Resultado: Empréstimo Concedido")
                                st.subheader(":green[Risco Baixo]")

                            else:
                                st.error("")
                                img_path = os.path.join(os.path.dirname(__file__), "imgs", "speedometer.png")
                                st.image(img_path, caption="", width=105)
                                st.subheader(f"Resultado: Empréstimo Negado")
                                st.subheader(":red[Risco Alto]")

        # Outra página
        if page == "Do Arquivo CSV":
            df = pd.DataFrame()
            the_data = st.file_uploader(
                "Envie seu arquivo principal (CSV)📂", type="csv")

            if the_data is not None:
                if the_data.name.split(".")[-1].lower() != "csv":
                    st.error("Por favor, envie somente arquivos CSV")
                else:
                    st.session_state.the_df = pd.read_csv(the_data)
                    df = st.session_state.the_df.copy()
                    df.dropna(inplace=True)

            with header:
                st.header("Previsão a partir do arquivo ")

            with content:
                st.write("")
                is_right_data = check_columns(df, ['Annual_Income', 'Applicant_Age', 'Work_Experience', 'Marital_Status',
                                                   'House_Ownership', 'Vehicle_Ownership',
                                                   'Years_in_Current_Work'])

                if is_right_data:
                    st.dataframe(df.sample(frac=0.35, random_state=99),
                                 use_container_width=True, hide_index=True)

                    if st.button("✨ Prever ✨", type="primary"):
                        with st.spinner("Realizando Previsões..."):
                            df_encodded = pd.get_dummies(df, columns=['Marital_Status', 'House_Ownership', 'Vehicle_Ownership'],
                                                         drop_first=True)*1

                            scaled_data = scaler.transform(df_encodded)

                            predictions = model.predict(scaled_data)
                            predictions = (predictions > 0.5) * 1

                            full_df = df.copy()
                            full_df["Previsão de Inadimplência"] = predictions

                            st.dataframe(
                                full_df, use_container_width=True, hide_index=True)

                else:
                    st.info(
                        "Por favor, envie um arquivo com as mesmas colunas e ordem correta", icon="🚨")
                    st.info(
                        "['Annual_Income', 'Applicant_Age', 'Work_Experience', 'Marital_Status', 'House_Ownership', 'Vehicle_Ownership', 'Years_in_Current_Work']")


run()

