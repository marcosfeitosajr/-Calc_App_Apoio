# Calc App Apoio

Este projeto é uma aplicação [Streamlit](https://streamlit.io/) para cálculo de apoios do tipo POT.

## Como executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Rode a aplicação:
   ```bash
   streamlit run app.py
   ```

Você também pode executar os cálculos em modo texto:
```bash
python -m calc_app.cli 1000 5
```
O exemplo acima considera 1000 kN de carga vertical máxima e
5 mm de deslocamento longitudinal.

O antigo arquivo `Cálculo_POT_UNI.py` foi refatorado. O cálculo está agora
organizado no módulo `calc_app/calculator.py` e a interface em
`calc_app/pot_calc.py`.
