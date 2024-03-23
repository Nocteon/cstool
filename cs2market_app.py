import json
import numpy as np
import requests
import streamlit as st
import pandas as pd

# API keys ended up never being used for my calls
hash_name = "AK-47 | Redline"
condition = " (Field-Tested)"
sort = 'lowest_price'
max_float = 0.20
price = 0.00
currency='USD'
link = 'https://csfloat.com/api/v1/listings/?type=buy_now&market_hash_name='+hash_name+condition+'&sort_by='+sort+'&max_float='+str(max_float)+'&limit=1'
theme_color = "#E07F0A"
response = None

st.set_page_config(
        page_title="CS2 Deal Finder",
        layout="wide",
        menu_items={
            'About' : '# CS2 Deal Finder\nThanks to professionally-tuned settings, this website allows you to find the best deals on some of the most popular CS2 skins on the marketplace!'
        }
    )
page_selectbox = st.sidebar.selectbox(
    "Current Page",
    ["Skin Search","Settings",'Credit']
)

#page_selectbox = st.sidebar.radio("Sections",
#    ["Skin Search","Settings",'Credit'])
if page_selectbox == "Skin Search":
    st.title("Counter Strike 2 - Skin Pricing Tool")
    st.header("Check prices of some of the most popular CS2 skins today! Don't make the wrong decisions, buy only the best deals found here!")
    skin_selected = st.selectbox("Select a skin:",
                                options=["[Select a skin]",
                                         "AK-47 | Ice Coaled",
                                         "AK-47 | Redline",
                                         "AK-47 | Slate",
                                         "M4A1-S | Hyper Beast",
                                         "M4A1-S | Emphorosaur-S",
                                         "AWP | Duality",
                                         "MP9 | Starlight Protector",
                                         "MP7 | Motherboard",
                                         "Galil AR | Cerberus",
                                         "Negev | dev_texture"])
    if st.checkbox("Float Slider"):
        max_float = st.slider("Maximum Float", value=0.20, min_value=.16, max_value=0.38, step=0.01)
        st.caption(
            "The float of a skin determines how scratched it is. This site uses floats within the wear range \"Field Tested\". For more info on Weapon Floats: https://cs.money/blog/cs-go-skins/float-value-how-cs-go-skins-wear-our/ ")
    if st.checkbox("Currency (Default USD)"):
        currency = st.radio(
                "Select a currency",
                ['USD','EUR','GBP','CAD','CNY']
            )
    def search():
        #image_showcase() Moved to show picture all the time instead of only after search
        st.warning("\"Search\" can take up to two minutes to find the optimal price of the skin"
                   " when servers are under heavy load or at peak hours")
        hash_name = skin_selected
        link = 'https://csfloat.com/api/v1/listings/?type=buy_now&market_hash_name=' + hash_name + condition + '&sort_by=' + sort + '&max_float=' + str(max_float) + '&limit=1'
        response = requests.get(link).json()[0]
        if requests != None:
            price = response['price']/100.0
            currency_conversion = 1
            match currency:
                case 'USD':
                    currency_conversion = 1
                case 'EUR':
                    currency_conversion = .92
                case 'GBP':
                    currency_conversion = .79
                case 'CAD':
                    currency_conversion = 1.35
                case 'CNY':
                    currency_conversion = 7.07

            st.subheader("This skin currently costs ${:.2f} ".format(price*currency_conversion) + currency)
            st.write("You can purchase it here: https://csfloat.com/item/"+response['id'])

    def image_showcase():
        match skin_selected:
            case "AK-47 | Ice Coaled":
                st.image("cs_media/ice_coaled.png")
                st.caption("It has been custom painted with a vibrant green and blue gradient. \"Cold to the touch\"")
            case "AK-47 | Redline":
                st.image("cs_media/redline.png")
                st.caption("It has been painted using a carbon fiber hydrographic and a dry-transfer decal of a red pinstripe. \"Never be afraid to push it to the limit\"")
            case "AK-47 | Slate":
                st.image("cs_media/slate.png")
                st.caption("A custom paint job has been applied which can only be described as \"black on black on slate black\". \"Call a doctor, they're gonna need one\"")
            case "M4A1-S | Hyper Beast":
                st.image("cs_media/hyper_beast.png")
                st.caption("It has been custom painted with a beastly creature in psychadelic colours. \"You really want to impress me Booth? Make this black light sensitive - Rona Sabri, Rising Star\"")
            case "M4A1-S | Emphorosaur-S":
                st.image("cs_media/emph-s.png")
                st.caption("It has been custom painted to look like a dinosaur is clawing through the side of the weapon. \"Feeding frenzy\"")
            case "AWP | Duality":
                st.image("cs_media/duality.png")
                st.caption("It has been custom painted with a snake on either side. One snake is red and the other is gold. \"There's two sides to every story\"")
            case "MP9 | Starlight Protector":
                st.image("cs_media/starlight.png")
                st.caption("This custom paint job features a unicorn with a rainbow mane atop a white base. It has been finished with gold accents. \"May the deity protect you, should the deity select you\"")
            case "MP7 | Motherboard":
                st.image("cs_media/motherboard.png")
                st.caption("A green and white circuit board pattern has been applied. \"Stay connected\"")
            case "Galil AR | Cerberus":
                st.image("cs_media/cerberus.png")
                st.caption("It has been custom painted with a depiction of Cerberus, the mythical three headed dog that guards the underworld.")
            case "Negev | dev_texture":
                st.image("cs_media/dev_texture.png")
                st.caption("It has been custom painted with an orange base and grey developer textures. \"hammer.exe time\"")

    image_showcase()

    if st.button("Find Lowest Price"):
        if skin_selected != "[Select a skin]":
            search()
        else:
            st.error("Select a skin!")





if page_selectbox == "Settings":

    def extra_info():
        theme_color = st.color_picker("Theme Color")
        st.warning("Color changes will apply after refresh")
        if st.button("Submit Color"):
            file = open(".streamlit/config.toml","w")
            file.write("[theme]\nbase=\"dark\"\n")
            file.write("primaryColor=\"{color}\"\n".format(color = theme_color))
            file.close()
            st.toast("Theme Updated")
        if st.button("Reset Color"):
            file = open(".streamlit/config.toml", "w")
            file.write("[theme]\nbase=\"dark\"\n")
            file.write("primaryColor=\"#E07F0A\"\n")
            file.close()
            st.toast("Theme Updated")
        st.caption("Manual refresh applies last submitted color instantly")
        if st.button("Manual Refresh"):
            st.toast("Refreshed")

    extra_info()

    report = st.text_area("Bug Report")
    if st.button("Send"):
        st.success("Feedback Sent - no receiver unfortunately")
    #"No clue how to send that report to my Email"

if page_selectbox == "Credit":
    st.title("Credits")
    st.header("This page was created as part of FIU's Human Computer Interaction course.")
    st.subheader("Massive thanks to Professor Reis for his guidance through learning Streamlit")
    campuses_map = st.checkbox("See all the Miami FIU campuses")
    if campuses_map:
        map_data = pd.DataFrame(
            np.array([
                [25.759005, -80.373825],
                [25.770459, -80.368130],
                [25.910728, -80.138982],
                [25.992332, -80.339832],
                [25.763418, -80.190564],
                [25.790110, -80.131561],
                #[24.950351, -80.452974],
                #[38.895549, -77.011910],
                [25.772754, -80.134411],
                [25.781113, -80.132460]]
            ),
            columns=['lat', 'lon']
        )
        st.map(map_data)
        st.caption("Map of Miami FIU Campuses")
        if st.checkbox("Raw Coordinates"):
            table_data = pd.DataFrame(
                np.array([
                    [25.759005, -80.373825],
                    [25.770459, -80.368130],
                    [25.910728, -80.138982],
                    [25.992332, -80.339832],
                    [25.763418, -80.190564],
                    [25.790110, -80.131561],
                    # [24.950351, -80.452974],
                    # [38.895549, -77.011910],
                    [25.772754, -80.134411],
                    [25.781113, -80.132460]]
                ),
                columns=['Latitude', 'Longitude']
            )
            st.dataframe(table_data)
            st.caption("Latitude, Longitude of the marked campuses")

    report = st.text_input("Feedback")
    if st.button("Send"):
        st.success("Feedback Sent - no receiver unfortunately")
    st.caption("This website is not affiliated with Valve or the CSfloat website, and is an independent project devloped by Ralph Calixte at FIU")
    #"No clue how to send this report to my email"
