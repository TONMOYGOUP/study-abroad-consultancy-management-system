from database import init_db, add_faq


# =========================================================
# PVC GLOBAL FAQ KNOWLEDGE BASE
# =========================================================

faqs = [

    # =====================================================
    # GENERAL / ADMISSION
    # =====================================================

    {
        "category": "Admission",
        "question": "How do I start my study abroad journey?",
        "answer": "Start by discussing your academic background, preferred destination, intended course, budget, and career goals with a PVC Global counsellor. We can then help you shortlist suitable study options and explain the next steps.",
        "keywords": "study abroad, start, admission, counselling, application"
    },

    {
        "category": "Admission",
        "question": "How does PVC Global help students?",
        "answer": "PVC Global provides guidance on destination selection, course and university selection, application preparation, document guidance, scholarship information, visa preparation, and pre-departure support.",
        "keywords": "PVC Global, services, help, student support"
    },

    {
        "category": "Admission",
        "question": "How do I choose the right course?",
        "answer": "The right course depends on your previous education, career goals, interests, academic strengths, budget, and preferred destination. PVC Global can help you compare suitable course options.",
        "keywords": "course, subject, degree, choose course, program"
    },

    {
        "category": "Admission",
        "question": "Can I study abroad with an average academic result?",
        "answer": "Yes. Many institutions offer programs for students with different academic profiles. Eligibility depends on the specific university, course, qualification, and destination.",
        "keywords": "average result, GPA, academic result, eligibility"
    },

    {
        "category": "Admission",
        "question": "Can I apply to more than one university?",
        "answer": "Yes. Applying to multiple suitable universities can increase your options. The number of applications should be planned according to your profile, budget, deadlines, and admission strategy.",
        "keywords": "multiple university, applications, apply university"
    },

    {
        "category": "Admission",
        "question": "When should I start my application?",
        "answer": "It is generally better to begin several months before your intended intake. Early preparation gives you more time for university selection, documents, English tests, applications, and visa preparation.",
        "keywords": "application time, intake, deadline, apply early"
    },

    {
        "category": "Admission",
        "question": "Which intake should I choose?",
        "answer": "The best intake depends on your preferred university, course availability, application deadlines, academic preparation, and visa timeline. PVC Global can help you compare available intake options.",
        "keywords": "intake, January intake, September intake, admission intake"
    },

    {
        "category": "Admission",
        "question": "Can I change my course after receiving an offer?",
        "answer": "Course changes depend on the university and stage of the admission process. Some institutions may allow changes before enrolment, while others require a new application.",
        "keywords": "change course, course change, offer letter"
    },

    # =====================================================
    # DOCUMENTS
    # =====================================================

    {
        "category": "Documents",
        "question": "What documents are usually required for university applications?",
        "answer": "Common documents may include academic certificates and transcripts, passport, English language test results where required, CV or resume, statement of purpose, recommendation letters, photographs, and other course-specific documents.",
        "keywords": "documents, university documents, transcript, passport, SOP, CV"
    },

    {
        "category": "Documents",
        "question": "Do I need a passport before applying?",
        "answer": "A valid passport is commonly required for international applications and visa processing. Requirements can vary, so it is best to have a valid passport prepared before starting the full process.",
        "keywords": "passport, application, documents"
    },

    {
        "category": "Documents",
        "question": "What is a Statement of Purpose?",
        "answer": "A Statement of Purpose, or SOP, is a written explanation of your academic background, goals, reasons for choosing a course and institution, and future plans. Its requirements vary by university.",
        "keywords": "SOP, statement of purpose, personal statement"
    },

    {
        "category": "Documents",
        "question": "Do I need a CV for studying abroad?",
        "answer": "A CV may be required for certain courses, universities, scholarships, internships, or postgraduate applications. Whether it is mandatory depends on the specific application.",
        "keywords": "CV, resume, documents"
    },

    {
        "category": "Documents",
        "question": "What are academic transcripts?",
        "answer": "Academic transcripts are official records showing the subjects you studied and the grades or marks you achieved. Universities commonly use them to assess academic eligibility.",
        "keywords": "transcript, academic transcript, marksheet"
    },

    {
        "category": "Documents",
        "question": "Can I apply before receiving my final certificate?",
        "answer": "Some universities allow students to apply using available academic documents and provide final certificates later. The exact policy depends on the institution and course.",
        "keywords": "final certificate, provisional, apply before certificate"
    },

    # =====================================================
    # IELTS / ENGLISH
    # =====================================================

    {
        "category": "IELTS",
        "question": "Do I need IELTS to study abroad?",
        "answer": "English language requirements depend on the destination, university, course, and your previous education. IELTS is common, but some institutions may accept other English tests or specific exemptions.",
        "keywords": "IELTS, English, English test, language requirement"
    },

    {
        "category": "IELTS",
        "question": "What IELTS score do I need?",
        "answer": "Required IELTS scores vary by university and course. Many programs have minimum overall and individual band requirements, so the exact requirement should be checked for the specific program.",
        "keywords": "IELTS score, IELTS requirement, band score"
    },

    {
        "category": "IELTS",
        "question": "Can I study abroad without IELTS?",
        "answer": "In some cases, universities may accept alternative English tests or provide exemptions based on previous education or other conditions. This depends entirely on the institution and course.",
        "keywords": "without IELTS, IELTS alternative, English exemption"
    },

    {
        "category": "IELTS",
        "question": "Which English tests are commonly accepted?",
        "answer": "Depending on the institution, commonly accepted tests may include IELTS, TOEFL, PTE, and other approved English language tests.",
        "keywords": "TOEFL, PTE, IELTS, English test"
    },

    {
        "category": "IELTS",
        "question": "Can I apply if I have not taken IELTS yet?",
        "answer": "Some universities may allow applications before the English test result is available, while others require proof of English proficiency during application. The policy varies by institution.",
        "keywords": "IELTS pending, apply without result, English test pending"
    },

    # =====================================================
    # UK
    # =====================================================

    {
        "category": "UK",
        "question": "Why do students choose the United Kingdom?",
        "answer": "The UK is popular for its internationally recognized universities, a wide range of programs, strong academic reputation, and comparatively structured degree pathways.",
        "keywords": "UK, United Kingdom, study UK, benefits"
    },

    {
        "category": "UK",
        "question": "How long does a typical master's degree take in the UK?",
        "answer": "Many full-time taught master's programs in the UK can be completed in about one year, although the duration varies by program and institution.",
        "keywords": "UK masters, master's duration, UK degree"
    },

    {
        "category": "UK",
        "question": "Can international students work while studying in the UK?",
        "answer": "Work conditions depend on your visa type and current immigration rules. Students should check the official UK government guidance and the conditions attached to their visa.",
        "keywords": "UK work, student work, UK student visa"
    },

    {
        "category": "UK",
        "question": "What is a CAS in the UK admission process?",
        "answer": "CAS stands for Confirmation of Acceptance for Studies. It is an electronic document issued by a UK institution to an eligible student and is used as part of the Student visa application process.",
        "keywords": "CAS, UK CAS, confirmation acceptance studies"
    },

    # =====================================================
    # CANADA
    # =====================================================

    {
        "category": "Canada",
        "question": "Why do students choose Canada?",
        "answer": "Canada is known for its diverse educational institutions, internationally respected programs, multicultural environment, and a wide range of study options for international students.",
        "keywords": "Canada, study Canada, benefits"
    },

    {
        "category": "Canada",
        "question": "What English score is required for Canada?",
        "answer": "English requirements vary by institution and program. Universities and colleges may set different overall and individual score requirements, so the exact program requirement should be checked.",
        "keywords": "Canada IELTS, Canada English score, language requirement"
    },

    {
        "category": "Canada",
        "question": "Can international students work while studying in Canada?",
        "answer": "Work eligibility depends on your study permit and the rules in effect when you study. Students should always verify the latest conditions through official Canadian government sources.",
        "keywords": "Canada work, student job, study permit"
    },

    {
        "category": "Canada",
        "question": "What is a study permit?",
        "answer": "A study permit is the document issued by the Canadian government that generally allows an eligible international student to study at a designated learning institution in Canada.",
        "keywords": "study permit, Canada visa, Canada student"
    },

    # =====================================================
    # AUSTRALIA
    # =====================================================

    {
        "category": "Australia",
        "question": "Why is Australia a popular study destination?",
        "answer": "Australia offers a wide selection of universities and institutions, internationally recognized qualifications, diverse programs, and a strong international student community.",
        "keywords": "Australia, study Australia, benefits"
    },

    {
        "category": "Australia",
        "question": "What is a CoE in Australia?",
        "answer": "CoE stands for Confirmation of Enrolment. It is an official document issued by an Australian education provider after enrolment requirements are completed and is used in the student visa process.",
        "keywords": "CoE, confirmation enrolment, Australia"
    },

    {
        "category": "Australia",
        "question": "Can students work while studying in Australia?",
        "answer": "International student work rights depend on the visa conditions applicable to the student. Always check the latest Australian government requirements before relying on any work-related information.",
        "keywords": "Australia work, student job, work rights"
    },

    {
        "category": "Australia",
        "question": "Do Australian universities require IELTS?",
        "answer": "Many Australian institutions require proof of English proficiency, but accepted tests and minimum scores vary by university and program.",
        "keywords": "Australia IELTS, English requirement, language test"
    },

    # =====================================================
    # USA
    # =====================================================

    {
        "category": "USA",
        "question": "Why should I consider studying in the United States?",
        "answer": "The United States offers a large range of universities, programs, research opportunities, and specialized fields of study. Students can choose from institutions with different academic strengths and admission requirements.",
        "keywords": "USA, United States, study USA"
    },

    {
        "category": "USA",
        "question": "Do US universities require standardized tests?",
        "answer": "Requirements vary significantly by university and program. Some institutions may have test policies that differ by applicant or course, so current university-specific requirements should be checked.",
        "keywords": "SAT, GRE, GMAT, standardized test, USA"
    },

    {
        "category": "USA",
        "question": "What is an F-1 student visa?",
        "answer": "The F-1 visa is a U.S. nonimmigrant visa category generally used by eligible students who want to study at an approved academic institution in the United States.",
        "keywords": "F1, F-1 visa, USA student visa"
    },

    {
        "category": "USA",
        "question": "Can international students work in the USA?",
        "answer": "Employment for international students is subject to immigration rules and the conditions of their status. Work authorization is not automatic for all types of employment.",
        "keywords": "USA work, F1 work, student job"
    },

    # =====================================================
    # GERMANY
    # =====================================================

    {
        "category": "Germany",
        "question": "Why do students choose Germany?",
        "answer": "Germany is attractive to international students because of its strong universities, research environment, engineering and technology programs, and a range of study options.",
        "keywords": "Germany, study Germany, benefits"
    },

    {
        "category": "Germany",
        "question": "Are there English-taught programs in Germany?",
        "answer": "Yes. Many German universities offer English-taught programs, particularly at the master's level. Availability depends on the university and subject area.",
        "keywords": "Germany English program, English taught Germany"
    },

    {
        "category": "Germany",
        "question": "Do I need German language skills to study in Germany?",
        "answer": "Not always. English-taught programs generally have English language requirements instead. German language requirements may apply to German-taught programs or specific situations.",
        "keywords": "German language, Germany IELTS, English program"
    },

    {
        "category": "Germany",
        "question": "What is a blocked account?",
        "answer": "A blocked account is a financial arrangement used by many international students to demonstrate access to required living funds for certain German visa processes. Exact financial requirements can change and should be checked against current official guidance.",
        "keywords": "blocked account, Germany visa, financial proof"
    },

    # =====================================================
    # ITALY
    # =====================================================

    {
        "category": "Italy",
        "question": "Why study in Italy?",
        "answer": "Italy offers universities with long academic traditions, a variety of programs, cultural experiences, and study opportunities across many fields.",
        "keywords": "Italy, study Italy, benefits"
    },

    {
        "category": "Italy",
        "question": "Are scholarships available in Italy?",
        "answer": "Scholarship and financial support opportunities may be available through universities, regional programs, and other institutions. Eligibility and application requirements vary.",
        "keywords": "Italy scholarship, scholarship Italy, funding"
    },

    {
        "category": "Italy",
        "question": "Are English-taught programs available in Italy?",
        "answer": "Yes. A number of Italian universities offer English-taught programs, especially at the master's level. Availability depends on the university and subject.",
        "keywords": "Italy English program, English taught Italy"
    },

    # =====================================================
    # SCHOLARSHIPS
    # =====================================================

    {
        "category": "Scholarship",
        "question": "Can international students get scholarships?",
        "answer": "Yes. Depending on the destination and institution, scholarships may be available based on academic performance, financial need, merit, subject area, or other criteria.",
        "keywords": "scholarship, international student, funding"
    },

    {
        "category": "Scholarship",
        "question": "How can I improve my scholarship chances?",
        "answer": "Strong academic performance, a clear statement of purpose, relevant achievements, extracurricular activities, research experience where applicable, and meeting all application requirements can strengthen a scholarship application.",
        "keywords": "scholarship chances, merit, funding"
    },

    {
        "category": "Scholarship",
        "question": "Does PVC Global guarantee a scholarship?",
        "answer": "No. Scholarship decisions are made by universities or scholarship providers. PVC Global can provide guidance about available opportunities and application preparation, but cannot guarantee an award.",
        "keywords": "scholarship guarantee, PVC Global scholarship"
    },

    {
        "category": "Scholarship",
        "question": "Can I apply for scholarships after receiving admission?",
        "answer": "Some scholarships require applications before or together with admission, while others can be applied for after admission. The timeline depends on the specific scholarship.",
        "keywords": "scholarship after admission, scholarship deadline"
    },

    # =====================================================
    # VISA
    # =====================================================

    {
        "category": "Visa",
        "question": "Does PVC Global help with visa preparation?",
        "answer": "Yes. PVC Global can guide students through document preparation, application steps, and general visa preparation. Final visa decisions are made by the relevant immigration authority.",
        "keywords": "visa, visa assistance, visa guidance"
    },

    {
        "category": "Visa",
        "question": "Can PVC Global guarantee my visa?",
        "answer": "No. No consultancy can guarantee a visa decision. Visa applications are assessed by the relevant government authority according to its rules and the applicant's circumstances.",
        "keywords": "visa guarantee, visa approval"
    },

    {
        "category": "Visa",
        "question": "What financial documents may be needed for a student visa?",
        "answer": "Financial evidence varies by destination and visa type. It may include bank statements, sponsorship evidence, scholarship letters, deposits, or other accepted proof of funds.",
        "keywords": "financial documents, bank statement, visa funds"
    },

    {
        "category": "Visa",
        "question": "How long does visa processing take?",
        "answer": "Visa processing times vary by country, visa category, application volume, season, and individual circumstances. Applicants should check the latest official processing-time guidance for their destination.",
        "keywords": "visa processing time, visa timeline"
    },

    # =====================================================
    # APPLICATION PROCESS
    # =====================================================

    {
        "category": "Application Process",
        "question": "What happens after I choose a university?",
        "answer": "The next steps typically include reviewing eligibility, preparing documents, completing the application, submitting supporting materials, tracking the application, and responding to any requests from the institution.",
        "keywords": "after university selection, application process"
    },

    {
        "category": "Application Process",
        "question": "How do I track my university application?",
        "answer": "Tracking methods depend on the university. Some institutions provide an applicant portal or email updates where you can monitor application progress.",
        "keywords": "application tracking, university portal"
    },

    {
        "category": "Application Process",
        "question": "What happens after receiving an offer letter?",
        "answer": "After receiving an offer, you should carefully review the conditions, meet any outstanding requirements, make required payments where applicable, and follow the institution's instructions for enrolment and visa preparation.",
        "keywords": "offer letter, admission offer, next step"
    },

    {
        "category": "Application Process",
        "question": "What is a conditional offer?",
        "answer": "A conditional offer means the university is offering admission subject to one or more requirements being completed, such as submitting a final certificate, meeting an English requirement, or providing additional documents.",
        "keywords": "conditional offer, offer letter"
    },

    {
        "category": "Application Process",
        "question": "What is an unconditional offer?",
        "answer": "An unconditional offer generally means the university has confirmed admission without outstanding academic or document conditions, although other enrolment steps may still remain.",
        "keywords": "unconditional offer, admission"
    },

    # =====================================================
    # PRE-DEPARTURE
    # =====================================================

    {
        "category": "Pre-Departure",
        "question": "What is pre-departure support?",
        "answer": "Pre-departure support helps students prepare for travel and arrival. Topics may include travel planning, accommodation, essential documents, budgeting, and practical preparation.",
        "keywords": "pre departure, travel, accommodation, preparation"
    },

    {
        "category": "Pre-Departure",
        "question": "Should I arrange accommodation before traveling?",
        "answer": "It is generally advisable to have a suitable accommodation plan before traveling. Options may include university accommodation, private housing, or other student housing arrangements.",
        "keywords": "accommodation, housing, student housing"
    },

    {
        "category": "Pre-Departure",
        "question": "What should I carry when traveling for study?",
        "answer": "Students should organize essential travel and academic documents, passport and visa, admission documents, financial information, medication where applicable, and other necessary personal items.",
        "keywords": "travel documents, packing, departure"
    }

]


# =========================================================
# INSERT FAQS
# =========================================================

def seed_faqs():

    init_db()

    added = 0
    skipped = 0

    from database import get_connection

    conn = get_connection()
    cursor = conn.cursor()

    for faq in faqs:

        # Prevent duplicate questions
        cursor.execute(
            """
            SELECT id
            FROM faqs
            WHERE question = ?
            """,
            (faq["question"],)
        )

        existing = cursor.fetchone()

        if existing:
            skipped += 1
            continue

        cursor.execute(
            """
            INSERT INTO faqs
            (
                category,
                question,
                answer,
                keywords
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                faq["category"],
                faq["question"],
                faq["answer"],
                faq["keywords"]
            )
        )

        added += 1

    conn.commit()
    conn.close()

    print()
    print("==============================================")
    print("PVC GLOBAL FAQ KNOWLEDGE BASE")
    print("==============================================")
    print(f"FAQ added   : {added}")
    print(f"FAQ skipped : {skipped}")
    print(f"Total FAQs  : {len(faqs)}")
    print("==============================================")
    print("FAQ database setup completed.")
    print()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":
    seed_faqs()