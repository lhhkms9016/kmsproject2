import streamlit as st
import pandas as pd
import altair as alt

def traffic1():
    # Streamlit app title
    st.title('회선 트래픽 분석 (2024년 5월)')

    # File uploader for CSV files
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

    if uploaded_file is not None:
        # Read the uploaded CSV file
        data = pd.read_csv(uploaded_file)

        # Removing leading and trailing spaces from column names
        data.columns = data.columns.str.strip()

        # Adding new columns for average and maximum bps in mbps
        data['in_mbps'] = data['in_bps'] / 1000000
        data['out_mbps'] = data['out_bps'] / 1000000

        # Sidebar multiselect for 'type' column
        st.sidebar.header('Filter options')
        types = data['type'].unique()
        all_types_option = '모두 선택'
        selected_types = st.sidebar.multiselect('Select types to filter', [all_types_option] + list(types), default=[all_types_option])

        # If '모두 선택' is selected, select all types
        if all_types_option in selected_types:
            selected_types = types

        # Filter data based on selected types
        filtered_data = data[data['type'].isin(selected_types)]

        ## Display the original data
        #st.subheader('Original Data')
        #st.dataframe(data)

        # Grouping by type, category1, category2, category3, category4 and calculating mean for in_mbps and out_mbps
        original_grouped_df = filtered_data.groupby(['type', 'category1', 'category2', 'category3', 'category4'], observed=False).agg(
            average_in_mbps=('in_mbps', 'mean'),
            average_out_mbps=('out_mbps', 'mean'),
            max_in_mbps=('in_mbps', 'max'),
            max_out_mbps=('out_mbps', 'max')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        original_grouped_df['average_in_mbps'] = original_grouped_df['average_in_mbps'].round(2)
        original_grouped_df['average_out_mbps'] = original_grouped_df['average_out_mbps'].round(2)
        original_grouped_df['max_in_mbps'] = original_grouped_df['max_in_mbps'].round(2)
        original_grouped_df['max_out_mbps'] = original_grouped_df['max_out_mbps'].round(2)

        # Display the grouped dataframe using Streamlit for original data
        st.subheader('회선 유형별 데이터')
        st.dataframe(original_grouped_df)

        # Grouping by the day column and calculating mean for in_mbps and out_mbps
        grouped_df = filtered_data.groupby(['day'], observed=False).agg(
            average_in_mbps=('in_mbps', 'mean'),
            average_out_mbps=('out_mbps', 'mean')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        grouped_df['average_in_mbps'] = grouped_df['average_in_mbps'].round(2)
        grouped_df['average_out_mbps'] = grouped_df['average_out_mbps'].round(2)

        # Display the grouped dataframe using Streamlit for grouped data by day
        st.subheader('1_일자별 평균 데이터')
        st.dataframe(grouped_df)

        # Creating a line chart for in_mbps and out_mbps average values by day
        day_chart = alt.Chart(grouped_df).transform_fold(
            ['average_in_mbps', 'average_out_mbps'],
            as_=['Measurement', 'Mbps']
        ).mark_line().encode(
            x=alt.X('day:Q', title='Day'),
            y=alt.Y('Mbps:Q', title='Mbps'),
            color=alt.Color('Measurement:N', title='Measurement'),
            tooltip=['day', 'Measurement:N', 'Mbps:Q']
        ).interactive()

        st.altair_chart(day_chart, use_container_width=True)

        # Grouping by the weekday2 column and calculating mean for in_mbps and out_mbps
        weekday_order = ['월', '화', '수', '목', '금', '토', '일']
        filtered_data['weekday2'] = pd.Categorical(filtered_data['weekday2'], categories=weekday_order, ordered=True)
        
        weekday_grouped_df = filtered_data.groupby(['weekday2'], observed=False).agg(
            average_in_mbps=('in_mbps', 'mean'),
            average_out_mbps=('out_mbps', 'mean')
        ).reset_index().sort_values(by='weekday2')

        # Formatting the numeric columns to two decimal places
        weekday_grouped_df['average_in_mbps'] = weekday_grouped_df['average_in_mbps'].round(2)
        weekday_grouped_df['average_out_mbps'] = weekday_grouped_df['average_out_mbps'].round(2)

        # Display the grouped dataframe using Streamlit for grouped data by weekday2
        st.subheader('2_요일별 평균 데이터')
        st.dataframe(weekday_grouped_df)

        # Creating a line chart for in_mbps and out_mbps average values by weekday2
        weekday_chart = alt.Chart(weekday_grouped_df).transform_fold(
            ['average_in_mbps', 'average_out_mbps'],
            as_=['Measurement', 'Mbps']
        ).mark_line().encode(
            x=alt.X('weekday2:N', title='Weekday', sort=weekday_order),
            y=alt.Y('Mbps:Q', title='Mbps'),
            color=alt.Color('Measurement:N', title='Measurement'),
            tooltip=['weekday2:N', 'Measurement:N', 'Mbps:Q']
        ).interactive()

        st.altair_chart(weekday_chart, use_container_width=True)

        # Grouping by the hour column and calculating mean for in_mbps and out_mbps
        hourly_grouped_df = filtered_data.groupby(['hour'], observed=False).agg(
            average_in_mbps=('in_mbps', 'mean'),
            average_out_mbps=('out_mbps', 'mean')
        ).reset_index()

        # Formatting the numeric columns to two decimal places
        hourly_grouped_df['average_in_mbps'] = hourly_grouped_df['average_in_mbps'].round(2)
        hourly_grouped_df['average_out_mbps'] = hourly_grouped_df['average_out_mbps'].round(2)

        # Display the grouped dataframe using Streamlit for grouped data by hour
        st.subheader('시간대별 평균 데이터')
        st.dataframe(hourly_grouped_df)

        # Creating a line chart for in_mbps and out_mbps average values by hour
        hour_chart = alt.Chart(hourly_grouped_df).transform_fold(
            ['average_in_mbps', 'average_out_mbps'],
            as_=['Measurement', 'Mbps']
        ).mark_line().encode(
            x=alt.X('hour:Q', title='Hour'),
            y=alt.Y('Mbps:Q', title='Mbps'),
            color=alt.Color('Measurement:N', title='Measurement'),
            tooltip=['hour:Q', 'Measurement:N', 'Mbps:Q']
        ).interactive()

        st.altair_chart(hour_chart, use_container_width=True)

    else:
        st.write("Please upload a CSV file to proceed.")
