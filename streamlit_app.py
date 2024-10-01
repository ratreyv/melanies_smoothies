# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col, when_matched

# Write directly to the app
st.title(":cup_with_straw: Pending Smoothie Orders  :cup_with_straw:")
st.write(
    """Orders that needs to filled.
    """
)

#option = st.selectbox ('How would you like to be contacted?',
#('Email','Home Phone','Mobile Phone'))

#st.write('You selected: ' ,option)


#option = st.selectbox ('What is your favorite fruit?',
#('Banana','Strawberries','Peaches'))

#st.write('Your favorite fruit is: ' ,option)


session = get_active_session()
#my_dataframe = session.table("smoothies.public.orders").select(col('INGREDIENTS'),col('NAME_ON_ORDER'),col('ORDER_FILLED'))
my_dataframe = session.table("smoothies.public.orders").filter(col("ORDER_FILLED")==0).collect()
#st.dataframe(data=my_dataframe, use_container_width=True)
#editable_df = st.data_editor(my_dataframe)

editable_df = st.data_editor(my_dataframe,column_order=("ORDER_UID","INGREDIENTS","NAME_ON_ORDER","ORDER_FILLED"), use_container_width=True)
 
#st.dataframe(editable_df)

favorite_command = editable_df.loc[editable_df["ORDER_FILLED"].idxmax()]["ORDER_UID"]
st.markdown(f"Your favorite command is **{favorite_command}** 🎈")

#st.dataframe(data=editable_df, use_container_width=True)

submitted = st.button('Submit')

if submitted:
     
    og_dataset = session.table("smoothies.public.orders")
    
    #edited_dataset = session.table("smoothies.public.orders")
    
    #edited_dataset = session.create_dataframe(editable_df)
    edited_dataset = pd.DataFrame(editable_df)

    try:
        og_dataset.merge(edited_dataset
                     , (og_dataset['ORDER_UID'] == edited_dataset['ORDER_UID'])
                     , [when_matched().update({'ORDER_FILLED': edited_dataset['ORDER_FILLED']})]
                    )
        st.success("Order(s) Updated !",icon="👍")
    except:
        st.write('Something went wrong!')   
    #st.success("Someone clicked the button. ",icon="👍")





