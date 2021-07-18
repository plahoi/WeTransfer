import streamlit as st
import base64
import altair as alt
import components

from urllib.error import URLError


def get_table_download_link_csv(df):
    csv = df.to_csv(columns=['dttm', 'usd_price', 'eur_price', 'week_rolling_avg'], index=False).encode()
    b64 = base64.b64encode(csv).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="WeTransfer_AntonPoliakov.csv" target="_blank">Download csv file</a>'
    return href


try:
    cols1 = st.beta_columns(1)
    start_date, end_date = components.dates_threshold()
    # Let's get the data we need!
    data = components.get_coin_data(start_date, end_date)
    data = components.trim_dataframe(data, start_date, end_date)

    data.reset_index(inplace=True)
    data.rename(columns={'index': 'dttm'}, inplace=True)
    data['dttm'] = data['dttm'].dt.strftime('%Y-%m-%d')

    st.write('Data preview', data.head())
    chart = (
        alt.Chart(data)
        .mark_area(opacity=0.3)
        .encode(
                x=alt.X('dttm:T', axis=alt.Axis(tickCount=12, grid=True)),
                y=alt.Y('week_rolling_avg:Q')
            )
    )
    st.altair_chart(chart, use_container_width=True)
    st.markdown(get_table_download_link_csv(data), unsafe_allow_html=True)

except URLError as e:
    st.error(
        """
        **This demo requires internet access.**

        Connection error: %s
    """
        % e.reason
    )
