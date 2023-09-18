import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random
import os


class Mail:
    emails = [
        {
            'subject': "Urgent: Student's Attendance Concerns",
            'body_message': '''
                I am writing to inform you about a situation regarding one of your students. Their attendance has sharply declined, putting them at risk of dropping out.

                We kindly request:
                  1. Review their attendance records.
                  2. Facilitate a meeting with parents, teachers, and support staff.
                  3. Implement an intervention plan.
                  4. Regular updates on progress.

                  We are committed to collaborating for your student's success.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Concerns About Student's Dropout",
            'body_message': '''
                I'm writing to address a concerning issue at your school. Your student will be dropping out, and there are indications that their decision may be related to their nationality.

                We take pride in fostering an inclusive, discrimination-free environment. Every student, irrespective of nationality or background, deserves equal opportunities.

                I kindly request your assistance in investigating the reasons behind the student's dropout to prevent similar situations in the future. I also propose a meeting involving their parents or guardians, and relevant school staff to explore reintegration options.

                Our mission is to ensure every student feels valued and supported. We're committed to addressing this issue promptly, eliminating nationality-based barriers to education.

                Thank you for your attention and collaboration.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Concerns About Student's Dropout",
            'body_message': '''
                I'm writing about your student of your school, facing recent academic challenges that could affect their grade level.

                We are dedicated to an inclusive, discrimination-free environment for all students. We need your assistance to investigate the reasons behind student's departure and prevent future incidents.

                I suggest a meeting involvingtheir parents, and relevant staff to explore reintegration options.

                Our goal is to ensure equal opportunities and eliminate nationality-based barriers to education.  Your cooperation is greatly appreciated!

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Urgent: Student Tuition Fee Delinquency and Risk of Dropout",
            'body_message': '''
                We write as a team to express our deep concern about your student, whose tuition fees have not been paid for an extended period. This puts your student at risk of discontinuing their education.


                We kindly request:

                 1. A tuition fee assessment to gauge the extent of delinquency.
                 2. Your guidance in exploring financial assistance options, both within the school and externally.
                 3. Delicate communication with family to emphasize our commitment to helping in financial challenges.
                 4. Provision of academic support to manage their studies during this period.
                 5. Regular updates on progress in resolving this financial situation.

                 We believe addressing this matter promptly and empathetically can ensure continued education and success.

                 Thank you for your dedication to our students' well-being.


                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Addressing the Impact of Educational Special Needs on School Dropout",
            'body_message': '''
                I hope this email finds you well. I am writing to bring to your attention a significant concern within our educational community regarding student dropout rates, particularly among those with special educational needs.

                It has come to our attention that students with special educational needs may face unique challenges that lead to higher dropout rates. Ensuring the success and well-being of all our students is at the core of our educational mission, and we believe it is imperative to address this issue effectively.

                To tackle this issue, we are proposing a comprehensive review of our support systems for students with special educational needs. We aim to identify and rectify any gaps in our services, ensuring that these students receive the personalized assistance required for their academic journey.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Student Displacement and Risk of Dropout",
            'body_message': '''
                 We write to highlight a pressing concern regarding a dedicated student of your school. Your student is currently facing displacement from their living arrangement, placing at risk of dropping out.

                We kindly request:

                 1. A confidential assessment of the extent of displacement.
                 2. Immediate support to ensure continued access to education.
                 3. Sensitive communication with family to explore solutions.
                 4. Academic accommodations to aid in managing studies during this period.
                 5. Regular updates on situation and its impact on education.

                Your commitment to our students' well-being is greatly appreciated.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Concerns About Student's Low Previous Qualifications and Risk of Dropout",
            'body_message': '''
                We are writing to express our concern regarding a current student of your school, who has a history of low previous qualifications. This situation raises the risk of potentially dropping out.

                To address this, we kindly request:

               1. A comprehensive academic assessment to understand current standing.
               2. Development of a personalized learning plan to provide tailored support.
               3. Assigning a mentor or counselor to monitor progress.
               4. Encouraging family engagement to create a collaborative support network.
               5. Regular updates on academic progress and interventions.

               We believe that with your guidance and our collaborative efforts, we can help [Student's Name] overcome previous challenges and ensure a successful academic journey.

                Thank you for your commitment to our students' success.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Addressing School Dropout Due to Financial Constraints",
            'body_message': '''
                I'm writing to address a pressing concern in our educational community - the growing number of students leaving due to financial difficulties.

                Our mission is to provide quality education and equal opportunities to all students. Unfortunately, financial constraints are causing some to drop out.

                We propose reviewing our support systems for financially challenged students, with input from parents, educators, counselors, and financial aid experts, to enhance assistance and prevent dropouts.

                Our goal is to create an inclusive and equitable learning environment for all students to succeed academically.

                Your expertise and support are crucial. Together, we can ensure no student's educational dreams are thwarted by financial challenges.

                Thank you for your attention and anticipated collaboration.

                Regards,
                Team StopDrop!
            '''
        },
        {
            'subject': "Addressing School Dropout Concerns Linked to Curriculum Results",
            'body_message': '''
                I hope this message finds you well. We are addressing a pressing issue in our educational community - an increasing number of student dropouts related to curriculum challenges.

                To tackle this, we propose a thorough curriculum review involving teachers, coordinators, administrators, and parents to enhance engagement and support for struggling students.

                Our goal is to create a more nurturing learning environment where all students can succeed academically.

                Your insights and collaboration are invaluable. Thank you for your attention to this matter and your participation in our efforts.

                Regards,
                Team StopDrop!
            '''
        }
    ]

    smtp_server = 'smtp.gmail.com'  # Replace with your SMTP server address
    smtp_port = 587  # Replace with your SMTP server's port (587 for TLS, 465 for SSL)

    def __init__(self, sender_mail, receiver_mail, authentication_app_key):
        self.sender_mail = sender_mail
        self.receiver_mail = receiver_mail
        self.authentication_app_key = authentication_app_key

    def send_mail(self):

        random_email=random.choice(self.emails)
        sender_email = self.sender_mail
        sender_password = self.authentication_app_key
        recipient_email = self.receiver_mail

        # msg
        subject = random_email['subject']
        content = random_email['body_message']
        #

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        body = MIMEText(content, 'plain')
        msg.attach(body)

        filename = 'Dropoutdataframe.csv'
        with open('Dropoutdataframe.csv', 'r') as dropout_csv:
            attachment = MIMEApplication(dropout_csv.read(), Name=filename)

        attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
        msg.attach(attachment)

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()  # Use TLS encryption
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
            server.quit()
            print("Email sent successfully!")
        except Exception as e:
            print(f"Email could not be sent. Error: {str(e)}")


