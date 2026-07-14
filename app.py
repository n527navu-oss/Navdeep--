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
            # 📚 संपूर्ण एनसीईआरटी कक्षा 9 और 10 का एम्बेडेड डेटाबेस
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
                {"Topic_ID": "M911", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 195, "End_Page": 208, "Topic": "Ch 11: पृष्ठीय क्षेत्रफल और आयतन - लंब वृत्तीय शंकु, गोले और अर्धगोले", "Homework": "Ex 11.1 to 11.4 Selected Qs"},
                {"Topic_ID": "M912", "Class": "Class 9", "Subject": "Mathematics", "Start_Page": 209, "End_Page": 220, "Topic": "Ch 12: सांख्यिकी (Statistics) - आंकड़ों का आलेखीय निरूपण (दंड, आयत चित्र)", "Homework": "Ex 12.1 Complete"},

                # === CLASS 9 SCIENCE ===
                {"Topic_ID": "S901", "Class": "Class 9", "Subject": "Science", "Start_Page": 1, "End_Page": 13, "topic": "Ch 1: हमारे आस-पास के पदार्थ - अवस्थाएं, वाष्पीकरण, तापमान प्रभाव", "Homework": "पाठ्यपुस्तक के आंतरिक प्रश्न 1-5"},
                {"Topic_ID": "S902", "Class": "Class 9", "Subject": "Science", "Start_Page": 14, "End_Page": 31, "topic": "Ch 2: क्या हमारे आस-पास के पदार्थ शुद्ध हैं - विलयन, कोलाइड, निलंबन", "Homework": "अभ्यास प्रश्न 1 से 5"},
                {"Topic_ID": "S903", "Class": "Class 9", "Subject": "Science", "Start_Page": 32, "End_Page": 45, "topic": "Ch 3: परमाणु एवं अणु - रासायनिक संयोजन के नियम, मोल संकल्पना, सूत्र", "Homework": "अणुभार और रासायनिक सूत्र बनाना"},
                {"Topic_ID": "S904", "Class": "Class 9", "Subject": "Science", "Start_Page": 46, "End_Page": 56, "topic": "Ch 4: परमाणु की संरचना - थॉमसन, रदरफोर्ड, बोर मॉडल, संयोजकता", "Homework": "प्रथम 18 तत्वों के इलेक्ट्रॉनिक विन्यास"},
                {"Topic_ID": "S905", "Class": "Class 9", "Subject": "Science", "Start_Page": 57, "End_Page": 68, "topic": "Ch 5: जीवन की मौलिक इकाई - कोशिका, अंगक, माइटोकॉन्ड्रिया, प्लाज्मा", "Homework": "पादप और जंतु कोशिका का नामांकित चित्र"},
                {"Topic_ID": "S906", "Class": "Class 9", "Subject": "Science", "Start_Page": 69, "End_Page": 86, "topic": "Ch 6: ऊतक (Tissues) - विभज्योतक, स्थायी ऊतक, जंतु ऊतक प्रकार", "Homework": "पेरेन्काइमा और स्क्लेरेन्काइमा में अंतर"},
                {"Topic_ID": "S907", "Class": "Class 9", "Subject": "Science", "Start_Page": 87, "End_Page": 104, "topic": "Ch 7: गति (Motion) - दूरी, विस्थापन, वेग, त्वरण, गति के तीन समीकरण", "Homework": "गति के समीकरणों पर आधारित आंकिक प्रश्न"},
                {"Topic_ID": "S908", "Class": "Class 9", "Subject": "Science", "Start_Page": 105, "End_Page": 120, "topic": "Ch 8: बल तथा गति के नियम - जड़त्व, न्यूटन के नियम, संवेग संरक्षण", "Homework": "न्यूटन के द्वितीय नियम का गणितीय रूप"},
                {"Topic_ID": "S909", "Class": "Class 9", "Subject": "Science", "Start_Page": 121, "End_Page": 138, "topic": "Ch 9: गुरुत्वाकर्षण - सार्वत्रिक नियम, मुक्त पतन, उत्प्लावकता, भार", "Homework": "द्रव्यमान और भार में अंतर स्पष्ट करें"},
                {"Topic_ID": "S910", "Class": "Class 9", "Subject": "Science", "Start_Page": 139, "End_Page": 150, "topic": "Ch 10: कार्य तथा ऊर्जा - कार्य, गतिज ऊर्जा, स्थितिज ऊर्जा, संरक्षण नियम", "Homework": "स्थितिज ऊर्जा का सूत्र व्युत्पन्न करना"},
                {"Topic_ID": "S911", "Class": "Class 9", "Subject": "Science", "Start_Page": 151, "End_Page": 165, "topic": "Ch 11: ध्वनि (Sound) - ध्वनि संचरण, अनुदैर्ध्य तरंगें, पराश्रव्य ध्वनि, सोनार", "Homework": "सोनार (SONAR) की कार्यविधि चित्र सहित"},
                {"Topic_ID": "S912", "Class": "Class 9", "Subject": "Science", "Start_Page": 166, "End_Page": 180, "topic": "Ch 12: खाद्य संसाधनों में सुधार - फसल प्रबंधन, कुक्कुट व मत्स्य पालन", "Homework": "जैविक खाद और रासायनिक उर्वरक में अंतर"},

                # === CLASS 9 SOCIAL SCIENCE ===
                {"Topic_ID": "SS901", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 1, "End_Page": 24, "Topic": "History Ch 1: फ्रांसीसी क्रांति - समाज, बास्तील पतन, आतंक का राज", "Homework": "फ्रांसीसी क्रांति के सामाजिक कारणों का वर्णन"},
                {"Topic_ID": "SS902", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 25, "End_Page": 48, "Topic": "History Ch 2: यूरोप में समाजवाद एवं रूसी क्रांति - जार का शासन, अक्टूबर क्रांति", "Homework": "बोल्शेविकों और मेन्शेविकों में अंतर"},
                {"Topic_ID": "SS903", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 49, "End_Page": 74, "Topic": "History Ch 3: नात्सीवाद और हिटलर का उदय - प्रोपेगैंडा, यहूदियों पर अत्याचार", "Homework": "हिटलर के उदय के प्रमुख कारण"},
                {"Topic_ID": "SS904", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 75, "End_Page": 94, "Topic": "Geography Ch 1: भारत - आकार और स्थिति - मानक समय रेखा, पड़ोसी देश", "Homework": "मानचित्र: भारत के तटीय राज्य अंकित करना"},
                {"Topic_ID": "SS905", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 95, "End_Page": 110, "Topic": "Geography Ch 2: भारत का भौतिक स्वरूप - हिमालय, विशाल मैदान, थार मरुस्थल", "Homework": "पूर्वी घाट और पश्चिमी घाट की तुलना"},
                {"Topic_ID": "SS906", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 111, "End_Page": 125, "Topic": "Geography Ch 3: अपवाह (Drainage) - हिमालयी और प्रायद्वीपीय नदियाँ, झीलें", "Homework": "गंगा नदी तंत्र का रेखाचित्र"},
                {"Topic_ID": "SS907", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 126, "End_Page": 140, "Topic": "Civics Ch 1: लोकतंत्र क्या? लोकतंत्र क्यों? - परिभाषा, विशेषताएं, महत्त्व", "Homework": "लोकतंत्र के पांच प्रमुख गुणों की सूची"},
                {"Topic_ID": "SS908", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 141, "End_Page": 155, "Topic": "Civics Ch 2: संविधान निर्माण - भारतीय संविधान सभा, दर्शन और प्रस्तावना", "Homework": "संविधान की प्रस्तावना के मुख्य शब्द"},
                {"Topic_ID": "SS909", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 156, "End_Page": 170, "Topic": "Economics Ch 1: पालमपुर गाँव की कहानी - भूमि, श्रम, भौतिक व मानव पूंजी", "Homework": "हरित क्रांति के सकारात्मक व नकारात्मक प्रभाव"},
                {"Topic_ID": "SS910", "Class": "Class 9", "Subject": "Social Science", "Start_Page": 171, "End_Page": 190, "Topic": "Economics Ch 2: संसाधन के रूप में लोग - साक्षरता, स्वास्थ्य, बेरोजगारी", "Homework": "शिक्षित बेरोजगारी भारत के लिए चुनौती क्यों है?"},

                # === CLASS 10 MATHEMATICS ===
                {"Topic_ID": "M1001", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 1, "End_Page": 18, "Topic": "Ch 1: वास्तविक संख्याएं (Real Numbers) - अंकगणित की आधारभूत प्रमेय, अपरिमेयता", "Homework": "Ex 1.1 & 1.2 Complete"},
                {"Topic_ID": "M1002", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 19, "End_Page": 38, "Topic": "Ch 2: बहुपद (Polynomials) - शून्यकों का ज्यामितीय अर्थ, गुणांकों में संबंध", "Homework": "Ex 2.1 & 2.2 Complete"},
                {"Topic_ID": "M1003", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 39, "End_Page": 70, "Topic": "Ch 3: रैखिक समीकरण युग्म - प्रतिस्थापन, विलोपन, संगत/असंगत शर्तें", "Homework": "Ex 3.1 to 3.3 Selected Qs"},
                {"Topic_ID": "M1004", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 71, "End_Page": 98, "Topic": "Ch 4: द्विघात समीकरण (Quadratic Equations) - गुणनखंड हल, द्विघाती सूत्र, विविक्तकर", "Homework": "Ex 4.1 to 4.3 Selected Qs"},
                {"Topic_ID": "M1005", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 99, "End_Page": 124, "Topic": "Ch 5: समांतर श्रेढ़ियाँ (AP) - n-वाँ पद ($a_n$), प्रथम n पदों का योग ($S_n$)", "Homework": "Ex 5.2 & 5.3 Selected Qs"},
                {"Topic_ID": "M1006", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 125, "End_Page": 164, "Topic": "Ch 6: त्रिभुज (Triangles) - समरूपता कसौटियाँ, थेल्स प्रमेय (BPT)", "Homework": "Ex 6.1 & 6.2 Complete"},
                {"Topic_ID": "M1007", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 165, "End_Page": 186, "Topic": "Ch 7: निर्देशांक ज्यामिति - दूरी सूत्र, विभाजन सूत्र (Section Formula)", "Homework": "Ex 7.1 & 7.2 Complete"},
                {"Topic_ID": "M1008", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 187, "End_Page": 214, "Topic": "Ch 8: त्रिकोणमिति का परिचय - त्रिकोणमितीय अनुपात, विशिष्ट कोण, सर्वसमिकाएं", "Homework": "Ex 8.1 & 8.3 Selected Qs"},
                {"Topic_ID": "M1009", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 215, "End_Page": 232, "Topic": "Ch 9: त्रिकोणमिति के अनुप्रयोग - ऊँचाई और दूरी, उन्नयन व अवनमन कोण", "Homework": "Ex 9.1 Q1-Q8"},
                {"Topic_ID": "M1010", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 233, "End_Page": 248, "Topic": "Ch 10: वृत्त (Circles) - स्पर्श रेखाएं, बाह्य बिंदु से खींची गई स्पर्श रेखाओं की समानता", "Homework": "Ex 10.2 Complete"},
                {"Topic_ID": "M1011", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 249, "End_Page": 264, "Topic": "Ch 11: वृत्तों से संबंधित क्षेत्रफल - त्रिज्यखंड और वृत्तखंड का क्षेत्रफल", "Homework": "Ex 11.1 Complete"},
                {"Topic_ID": "M1012", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 265, "End_Page": 276, "Topic": "Ch 12: पृष्ठीय क्षेत्रफल और आयतन - ठोसों के संयोजन का क्षेत्रफल व आयतन", "Homework": "Ex 12.1 Selected Qs"},
                {"Topic_ID": "M1013", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 277, "End_Page": 296, "Topic": "Ch 13: सांख्यिकी (Statistics) - वर्गीकृत आंकड़ों का माध्य, बहुलक, माध्यक", "Homework": "Ex 13.1 to 13.3 Selected Qs"},
                {"Topic_ID": "M1014", "Class": "Class 10", "Subject": "Mathematics", "Start_Page": 297, "End_Page": 312, "Topic": "Ch 14: प्रायिकता (Probability) - सैद्धांतिक दृष्टिकोण, ताश व पासे के प्रश्न", "Homework": "Ex 14.1 Q1-Q15"},

                # === CLASS 10 SCIENCE ===
                {"Topic_ID": "S1001", "Class": "Class 10", "Subject": "Science", "Start_Page": 1, "End_Page": 17, "Topic": "Ch 1: रासायनिक अभिक्रियाएं एवं समीकरण - संतुलन, विस्थापन, अपचयन-उपचयन", "Homework": "अभ्यास के रासायनिक समीकरण संतुलित करना"},
                {"Topic_ID": "S1002", "Class": "Class 10", "Subject": "Science", "Start_Page": 18, "End_Page": 37, "Topic": "Ch 2: अम्ल, क्षारक एवं लवण - pH पैमाना, विरंजन चूर्ण, बेकिंग सोड़ा, पीओपी", "Homework": "लवणों के रासायनिक नाम व सूत्र"},
                {"Topic_ID": "S1003", "Class": "Class 10", "Subject": "Science", "Start_Page": 38, "End_Page": 59, "Topic": "Ch 3: धातु एवं अधातु - सक्रियता श्रेणी, आयनिक यौगिक, निष्कर्षण, संक्षारण", "Homework": "धातुओं व अधातुओं के रासायनिक अंतर"},
                {"Topic_ID": "S1004", "Class": "Class 10", "Subject": "Science", "Start_Page": 60, "End_Page": 79, "Topic": "Ch 4: कार्बन एवं उसके यौगिक - सहसंयोजी आबंध, IUPAC नामकरण, साबुन-अपमार्जक", "Homework": "एथेनॉलिक अम्ल की रासायनिक अभिक्रियाएं"},
                {"Topic_ID": "S1005", "Class": "Class 10", "Subject": "Science", "Start_Page": 80, "End_Page": 98, "Topic": "Ch 5: जैव प्रक्रम - मानव पाचन, श्वसन, दोहरा परिसंचरण, वृक्काणु उत्सर्जन", "Homework": "नेफ्रॉन (वृक्काणु) की संरचना का नामांकित चित्र"},
                {"Topic_ID": "S1006", "Class": "Class 10", "Subject": "Science", "Start_Page": 99, "End_Page": 114, "Topic": "Ch 6: नियंत्रण एवं समन्वय - न्यूरॉन, प्रतिवर्ती चाप, अंतःस्रावी ग्रंथियाँ (हार्मोन)", "Homework": "तंत्रिका कोशिका का स्वच्छ चित्र"},
                {"Topic_ID": "S1007", "Class": "Class 10", "Subject": "Science", "Start_Page": 115, "End_Page": 132, "Topic": "Ch 7: जीव जनन कैसे करते हैं - द्विखंडन, पुनरुद्भवन, पुष्प संरचना, मानव जनन", "Homework": "नर व मादा जनन तंत्र के कार्य स्पष्ट करें"},
                {"Topic_ID": "S1008", "Class": "Class 10", "Subject": "Science", "Start_Page": 133, "End_Page": 149, "Topic": "Ch 8: आनुवंशिकता - मेंडेल के नियम (मोनोहाइब्रिड/डाईहाइब्रिड क्रॉस), लिंग निर्धारण", "Homework": "लिंग निर्धारण का चेकर बोर्ड आरेख"},
                {"Topic_ID": "S1009", "Class": "Class 10", "Subject": "Science", "Start_Page": 150, "End_Page": 169, "Topic": "Ch 9: प्रकाश – परावर्तन तथा अपवर्तन - किरण आरेख, दर्पण व लेंस सूत्र, अपवर्तनांक", "Homework": "लेंस सूत्र पर आधारित आंकिक प्रश्न"},
                {"Topic_ID": "S1010", "Class": "Class 10", "Subject": "Science", "Start_Page": 170, "End_Page": 184, "Topic": "Ch 10: मानव नेत्र तथा रंगबिरंगा संसार - निकट/दीर्घ दृष्टि दोष, प्रिज्म विक्षेपण, प्रकीर्णन", "Homework": "दृष्टि दोष निवारण के किरण आरेख"},
                {"Topic_ID": "S1011", "Class": "Class 10", "Subject": "Science", "Start_Page": 185, "End_Page": 204, "Topic": "Ch 11: विद्युत (Electricity) - ओम का नियम, श्रेणीक्रम व समांतर क्रम, जूल का तापन", "Homework": "प्रतिरोधों के संयोजन के आंकिक प्रश्न"},
                {"Topic_ID": "S1012", "Class": "Class 10", "Subject": "Science", "Start_Page": 205, "End_Page": 218, "Topic": "Ch 12: विद्युत धारा के चुंबकीय प्रभाव - चुंबकीय क्षेत्र रेखाएं, फ्लेमिंग नियम, सोलेनोइड", "Homework": "दाहिने हाथ के अंगूठे का नियम स्पष्ट करें"},
                {"Topic_ID": "S1013", "Class": "Class 10", "Subject": "Science", "Start_Page": 219, "End_Page": 230, "Topic": "Ch 13: हमारा पर्यावरण - पारितंत्र, ओजोन परत अवक्षय, जैव आवर्धन", "Homework": "आहार श्रृंखला में ऊर्जा प्रवाह का नियम"},

                # === CLASS 10 SOCIAL SCIENCE ===
                {"Topic_ID": "SS1001", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 1, "End_Page": 28, "Topic": "History Ch 1: यूरोप में राष्ट्रवाद का उदय - वियना कांग्रेस, मेत्सिनी, जर्मनी एकीकरण", "Homework": "जर्मनी के एकीकरण की प्रक्रिया पर नोट"},
                {"Topic_ID": "SS1002", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 29, "End_Page": 52, "Topic": "History Ch 2: भारत में राष्ट्रवाद - जलियांवाला बाग, रोलेट एक्ट, खिलाफत, सविनय अवज्ञा", "Homework": "गांधीजी की दांडी यात्रा का महत्व लिखो"},
                {"Topic_ID": "SS1003", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 53, "End_Page": 76, "Topic": "Geography Ch 1: संसाधन एवं विकास - वर्गीकरण, सतत पोषणीय विकास, मृदा प्रकार", "Homework": "काली मिट्टी और जलोढ़ मिट्टी में अंतर"},
                {"Topic_ID": "SS1004", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 77, "End_Page": 92, "Topic": "Geography Ch 2: वन एवं वन्य जीव संसाधन - जैव विविधता, संकटग्रस्त जातियां, चिपको आंदोलन", "Homework": "वन्यजीव संरक्षण अधिनियम 1972 के प्रावधान"},
                {"Topic_ID": "SS1005", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 93, "End_Page": 110, "Topic": "Geography Ch 3: जल संसाधन - बहुउद्देशीय परियोजनाएं, वर्षा जल संग्रहण तकनीक", "Homework": "बाँधों के सामाजिक-आर्थिक प्रभाव"},
                {"Topic_ID": "SS1006", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 111, "End_Page": 130, "Topic": "Civics Ch 1: सत्ता की साझेदारी - बेल्जियम का मॉडल, श्रीलंका में बहुसंख्यकवाद", "Homework": "श्रीलंका में गृहयुद्ध के प्रमुख कारण"},
                {"Topic_ID": "SS1007", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 131, "End_Page": 150, "Topic": "Civics Ch 2: संघवाद - संघीय व्यवस्था की विशेषताएं, भारत में विकेंद्रीकरण", "Homework": "स्थानीय सरकारों (पंचायती राज) के महत्व"},
                {"Topic_ID": "SS1008", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 151, "End_Page": 168, "Topic": "Economics Ch 1: विकास (Development) - राष्ट्रीय आय, प्रति व्यक्ति आय, एचडीआई सूचकांक", "Homework": "मानव विकास सूचकांक के तीन घटक"},
                {"Topic_ID": "SS1009", "Class": "Class 10", "Subject": "Social Science", "Start_Page": 169, "End_Page": 190, "Topic": "Economics Ch 2: भारतीय अर्थव्यवस्था के क्षेत्रक - प्राथमिक, द्वितीयक, तृतीयक, नरेगा", "Homework": "संगठित और असंगठित रोजगार में अंतर"}
            ])
        
        if sheet_name == "Teachers": return st.session_state["fallback_teachers"]
        elif sheet_name == "Diary": return st.session_state["fallback_diary"]
        else: return st.session_state["fallback_syllabus"]

def save_row_to_sheet(sheet_name, new_row_dict):
    new_df = pd.DataFrame([new_row_dict])
    if sheet_name == "Teachers":
        st.session_state["fallback_teachers"] = pd.concat([st.session_state["fallback_teachers"], new_df], ignore_index=True)
    elif sheet_name == "Diary":
        st.session_state["fallback_diary"] = pd.concat([st.s

On Tue, 14 Jul, 2026, 9:42 am Navdeep Singh, <n527navu@gmail.com> wrote:
https://nb7ikngm2appsrezcm2u9kz.streamlit.app/
