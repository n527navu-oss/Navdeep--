import streamlit as st
import pandas as pd
from datetime import date
import random
import urllib.parse

# वेबसाइट का लेआउट और टाइटल सेट करना
st.set_page_config(page_title="MIS Complete School Diary", layout="wide", page_icon="🏛️")

st.title("🏛️ MIS Portal & Complete Syllabus Management System")
st.markdown("---")

# ----------------- 🔗 DATABASE INITIALIZATION & FALLBACKS -----------------
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
                # === CLASS 9 MATHEMATICS ===
                {"Topic_ID": "M901", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 1, "End_Page": 22, "Topic": "Ch 1: संख्या पद्धति (Number Systems) - अपरिमेय संख्याएं, दशमलव प्रसार, हर का परिमेयकरण", "Homework": "Ex 1.1 to 1.5 Selected Questions"},
                {"Topic_ID": "M902", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 23, "End_Page": 44, "Topic": "Ch 2: बहुपद (Polynomials) - शून्यक, शेषफल प्रमेय, बीजीय सर्वसमिकाएं", "Homework": "Ex 2.1 to 2.5 Selected Questions"},
                {"Topic_ID": "M903", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 45, "End_Page": 54, "Topic": "Ch 3: निर्देशांक ज्यामिति (Coordinate Geometry) - कार्तीय पद्धति, आलेखन", "Homework": "Ex 3.1 & 3.2 Complete"},
                {"Topic_ID": "M904", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 55, "End_Page": 70, "Topic": "Ch 4: दो चरों वाले रैखिक समीकरण - मानक रूप, समीकरण के हल, आलेख", "Homework": "Ex 4.1 & 4.2 Complete"},
                {"Topic_ID": "M905", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 71, "End_Page": 84, "Topic": "Ch 5: यूक्लिड की ज्यामिति का परिचय - अभिगृहीत, धारणाएं और प्रमेय", "Homework": "Ex 5.1 Complete"},
                {"Topic_ID": "M906", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 85, "End_Page": 108, "Topic": "Ch 6: रेखाएं और कोण (Lines and Angles) - आसन्न कोण, समांतर व तिर्यक रेखाएं", "Homework": "Ex 6.1 & 6.2 Selected Qs"},
                {"Topic_ID": "M907", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 109, "End_Page": 138, "Topic": "Ch 7: त्रिभुज (Triangles) - सर्वांगसमता की कसौटियाँ (SAS, ASA, SSS, RHS)", "Homework": "Ex 7.1 to 7.3 Selected Qs"},
                {"Topic_ID": "M908", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 139, "End_Page": 154, "Topic": "Ch 8: चतुर्भुज (Quadrilaterals) - समांतर चतुर्भुज के गुण, मध्य-बिंदु प्रमेय", "Homework": "Ex 8.1 & 8.2 Complete"},
                {"Topic_ID": "M909", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 155, "End_Page": 182, "Topic": "Ch 9: वृत्त (Circles) - जीवा द्वारा अंतरित कोण, चक्रीय चतुर्भुज", "Homework": "Ex 9.1 to 9.3 Selected Qs"},
                {"Topic_ID": "M910", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 183, "End_Page": 194, "Topic": "Ch 10: हीरोन का सूत्र (Heron's Formula) - त्रिभुज का क्षेत्रफल ज्ञात करना", "Homework": "Ex 10.1 Complete"},
                {"Topic_ID": "M911", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 195, "End_Page": 208, "Topic": "Ch 11: पृष्ठीय क्षेत्रफल और आयतन - शंकु, गोले और अर्धगोले", "Homework": "Ex 11.1 to 11.4 Selected Qs"},
                {"Topic_ID": "M912", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 209, "End_Page": 220, "Topic": "Ch 12: सांख्यिकी (Statistics) - आंकड़ों का आलेखीय निरूपण (दंड, आयत चित्र)", "Homework": "Ex 12.1 Complete"},
                # === CLASS 9 SCIENCE ===
                {"Topic_ID": "S901", "Class": "Class 9", "Subject": "Science", "Start_Page": 1, "End_Page": 13, "Topic": "Ch 1: हमारे आस-पास के पदार्थ - वाष्पीकरण, तापमान प्रभाव", "Homework": "आंतरिक प्रश्न 1-5"},
                {"Topic_ID": "S902", "Class": "Class 9", "Subject": "Science", "Start_Page": 14, "End_Page": 31, "Topic": "Ch 2: क्या हमारे आस-पास के पदार्थ शुद्ध हैं - विलयन, कोलाइड", "Homework": "अभ्यास प्रश्न 1 से 5"},
                {"Topic_ID": "S903", "Class": "Class 9", "Subject": "Science", "Start_Page": 32, "End_Page": 45, "Topic": "Ch 3: परमाणु एवं अणु - रासायनिक संयोजन के नियम, मोल संकल्पना", "Homework": "रासायनिक सूत्र बनाना"},
                {"Topic_ID": "S904", "Class": "Class 9", "Subject": "Science", "Start_Page": 46, "End_Page": 56, "Topic": "Ch 4: परमाणु की संरचना - थॉमसन, रदरफोर्ड, बोर मॉडल", "Homework": "इलेक्ट्रॉनिक विन्यास"},
                {"Topic_ID": "S905", "Class": "Class 9", "Subject": "Science", "Start_Page": 57, "End_Page": 68, "Topic": "Ch 5: जीवन की मौलिक इकाई - कोशिका, माइटोकॉन्ड्रिया, प्लाज्मा", "Homework": "कोशिका का चित्र"},
                {"Topic_ID": "S906", "Class": "Class 9", "Subject": "Science", "Start_Page": 69, "End_Page": 86, "Topic": "Ch 6: ऊतक (Tissues) - विभज्योतक, स्थायी व जंतु ऊतक प्रकार", "Homework": "जाइलम और फ्लोएम में अंतर"},
                {"Topic_ID": "S907", "Class": "Class 9", "Subject": "Science", "Start_Page": 87, "End_Page": 104, "Topic": "Ch 7: गति (Motion) - दूरी, विस्थापन, वेग, गति के तीन समीकरण", "Homework": " गति के आंकिक प्रश्न"},
                {"Topic_ID": "S908", "Class": "Class 9", "Subject": "Science", "Start_Page": 105, "End_Page": 120, "Topic": "Ch 8: बल तथा गति के नियम - जड़त्व, न्यूटन के नियम, संवेग", "Homework": "संवेग के प्रश्न"},
                {"Topic_ID": "S909", "Class": "Class 9", "Subject": "Science", "Start_Page": 121, "End_Page": 138, "Topic": "Ch 9: गुरुत्वाकर्षण - सार्वत्रिक नियम, मुक्त पतन, उत्प्लावकता", "Homework": "G और g में अंतर"},
                {"Topic_ID": "S910", "Class": "Class 9", "Subject": "Science", "Start_Page": 139, "End_Page": 150, "Topic": "Ch 10: कार्य तथा ऊर्जा - गतिज व स्थितिज ऊर्जा, संरक्षण नियम", "Homework": "स्थितिज ऊर्जा का सूत्र"},
                {"Topic_ID": "S911", "Class": "Class 9", "Subject": "Science", "Start_Page": 151, "End_Page": 165, "Topic": "Ch 11: ध्वनि (Sound) - ध्वनि संचरण, अनुदैर्ध्य तरंगें, सोनार", "Homework": "सोनार की कार्यविधि"},
                {"Topic_ID": "S912", "Class": "Class 9", "Subject": "Science", "Start_Page": 166, "End_Page": 180, "Topic": "Ch 12: खाद्य संसाधनों में सुधार - फसल प्रबंधन, कुक्कुट व मत्स्य पालन", "Homework": "जैविक खाद के लाभ"},
                # === CLASS 9 SOCIAL SCIENCE ===
                {"Topic_ID": "SS901", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 1, "End_Page": 24, "Topic": "History Ch 1: फ्रांसीसी क्रांति - समाज, बास्तील पतन, आतंक का राज", "Homework": "फ्रांसीसी क्रांति के कारण"},
                {"Topic_ID": "SS902", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 25, "End_Page": 48, "Topic": "History Ch 2: यूरोप में समाजवाद एवं रूसी क्रांति - अक्टूबर क्रांति", "Homework": "रूसी क्रांति के प्रश्न"},
                {"Topic_ID": "SS903", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 49, "End_Page": 74, "Topic": "History Ch 3: नात्सीवाद और हिटलर का उदय - हिटलर का शासन", "Homework": "हिटलर के उदय के कारण"},
                {"Topic_ID": "SS904", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 75, "End_Page": 94, "Topic": "Geography Ch 1: भारत - आकार और स्थिति - मानक समय रेखा", "Homework": "मानचित्र कार्य"},
                {"Topic_ID": "SS905", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 95, "End_Page": 110, "Topic": "Geography Ch 2: भारत का भौतिक स्वरूप - हिमालय, मैदान, पठार", "Homework": "भौतिक प्रदेशों की तुलना"},
                {"Topic_ID": "SS906", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 111, "End_Page": 125, "Topic": "Geography Ch 3: अपवाह (Drainage) - नदियाँ और झीलें", "Homework": "नदी तंत्र का रेखाचित्र"},
                {"Topic_ID": "SS907", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 126, "End_Page": 140, "Topic": "Civics Ch 1: लोकतंत्र क्या? लोकतंत्र क्यों? - विशेषताएं", "Homework": "लोकतंत्र के गुण"},
                {"Topic_ID": "SS908", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 141, "End_Page": 155, "Topic": "Civics Ch 2: संविधान निर्माण - भारतीय संविधान सभा", "Homework": "संविधान की प्रस्तावना"},
                {"Topic_ID": "SS909", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 156, "End_Page": 170, "Topic": "Economics Ch 1: पालमपुर गाँव की कहानी - उत्पादन के कारक", "Homework": "हरित क्रांति के प्रभाव"},
                {"Topic_ID": "SS910", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 171, "End_Page": 190, "Topic": "Economics Ch 2: resource के रूप में लोग - साक्षरता, बेरोजगारी", "Homework": "बेरोजगारी पर टिप्पणी"},
                # === CLASS 10 MATHEMATICS ===
                {"Topic_ID": "M1001", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 1, "End_Page": 18, "Topic": "Ch 1: वास्तविक संख्याएं (Real Numbers) - अंकगणित की आधारभूत प्रमेय, अपरिमेयता", "Homework": "Ex 1.1 & 1.2 Complete"},
                {"Topic_ID": "M1002", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 19, "End_Page": 38, "Topic": "Ch 2: बहुपद (Polynomials) - शून्यकों का ज्यामितीय अर्थ, गुणांकों में संबंध", "Homework": "Ex 2.1 & 2.2 Complete"},
                {"Topic_ID": "M1003", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 39, "End_Page": 70, "Topic": "Ch 3: रैखिक समीकरण युग्म - प्रतिस्थापन, विलोपन विधि", "Homework": "Ex 3.1 to 3.3 Selected Qs"},
                {"Topic_ID": "M1004", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 71, "End_Page": 98, "Topic": "Ch 4: द्विघात समीकरण (Quadratic Equations) - गुणनखंड हल, द्विघाती सूत्र", "Homework": "Ex 4.1 to 4.3 Selected Qs"},
                {"Topic_ID": "M1005", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 99, "End_Page": 124, "Topic": "Ch 5: समांतर श्रेढ़ियाँ (AP) - n-वाँ पद और n पदों का योग", "Homework": "Ex 5.2 & 5.3 Selected Qs"},
                {"Topic_ID": "M1006", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 125, "End_Page": 164, "Topic": "Ch 6: त्रिभुज (Triangles) - समरूपता कसौटियाँ, थेल्स प्रमेय (BPT)", "Homework": "Ex 6.1 & 6.2 Complete"},
                {"Topic_ID": "M1007", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 165, "End_Page": 186, "Topic": "Ch 7: निर्देशांक ज्यामिति - दूरी सूत्र, विभाजन सूत्र", "Homework": "Ex 7.1 & 7.2 Complete"},
                {"Topic_ID": "M1008", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 187, "End_Page": 214, "Topic": "Ch 8: त्रिकोणमिति का परिचय - अनुपात, विशिष्ट कोण, सर्वसमिकाएं", "Homework": "Ex 8.1 & 8.3 Selected Qs"},
                {"Topic_ID": "M1009", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 215, "End_Page": 232, "Topic": "Ch 9: त्रिकोणमिति के अनुप्रयोग - ऊँचाई और दूरी, उन्नयन कोण", "Homework": "Ex 9.1 Q1-Q8"},
                {"Topic_ID": "M1010", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 233, "End_Page": 248, "Topic": "Ch 10: वृत्त (Circles) - स्पर्श रेखाएं, प्रमेय", "Homework": "Ex 10.2 Complete"},
                {"Topic_ID": "M1011", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 249, "End_Page": 264, "Topic": "Ch 11: वृत्तों से संबंधित क्षेत्रफल - त्रिज्यखंड व वृत्तखंड", "Homework": "Ex 11.1 Complete"},
                {"Topic_ID": "M1012", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 265, "End_Page": 276, "Topic": "Ch 12: पृष्ठीय क्षेत्रफल और आयतन - संयोजन का क्षेत्रफल व आयतन", "Homework": "Ex 12.1 Selected Qs"},
                {"Topic_ID": "M1013", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 277, "End_Page": 296, "Topic": "Ch 13: सांख्यिकी (Statistics) - माध्य, बहुलक, माध्यक", "Homework": "Ex 13.1 to 13.3 Selected Qs"},
                {"Topic_ID": "M1014", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 297, "End_Page": 312, "Topic": "Ch 14: प्रायिकता (Probability) - ताश व पासे के प्रश्न", "Homework": "Ex 14.1 Q1-Q15"},
                # === CLASS 10 SCIENCE ===
                {"Topic_ID": "S1001", "Class": "Class 10", "Subject": "Science", "Start_Page": 1, "End_Page": 17, "Topic": "Ch 1: रासायनिक अभिक्रियाएं एवं समीकरण - संतुलन, विस्थापन, रेडॉक्स", "Homework": "समीकरण संतुलित करना"},
                {"Topic_ID": "S1002", "Class": "Class 10", "Subject": "Science", "Start_Page": 18, "End_Page": 37, "Topic": "Ch 2: अम्ल, क्षारक एवं लवण - pH पैमाना, बेकिंग सोड़ा, पीओपी", "Homework": "लवणों के रासायनिक सूत्र"},
                {"Topic_ID": "S1003", "Class": "Class 10", "Subject": "Science", "Start_Page": 38, "End_Page": 59, "Topic": "Ch 3: धातु एवं अधातु - सक्रियता श्रेणी, आयनिक यौगिक, निष्कर्षण", "Homework": "धातुओं के रासायनिक अंतर"},
                {"Topic_ID": "S1004", "Class": "Class 10", "Subject": "Science", "Start_Page": 60, "End_Page": 79, "Topic": "Ch 4: carbon एवं उसके यौगिक - सहसंयोजी आबंध, IUPAC नामकरण", "Homework": "साबुन की शोधन क्रिया"},
                {"Topic_ID": "S1005", "Class": "Class 10", "Subject": "Science", "Start_Page": 80, "End_Page": 98, "Topic": "Ch 5: जैव प्रक्रम - मानव पाचन, श्वसन, परिसंचरण, उत्सर्जन", "Homework": "नेफ्रॉन की संरचना का चित्र"},
                {"Topic_ID": "S1006", "Class": "Class 10", "Subject": "Science", "Start_Page": 99, "End_Page": 114, "Topic": "Ch 6: नियंत्रण एवं समन्वय - न्यूरॉन, प्रतिवर्ती चाप, पादप हार्मोन", "Homework": "मस्तिष्क के मुख्य भाग"},
                {"Topic_ID": "S1007", "Class": "Class 10", "Subject": "Science", "Start_Page": 115, "End_Page": 132, "Topic": "Ch 7: जीव जनन कैसे करते हैं - पुष्प संरचना, मानव लैंगिक जनन", "Homework": "नर व मादा जनन तंत्र"},
                {"Topic_ID": "S1008", "Class": "Class 10", "Subject": "Science", "Start_Page": 133, "End_Page": 149, "Topic": "Ch 8: आनुवंशिकता - मेंडेल के नियम, लिंग निर्धारण", "Homework": "लिंग निर्धारण का आरेख"},
                {"Topic_ID": "S1009", "Class": "Class 10", "Subject": "Science", "Start_Page": 150, "End_Page": 169, "Topic": "Ch 9: प्रकाश – परावर्तन तथा अपवर्तन - किरण आरेख, लेंस सूत्र", "Homework": "लेंस के आंकिक प्रश्न"},
                {"Topic_ID": "S1010", "Class": "Class 10", "Subject": "Science", "Start_Page": 170, "End_Page": 184, "Topic": "Ch 10: मानव नेत्र तथा संसार - निकट/दीर्घ दृष्टि दोष, प्रिज्म विक्षेपण", "Homework": "दृष्टि दोष निवारण आरेख"},
                {"Topic_ID": "S1011", "Class": "Class 10", "Subject": "Science", "Start_Page": 185, "End_Page": 204, "Topic": "Ch 11: विद्युत (Electricity) - ओम का नियम, श्रेणी/समांतर क्रम संयोजन", "Homework": "विद्युत के आंकिक प्रश्न"},
                {"Topic_ID": "S1012", "Class": "Class 10", "Subject": "Science", "Start_Page": 205, "End_Page": 218, "Topic": "Ch 12: विद्युत धारा के चुंबकीय प्रभाव - चुंबकीय क्षेत्र, फ्लेमिंग नियम", "Homework": "फ्लेमिंग का वामहस्त नियम"},
                {"Topic_ID": "S1013", "Class": "Class 10", "Subject": "Science", "Start_Page": 219, "End_Page": 230, "Topic": "Ch 13: हमारा पर्यावरण - पारितंत्र, ओजोन परत अवक्षय", "Homework": "आहार श्रृंखला का चित्र"},
                # === CLASS 10 SOCIAL SCIENCE ===
                {"Topic_ID": "SS1001", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 1, "End_Page": 28, "Topic": "History Ch 1: यूरोप में राष्ट्रवाद का उदय - वियना कांग्रेस, जर्मनी एकीकरण", "Homework": "यूरोप में राष्ट्रवाद के प्रश्न"},
                {"Topic_ID": "SS1002", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 29, "End_Page": 52, "Topic": "History Ch 2: भारत में राष्ट्रवाद - असहयोग, सविनय अवज्ञा आंदोलन", "Homework": "दांडी यात्रा का महत्व"},
                {"Topic_ID": "SS1003", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 53, "End_Page": 76, "Topic": "Geography Ch 1: संसाधन एवं विकास - वर्गीकरण, मृदा प्रकार", "Homework": "मृदा अपरदन रोकने के उपाय"},
                {"Topic_ID": "SS1004", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 77, "End_Page": 92, "Topic": "Geography Ch 2: वन एवं वन्य जीव - जैव विविधता, संकटग्रस्त जातियां", "Homework": "चिपको आंदोलन पर नोट"},
                {"Topic_ID": "SS1005", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 93, "End_Page": 110, "Topic": "Geography Ch 3: जल संसाधन - बहुउद्देशीय परियोजनाएं, जल संग्रहण", "Homework": "वर्षा जल संग्रहण के लाभ"},
                {"Topic_ID": "SS1006", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 111, "End_Page": 130, "Topic": "Civics Ch 1: सत्ता की साझेदारी - बेल्जियम और श्रीलंका का उदाहरण", "Homework": "सत्ता की साझेदारी क्यों आवश्यक है"},
                {"Topic_ID": "SS1007", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 131, "End_Page": 150, "Topic": "Civics Ch 2: संघवाद - संघीय व्यवस्था, भारत में विकेंद्रीकरण", "Homework": "स्थानीय सरकारों के कार्य"},
                {"Topic_ID": "SS1008", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 151, "End_Page": 168, "Topic": "Economics Ch 1: विकास (Development) - प्रति व्यक्ति आय, एचडीआई", "Homework": "विकास के लक्ष्य अलग क्यों होते हैं"},
                {"Topic_ID": "SS1009", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 169, "End_Page": 190, "Topic": "Economics Ch 2: भारतीय अर्थव्यवस्था के क्षेत्रक - प्राथमिक, द्वितीयक, तृतीयक", "Homework": "संगठित और असंगठित क्षेत्रक"}
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

# डेटाबेस लाइव लोड करना
teachers_df = load_data_from_sheet("Teachers")
diary_df = load_data_from_sheet("Diary")
syllabus_df = load_data_from_sheet("Syllabus")

# 🔍 लाइव डेटाबेस से सर्च करने वाला फंक्शन
def get_topics_and_hw_dynamic(selected_class, selected_subject, start_p, end_p):
    found_topics = []
    found_homework = []
    matched_data = syllabus_df[(syllabus_df["Class"] == selected_class) & (syllabus_df["Subject"] == selected_subject)]
    for index, item in matched_data.iterrows():
        if not (end_p < int(item["Start_Page"]) or start_p > int(item["End_Page"])):
            t_name = item.get("Topic", item.get("topic", "No Title"))
            found_topics.append(t_name)
            found_homework.append(item["Homework"])
    if not found_topics:
        return "इस पेज रेंज के लिए कोई टॉपिक नहीं मिला।", "N/A"
    return "\n".join(found_topics), " | ".join(found_homework)

# ----------------- 🔐 लॉगिन एवं रजिस्ट्रेशन -----------------
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
            else: st.error("❌ गलत मोबाइल नंबर या पिन!")
    with tab2:
        st.subheader("नया शिक्षक खाता")
        reg_name = st.text_input("शिक्षक का पूरा नाम:")
        reg_phone = st.text_input("मोबाइल नंबर (10 अंक):").strip()
        col_reg1, col_reg2 = st.columns(2)
        with col_reg1:
            if st.button("🔢 OTP पिन जनरेट करें", use_container_width=True):
                if len(reg_phone) == 10 and reg_phone.isdigit() and reg_name.strip() != "":
                    if reg_phone in teachers_df["Phone"].values: st.warning("⚠️ यह नंबर पहले से रजिस्टर्ड है!")
                    else:
                        st.session_state["current_otp"] = str(random.randint(1000, 9999))
                        st.session_state["temp_register_data"] = {"Phone": reg_phone, "Name": reg_name, "PIN": st.session_state["current_otp"], "Role": "Teacher"}
                        st.info(f"🔑 **वेरिफिकेशन कोड (OTP): {st.session_state['current_otp']}**")
                else: st.error("❌ सही मोबाइल नंबर और नाम दर्ज करें।")
        with col_reg2: otp_input = st.text_input("यहाँ प्राप्त OTP पिन डालें:", type="password").strip()
        if st.button("✅ रजिस्ट्रेशन कम्प्लीट करें", use_container_width=True):
            if "current_otp" in st.session_state and st.session_state["current_otp"] and otp_input == st.session_state["current_otp"]:
                save_row_to_sheet("Teachers", st.session_state["temp_register_data"])
                st.success(f"🎉 रजिस्ट्रेशन सफल! आपका लॉगिन पिन: {st.session_state['current_otp']} है।")
                st.session_state["current_otp"] = None
            else: st.error("❌ गलत OTP पिन!")

# ----------------- 🏫 लॉगिन के बाद मुख्य वेबसाइट इंटरफेस -----------------
else:
    user_row = teachers_df[teachers_df["Phone"] == st.session_state["current_user_phone"]].iloc[0]
    current_teacher_name = user_row["Name"]
    user_role = user_row["Role"]
    st.sidebar.markdown(f"### 👤 {current_teacher_name} ({user_role})")
    menu_options = ["📅 आज की नई एंट्री", "🔍 मेरी डायरी का स्टेटस (My Status)"]
    if user_role == "Admin":
        menu_options.extend(["📥 अप्रूवल विंडो (Approval Requests)", "📚 सिलेबस मैनेजमेंट (Syllabus Control)", "🛠️ एडमिन डैशबोर्ड (Teacher Management)"])
    app_mode = st.sidebar.radio("📁 वेबसाइट मेनू:", menu_options)
    if st.sidebar.button("🔒 लॉगआउट (Logout)", use_container_width=True):
        st.session_state["logged_in"] = False
        st.session_state["current_user_phone"] = ""
        st.rerun()

    if app_mode == "📅 आज की नई एंट्री":
        st.subheader("🆕 डेली डायरी एंट्री फॉर्म")
        col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
        with col_meta1: diary_date = st.date_input("📅 दिनांक:", date.today())
        with col_meta2: selected_period = st.selectbox("⏱️ पीरियड चुनें (Period):", [f"Period {i}" for i in range(1, 9)])
        with col_meta3: selected_class = st.radio("🏫 क्लास चुनें:", ["Class 9", "Class 10"], horizontal=True)
        with col_meta4: selected_subject = st.selectbox("📖 विषय चुनें:", ["Mathematics", "Science", "Social Science"])
        selected_section = st.selectbox("👥 सेक्शन चुनें:", ["Section A", "Section B", "Section C"] if selected_class == "Class 10" else ["Section A", "Section B"])
        col_page1, col_page2 = st.columns(2)
        with col_page1: start_page = st.number_input("📄 शुरूआती पेज:", min_value=1, value=1)
        with col_page2: end_page = st.number_input("📄 अंतिम पेज:", min_value=1, value=10)
        auto_topic, auto_hw = get_topics_and_hw_dynamic(selected_class, selected_subject, start_page, end_page)
        st.markdown("---")
        col_res1, col_res2 = st.columns(2)
        with col_res1: st.info(f"**📖 ऑटो-डिटेक्टेड टॉपिक्स:**\n\n{auto_topic}")
        with col_res2: st.success(f"**📝 ऑटो-असाइंड होमवर्क:**\n\n{auto_hw}")
        teacher_remarks = st.text_input("✏️ कोई अन्य टिप्पणी/रिमार्क (Optional):")
        whatsapp_msg = f"📝 *स्कूल डेली डायरी अपडेट*\n\n👤 *शिक्षक:* {current_teacher_name}\n📅 *दिनांक:* {diary_date.strftime('%d-%m-%Y')} | {selected_period}\n🏫 *कक्षा:* {selected_class} - {selected_section}\n📖 *विषय:* {selected_subject}\n📌 *आज पढ़ाया गया टॉपिक:*\n{auto_topic}\n\n📝 *आज का गृहकार्य (Homework):*\n{auto_hw}"
        whatsapp_url = f"https://wa.me/?text={urllib.parse.quote(whatsapp_msg)}"
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚀 प्रिंसिपल को अप्रूवल के लिए भेजें", use_container_width=True):
                new_data = {"Diary_ID": str(random.randint(100000, 999999)), "Teacher": current_teacher_name, "Date": diary_date.strftime('%Y-%m-%d'), "Period": selected_period, "Subject": selected_subject, "Class_Section": f"{selected_class} - {selected_section}", "Page_Range": f"Page {start_page} to {end_page}", "Topics": auto_topic, "Homework": auto_hw, "Remarks": teacher_remarks, "Status": "⏳ Pending"}
                save_row_to_sheet("Diary", new_data)
                st.success("✅ डायरी सफलतापूर्वक प्रिंसिपल के पास भेज दी गई है!")
        with col_btn2: st.markdown(f'<a href="{whatsapp_url}" target="_blank"><button style="width:100%; padding:10px; background-color:#25D366; color:white; border:none; border-radius:5px; font-weight:bold; cursor:pointer;">📢 Share Homework on WhatsApp</button></a>', unsafe_allow_html=True)

    elif app_mode == "🔍 मेरी डायरी का स्टेटस (My Status)":
        st.subheader("📊 आपकी डायरी प्रविष्टियों का स्टेटस")
        my_records = diary_df[diary_df["Teacher"] == current_teacher_name]
        if my_records.empty: st.info("आपने अभी तक कोई एंट्री नहीं की है।")
        else: st.dataframe(my_records[["Date", "Period", "Class_Section", "Subject", "Topics", "Status"]], use_container_width=True)

    elif app_mode == "📥 अप्रूवल विंडो (Approval Requests)":
        st.subheader("📥 शिक्षकों से प्राप्त पेंडिंग डायरी रिक्वेस्ट्स")
        pending_df = diary_df[diary_df["Status"] == "⏳ Pending"]
        if pending_df.empty: st.success("🎉 कोई भी पेंडिंग रिक्वेस्ट नहीं है।")
        else:
            for index, row in pending_df.iterrows():
                with st.expander(f"📋 {row['Teacher']} - {row['Class_Section']} ({row['Subject']})"):
                    st.info(f"**पढ़ाए गए टॉपिक:**\n{row['Topics']}\n\n**गृहकार्य:** {row['Homework']}")
                    col_app1, col_app2 = st.columns(2)
                    with col_app1:
                        if st.button("✅ Approve", key=f"app_{row['Diary_ID']}", use_container_width=True): update_diary_status(row['Diary_ID'], "✅ Approved"); st.rerun()
                    with col_app2:
                        if st.button("❌ Reject", key=f"rej_{row['Diary_ID']}", use_container_width=True): update_diary_status(row['Diary_ID'], "❌ Rejected"); st.rerun()

    elif app_mode == "📚 सिलेबस मैनेजमेंट (Syllabus Control)":
        st.subheader("📚 पाठ्यपुस्तक सिलेबस मैनेजमेंट")
        tab_s1, tab_s2 = st.tabs(["➕ नया टॉपिक जोड़ें", "❌ सिलेबस हटाएं"])
        with tab_s1:
            s_class = st.selectbox("🏫 कक्षा:", ["Class 9", "Class 10"])
            s_sub = st.selectbox("📖 विषय:", ["Mathematics", "Science", "Social Science"])
            s_start = st.number_input("📄 शुरूआती पेज:", min_value=1, value=1)
            s_end = st.number_input("📄 अंतिम पेज:", min_value=1, value=10)
            s_topic = st.text_input("📝 टॉपिक नाम:")
            s_hw = st.text_input("📝 गृहकार्य:")
            if st.button("💾 सिलेबस में शामिल करें", use_container_width=True):
                if s_topic.strip() != "" and s_end >= s_start:
                    save_row_to_sheet("Syllabus", {"Topic_ID": f"T{random.randint(100, 999)}", "Class": s_class, "Subject": s_sub, "Start_Page": s_start, "End_Page": s_end, "Topic": s_topic, "Homework": s_hw})
                    st.success("🎉 नया टॉपिक जुड़ गया!")
        with tab_s2:
            for index, s_row in syllabus_df.iterrows():
                t_title = s_row.get("Topic", s_row.get("topic", "No Title"))
                col_l1, col_l2 = st.columns([5, 1])
                with col_l1: st.info(f"**[{s_row['Class']} - {s_row['Subject']}]** {t_title}")
                with col_l2:
                    if st.button("🗑️", key=f"del_{s_row['Topic_ID']}", use_container_width=True): delete_syllabus_topic(s_row['Topic_ID']); st.success("हटाया गया!"); st.rerun()

    elif app_mode == "🛠️ एडमिन डैशबोर्ड (Teacher Management)":
        st.subheader("🛠️ मास्टर कंट्रोल पैनल")
        adm_t_name = st.text_input("टीचर का नाम:")
        adm_t_phone = st.text_input("मोबाइल नंबर (10 अंक):").strip()
        adm_t_pin = st.text_input("स्थायी पिन सेट करें:", value="1234").strip()
        if st.button("➕ टीचर रजिस्टर करें", use_container_width=True):
            if len(adm_t_phone) == 10 and adm_t_name.strip() != "":
                save_row_to_sheet("Teachers", {"Phone": adm_t_phone, "Name": adm_t_name, "PIN": adm_t_pin, "Role": "Teacher"})
                st.success("🎉 शिक्षक रजिस्टर हो गए!")
        st.markdown("---")
        approved_only_df = diary_df[diary_df["Status"] == "✅ Approved"]
        st.dataframe(approved_only_df, use_container_width=True)
        st.download_button(label="📥 डाउनलोड एक्सेल", data=approved_only_df.to_csv(index=False).encode('utf-8'), file_name=f"Approved_Diary_{date.today()}.csv", mime="text/csv", use_container_width=True)
                     
