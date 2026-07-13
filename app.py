import streamlit as st
import pandas as pd
from datetime import date
import random
import urllib.parse

# वेबसाइट का लेआउट और टाइटल सेट करना
st.set_page_config(page_title="MIS School Diary Portal", layout="wide", page_icon="🏛️")

st.title("🏛️ MIS Portal & Dynamic Syllabus Management System")
st.markdown("---")

# ----------------- 🔗 DATABASE INISHIALIZATION & FALLBACKS -----------------
def load_data_from_sheet(sheet_name):
    try:
        conn = st.connection("gsheets", type=st.connections.SQLConnection)
        df = conn.query(f"SELECT * FROM {sheet_name}")
        return df
    except:
        if sheet_name == "Teachers" and "fallback_teachers" not in st.session_state:
            st.session_state["fallback_teachers"] = pd.DataFrame([
                {"Phone": "9876543210", "Name": "पूनम (Poonam)", "PIN": "1234", "Role": "Teacher"},
                {"Phone": "0000000000", "Name": "प्रिंसिपल / एडमिन (Admin)", "PIN": "admin", "Role": "Admin"}
            ])
        if sheet_name == "Diary" and "fallback_diary" not in st.session_state:
            st.session_state["fallback_diary"] = pd.DataFrame(columns=[
                "Diary_ID", "Teacher", "Date", "Period", "Subject", "Class_Section", "Page_Range", "Topics", "Homework", "Remarks", "Status"
            ])
        if sheet_name == "Syllabus" and "fallback_syllabus" not in st.session_state:
            st.session_state["fallback_syllabus"] = pd.DataFrame([
                {"Topic_ID": "T1", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 1, "End_Page": 22, "Topic": "Ch 1: संख्या पद्धति (Number Systems)", "Homework": "Ex 1.1 to 1.3 Selected Qs"},
                {"Topic_ID": "T2", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 23, "End_Page": 44, "Topic": "Ch 2: बहुपद (Polynomials)", "Homework": "Ex 2.2 & 2.4 Selected Qs"},
                {"Topic_ID": "T3", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 1, "End_Page": 18, "Topic": "Ch 1: वास्तविक संख्याएं (Real Numbers)", "Homework": "Ex 1.1 & 1.2 Complete"}
            ])
        
        if sheet_name == "Teachers": return st.session_state["fallback_teachers"]
        elif sheet_name == "Diary": return st.session_state["fallback_diary"]
        else: return st.session_state["fallback_syllabus"]

def save_row_to_sheet(sheet_name, new_row_dict):
    new_df = pd.DataFrame([new_row_dict])
    if sheet_name == "Teachers":
        st.session_state["fallback_teachers"] = pd.concat([st.session_state["fallback_teachers"], new_df], ignore_index=True)
    elif sheet_name == "Diary":
        st.session_state["fallback_diary"] = pd.concat([st.session_state["fallback_diary"], new_df], ignore_index=True)
    elif sheet_name == "Syllabus":
        st.session_state["fallback_syllabus"] = pd.concat([st.session_state["fallback_syllabus"], new_df], ignore_index=True)

def update_diary_status(diary_id, new_status):
    df = st.session_state["fallback_diary"]
    st.session_state["fallback_diary"].loc[df["Diary_ID"] == diary_id, "Status"] = new_status

def delete_syllabus_topic(topic_id):
    df = st.session_state["fallback_syllabus"]
    st.session_state["fallback_syllabus"] = df[df["Topic_ID"] != topic_id]

# डेटाबेस हमेशा लाइव लोड रखना
teachers_df = load_data_from_sheet("Teachers")
diary_df = load_data_from_sheet("Diary")
syllabus_df = load_data_from_sheet("Syllabus")

# 🔍 लाइव सिलेबस डेटाबेस से टॉपिक ढूंढने वाला फंक्शन
def get_topics_and_hw_dynamic(selected_class, selected_subject, start_p, end_p):
    found_topics = []
    found_homework = []
    matched_data = syllabus_df[(syllabus_df["Class"] == selected_class) & (syllabus_df["Subject"] == selected_subject)]
    
    for index, item in matched_data.iterrows():
        if not (end_p < int(item["Start_Page"]) or start_p > int(item["End_Page"])):
            found_topics.append(item["Topic"])
            found_homework.append(item["Homework"])
            
    if not found_topics:
        return "इस पेज रेंज के लिए कोई टॉपिक नहीं मिला।", "N/A"
    return "\n".join(found_topics), " | ".join(found_homework)

# ----------------- 🔐 लॉगिन एवं रजिस्ट्रेशन गेटवे -----------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["current_user_phone"] = ""

if not st.session_state["logged_in"]:
    tab1, tab2 = st.tabs(["🔒 शिक्षक/एडमिन लॉगिन (Login)", "📝 नया रजिस्ट्रेशन (Register via OTP)"])
    
    with tab1:
        st.subheader("वेबसाइट लॉगिन पैनल")
        log_phone = st.text_input("रजिस्टर्ड मोबाइल नंबर (Admin: 0000000000):").strip()
        log_pin = st.text_input("सिक्योरिटी पिन (PIN):", type="password").strip()
        
        if st.button("🔓 लॉगिन करें", use_container_width=True):
            user_match = teachers_df[(teachers_df["Phone"] == log_phone) & (teachers_df["PIN"] == log_pin)]
            if not user_match.empty:
                st.session_state["logged_in"] = True
                st.session_state["current_user_phone"] = log_phone
                st.success("सफल लॉगिन!")
                st.rerun()
            else:
                st.error("❌ गलत मोबाइल नंबर या पिन!")
                
    with tab2:
        st.subheader("नया टीचर अकाउंट बनाएं")
        reg_name = st.text_input("शिक्षक का पूरा नाम (Full Name):")
        reg_phone = st.text_input("मोबाइल नंबर (10-Digit Phone):").strip()
        
        col_reg1, col_reg2 = st.columns(2)
        with col_reg1:
            if st.button("🔢 OTP पिन जनरेट करें", use_container_width=True):
                if len(reg_phone) == 10 and reg_phone.isdigit() and reg_name.strip() != "":
                    if reg_phone in teachers_df["Phone"].values:
                        st.warning("⚠️ यह नंबर पहले से रजिस्टर्ड है!")
                    else:
                        st.session_state["current_otp"] = str(random.randint(1000, 9999))
                        st.session_state["temp_register_data"] = {"Phone": reg_phone, "Name": reg_name, "PIN": st.session_state["current_otp"], "Role": "Teacher"}
                        st.info(f"🔑 **वेरिफिकेशन कोड (OTP): {st.session_state['current_otp']}**")
                else:
                    st.error("❌ सही मोबाइल नंबर और नाम दर्ज करें।")
                    
        with col_reg2:
            otp_input = st.text_input("यहाँ प्राप्त OTP पिन डालें:", type="password").strip()
            
        if st.button("✅ रजिस्ट्रेशन कम्प्लीट करें", use_container_width=True):
            if "current_otp" in st.session_state and st.session_state["current_otp"] and otp_input == st.session_state["current_otp"]:
                save_row_to_sheet("Teachers", st.session_state["temp_register_data"])
                st.success(f"🎉 रजिस्ट्रेशन सफल! आपका लॉगिन पिन: {st.session_state['current_otp']} है।")
                st.session_state["current_otp"] = None
            else:
                st.error("❌ गलत OTP पिन!")

# ----------------- 🏫 लॉगिन के बाद मुख्य वेबसाइट इंटरफेस -----------------
else:
    user_row = teachers_df[teachers_df["Phone"] == st.session_state["current_user_phone"]].iloc[0]
    current_teacher_name = user_row["Name"]
    user_role = user_row["Role"]
    
    st.sidebar.markdown(f"### 👤 {current_teacher_name} ({user_role})")
    
    menu_options = ["📅 आज की नई एंट्री", "🔍 मेरी डायरी का स्टेटस (My Status)"]
    if user_role == "Admin":
        menu_options.append("📥 अप्रूवल विंडो (Approval Requests)")
        menu_options.append("📚 सिलेबस मैनेजमेंट (Syllabus Control)")
        menu_options.append("🛠️ एडमिन डैशबोर्ड (Teacher Management)")
        
    app_mode = st.sidebar.radio("📁 वेबसाइट मेनू:", menu_options)
    
    if st.sidebar.button("🔒 लॉगआउट (Logout)", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["current_user_phone"] = ""
        st.rerun()

    # --- मोड 1: आज की नई एंट्री ---
    if app_mode == "📅 आज की नई एंट्री":
        st.subheader("🆕 डेली डायरी एंट्री फॉर्म")
        
        col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
        with col_meta1:
            diary_date = st.date_input("📅 दिनांक:", date.today())
        with col_meta2:
            selected_period = st.selectbox("⏱️ पीरियड चुनें (Period):", [f"Period {i}" for i in range(1, 9)])
        with col_meta3:
            selected_class = st.radio("🏫 क्लास चुनें:", ["Class 9", "Class 10"], horizontal=True)
        with col_meta4:
            selected_subject = st.selectbox("📖 विषय चुनें:", ["Mathematics", "Science", "Social Science"])

        selected_section = st.selectbox("👥 सेक्शन चुनें:", ["Section A", "Section B", "Section C"] if selected_class == "Class 10" else ["Section A", "Section B"])

        st.markdown(f"### 📖 आज {selected_period} में कहाँ से कहाँ तक पढ़ाया?")
        col_page1, col_page2 = st.columns(2)
        with col_page1:
            start_page = st.number_input("📄 शुरूआती पेज:", min_value=1, value=1)
        with col_page2:
            end_page = st.number_input("📄 अंतिम पेज:", min_value=1, value=10)

        auto_topic, auto_hw = get_topics_and_hw_dynamic(selected_class, selected_subject, start_page, end_page)

        st.markdown("---")
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.info(f"**📖 ऑटो-डिटेक्टेड टॉपिक्स:**\n\n{auto_topic}")
        with col_res2:
            st.success(f"**📝 ऑटो-असाइंड होमवर्क:**\n\n{auto_hw}")

        teacher_remarks = st.text_input("✏️ कोई अन्य टिप्पणी/रिमार्क (Optional):")

        # WhatsApp Message Share Setup
        whatsapp_msg = (
            f"📝 *स्कूल डेली डायरी अपडेट*\n\n"
            f"👤 *शिक्षक:* {current_teacher_name}\n"
            f"📅 *दिनांक:* {diary_date.strftime('%d-%m-%Y')} | {selected_period}\n"
            f"🏫 *कक्षा:* {selected_class} - {selected_section}\n"
            f"📖 *विषय:* {selected_subject}\n"
            f"📌 *आज पढ़ाया गया टॉपिक:*\n{auto_topic}\n\n"
            f"📝 *आज का गृहकार्य (Homework):*\n{auto_hw}\n"
            f"✏️ *टिप्पणी:* {teacher_remarks if teacher_remarks else 'N/A'}"
        )
        encoded_msg = urllib.parse.quote(whatsapp_msg)
        whatsapp_url = f"https://wa.me/?text={encoded_msg}"

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 प्रिंसिपल को अप्रूवल के लिए भेजें", use_container_width=True):
                new_data = {
                    "Diary_ID": str(random.randint(100000, 999999)),
                    "Teacher": current_teacher_name,
                    "Date": diary_date.strftime('%Y-%m-%d'),
                    "Period": selected_period,
                    "Subject": selected_subject,
                    "Class_Section": f"{selected_class} - {selected_section}",
                    "Page_Range": f"Page {start_page} to {end_page}",
                    "Topics": auto_topic,
                    "Homework": auto_hw,
                    "Remarks": teacher_remarks,
                    "Status": "⏳ Pending"
                }
                save_row_to_sheet("Diary", new_data)
                st.success("✅ डायरी सफलतापूर्वक प्रिंसिपल के पास अप्रूवल के लिए भेज दी गई है!")
                
        with col_btn2:
            st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">📢 Share Homework on WhatsApp</button></a>', unsafe_allow_html=True)

    # --- मोड 2: शिक्षक के लिए अपनी डायरी का स्टेटस देखना ---
    elif app_mode == "🔍 मेरी डायरी का स्टेटस (My Status)":
        st.subheader("📊 आपकी डायरी प्रविष्टियों का स्टेटस")
        my_records = diary_df[diary_df["Teacher"] == current_teacher_name]
        if my_records.empty:
            st.info("आपने अभी तक कोई एंट्री नहीं की है।")
        else:
            st.dataframe(my_records[["Date", "Period", "Class_Section", "Subject", "Topics", "Status"]], use_container_width=True)

    # --- मोड 3: प्रिंसिपल के लिए अप्रूवल विंडो ---
    elif app_mode == "📥 अप्रूवल विंडो (Approval Requests)":
        st.subheader("📥 शिक्षकों से प्राप्त पेंडिंग डायरी रिक्वेस्ट्स")
        pending_df = diary_df[diary_df["Status"] == "⏳ Pending"]
        
        if pending_df.empty:
            st.success("🎉 कोई भी पेंडिंग रिक्वेस्ट नहीं है।")
        else:
            for index, row in pending_df.iterrows():
                with st.expander(f"📋 {row['Teacher']} - {row['Class_Section']} ({row['Subject']}) | तारीख: {row['Date']}"):
                    st.write(f"**पीरियड:** {row['Period']} | **पेज रेंज:** {row['Page_Range']}")
                    st.info(f"**पढ़ाए गए टॉपिक:**\n{row['Topics']}")
                    st.success(f"**दिया गया गृहकार्य:**\n{row['Homework']}")
                    
                    col_app1, col_app2 = st.columns(2)
                    with col_app1:
                        if st.button("✅ Approve", key=f"app_{row['Diary_ID']}", use_container_width=True):
                            update_diary_status(row['Diary_ID'], "✅ Approved")
                            st.rerun()
                    with col_app2:
                        if st.button("❌ Reject", key=f"rej_{row['Diary_ID']}", use_container_width=True):
                            update_diary_status(row['Diary_ID'], "❌ Rejected")
                            st.rerun()

    # --- मोड 4: सिलेबस मैनेजमेंट डैशबोर्ड ---
    elif app_mode == "📚 सिलेबस मैनेजमेंट (Syllabus Control)":
        st.subheader("📚 पाठ्यपुस्तक सिलेबस मैनेजमेंट (प्रिंसिपल स्पेशल)")
        tab_s1, tab_s2 = st.tabs(["➕ नया टॉपिक/अध्याय जोड़ें", "❌ वर्तमान सिलेबस देखें और हटाएं"])
        
        with tab_s1:
            st.markdown("### ➕ नया टॉपिक लाइव जोड़ें")
            col_s_meta1, col_s_meta2 = st.columns(2)
            with col_s_meta1:
                s_class = st.selectbox("🏫 कक्षा (Class):", ["Class 9", "Class 10"])
            with col_s_meta2:
                s_sub = st.selectbox("📖 विषय (Subject):", ["Mathematics", "Science", "Social Science"])
                
            col_s_page1, col_s_page2 = st.columns(2)
            with col_s_page1:
                s_start = st.number_input("📄 शुरूआती पेज नंबर:", min_value=1, value=1, key="s_start")
            with col_s_page2:
                s_end = st.number_input("📄 अंतिम पेज नंबर:", min_value=1, value=10, key="s_end")
                
            s_topic = st.text_input("📝 अध्याय/टॉपिक का नाम:")
            s_hw = st.text_input("📝 डिफ़ॉल्ट गृहकार्य (Homework):")
            
            if st.button("💾 सिलेबस में शामिल करें", use_container_width=True):
                if s_topic.strip() != "" and s_end >= s_start:
                    new_topic = {
                        "Topic_ID": f"T{random.randint(100, 999)}", "Class": s_class, "Subject": s_sub,
                        "Start_Page": s_start, "End_Page": s_end, "Topic": s_topic, "Homework": s_hw
                    }
                    save_row_to_sheet("Syllabus", new_topic)
                    st.success(f"🎉 नया टॉपिक '{s_topic}' सफलतापूर्वक जोड़ दिया गया है!")
                else:
                    st.error("❌ कृपया सही विवरण भरें।")
                    
        with tab_s2:
            st.markdown("### 📋 वर्तमान एक्टिव सिलेबस लिस्ट")
            if syllabus_df.empty:
                st.warning("सिलेबस डेटाबेस खाली है।")
            else:
                for index, s_row in syllabus_df.iterrows():
                    col_list1, col_list2 = st.columns([5, 1])
                    with col_list1:
                        st.info(f"**[{s_row['Class']} - {s_row['Subject']}]** {s_row['Topic']} (Page {s_row['Start_Page']} to {s_row['End_Page']})")
                    with col_list2:
                        if st.button("🗑️ हटाएँ", key=f"del_{s_row['Topic_ID']}", use_container_width=True):
                            delete_syllabus_topic(s_row['Topic_ID'])
                            st.success("टॉपिक डिलीट कर दिया गया!")
                            st.rerun()

    # --- मोड 5: एडमिन डैशबोर्ड (टीचर और मास्टर रिकॉर्ड) ---
    elif app_mode == "🛠️ एडमिन डैशबोर्ड (Teacher Management)":
        st.subheader("🛠️ मास्टर कंट्रोल पैनल")
        tab_adm1, tab_adm2 = st.tabs(["👥 नए टीचर्स जोड़ें", "📊 स्वीकृत डायरी मास्टर डेटा"])
        
        with tab_adm1:
            st.markdown("### ➕ सीधे नए टीचर को जोड़ें")
            adm_t_name = st.text_input("टीचर का नाम:")
            adm_t_phone = st.text_input("टीचर का मोबाइल नंबर (10 अंक):").strip()
            adm_t_pin = st.text_input("स्थायी पिन सेट करें:", value="1234").strip()
            
            if st.button("➕ टीचर रजिस्टर करें", use_container_width=True):
                if len(adm_t_phone) == 10 and adm_t_name.strip() != "":
                    new_t = {"Phone": adm_t_phone, "Name": adm_t_name, "PIN": adm_t_pin, "Role": "Teacher"}
                    save_row_to_sheet("Teachers", new_t)
                    st.success(f"🎉 शिक्षक {adm_t_name} को रजिस्टर कर दिया गया है!")
                else:
                    st.error("❌ कृपया सही विवरण भरें।")
                    
        with tab_adm2:
            st.markdown("### 📋 केवल स्वीकृत (Approved) डायरी का डेटाबेस")
            approved_only_df = diary_df[diary_df["Status"] == "✅ Approved"]
            if approved_only_df.empty:
                st.info("अभी तक कोई भी डायरी अप्रूव नहीं हुई है।")
            else:
                st.dataframe(approved_only_df, use_container_width=True)
                csv_data = approved_only_df.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 डाउनलोड एक्सेल मास्टर रिपोर्ट", data=csv_data, file_name=f"Approved_Diary_{date.today()}.csv", mime="text/csv", use_container_width=True)
                 
