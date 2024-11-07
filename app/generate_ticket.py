from flask import Flask, render_template, request, redirect, url_for, session, flash
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import qrcode
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Admin credentials
ADMIN_USERNAME = 'vinod'
ADMIN_PASSWORD = 'tarun'

# Route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('generate_ticket_form'))
        else:
            return "Invalid Credentials. Try again."
    return render_template('login.html')


# Route for logout
@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    flash("You have been logged out.")  # Flash message for logout
    return redirect(url_for('login'))  # Redirect to login page

@app.route('/generate_ticket', methods=['GET', 'POST'])
def generate_ticket_form():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Gather form data
        customer_data = {
            "name": request.form['name'],
            "address": request.form['address'],
            "contact": request.form['contact'],
            "email": request.form['email'],
            "adults": request.form['adults'],
            "children_below_3": request.form['children_below_3'],
            "children_above_3": request.form['children_above_3'],
        }

        # Generate the PDF ticket
        pdf_path = generate_ticket_pdf(customer_data)

        # Send the email with the ticket PDF
        send_email(customer_data['email'], pdf_path)  # Use customer's email

        # Redirect back to the ticket generation form with a success message
        return redirect(url_for('generate_ticket_form', success=True))

    # Check for success message in the query parameters
    success = request.args.get('success')
    return render_template('index.html', success=success)



# Route for customer ticket generation form
#@app.route('/generate_ticket', methods=['GET', 'POST'])
def generate_ticket_form_old():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    if request.method == 'POST':
        # Gather form data
        customer_data = {
            "name": request.form['name'],
            "address": request.form['address'],
            "contact": request.form['contact'],
            "email": request.form['email'],
            "adults": request.form['adults'],
            "children_below_3": request.form['children_below_3'],
            "children_above_3": request.form['children_above_3'],
        }
        
        try:

            # Generate the PDF ticket
            pdf_path = generate_ticket_pdf(customer_data)

            # Send the email with the ticket PDF
            send_email(customer_data['email'], pdf_path)  # Use customer's email

            flash('Ticket generated and emailed successfully!', 'success')
        except Exception as e:
            flash('Failed to generate the ticket. Please try again.', 'error')

        return "Ticket Generated and Emailed"
    return render_template('index.html')

def generate_ticket_pdf(customer_data):
    # Create QR code data including children details
    qr_data = (
        f"Name: {customer_data['name']}\n"
        f"Address: {customer_data['address']}\n"
        f"Contact: {customer_data['contact']}\n"
        f"Adults: {customer_data['adults']}\n"
        f"Children Below 3: {customer_data['children_below_3']}\n"
        f"Children Above 3: {customer_data['children_above_3']}"
    )
    qr_img = qrcode.make(qr_data)
    qr_path = os.path.join('ticket_qr.png')
    qr_img.save(qr_path)

    # Generate the PDF
    pdf_path = os.path.join(f"ticket_{customer_data['name']}.pdf")
    pdf = canvas.Canvas(pdf_path, pagesize=letter)

    # Draw background
    pdf.drawImage('static/background.jpg', 0, 0, width=612, height=792)

    # Title and message
    pdf.setFont("Helvetica-Bold", 26)
    pdf.drawString(100, 740, "Longford Diwali Event: 2nd November")
    pdf.setFont("Helvetica", 18)
    pdf.drawString(100, 650, f"Hello {customer_data['name']}")

    # Venue details
    pdf.setFont("Helvetica", 14)
    pdf.drawString(100, 620, "Venue Address:")
    pdf.drawString(100, 600, "Temperance Hall, New St, Townparks, Longford, N39 R9X8")
    
    # Add a line gap after venue details
    pdf.drawString(100, 590, "")  # Empty line

    # Contact details
    pdf.drawString(100, 560, "Contacts:")
    pdf.drawString(100, 540, "0899820779 / 0892704476")
    pdf.drawString(100, 520, "Email: cshefali43@gmail.com / nickiesrules@gmail.com")

    # Add a line gap after contact details
    pdf.drawString(100, 510, "")  # Empty line

    # Event Date and Time
    pdf.drawString(100, 480, "Date and Time:")
    pdf.drawString(100, 460, "2nd November, Time: 5 pm - 9 pm")

    # Add details about the number of attendees
    pdf.drawString(100, 420, "Number of attendees:")
    pdf.drawString(100, 400, f"Adults: {customer_data['adults']}")
    pdf.drawString(100, 380, f"Children Below 3: {customer_data['children_below_3']}")
    pdf.drawString(100, 360, f"Children Above 3: {customer_data['children_above_3']}")

    # Add a line gap before QR code
    pdf.drawString(100, 320, "")  # Empty line

    # Add QR Code to the PDF
    pdf.drawImage(qr_path, 100, 150, width=150, height=150)

    # Save the PDF
    pdf.save()
    
    return pdf_path  # Return the path for emailing

def send_email(customer_email, pdf_path):
    sender_email = "vinoddublin@gmail.com"
    sender_password = "vzvc tzwo spqa ewvr"  # Change this to your actual password
    subject = "Your Longford Diwali Event Ticket"
    message = f"Dear {customer_email.split('@')[0]},\n\nPlease find attached your ticket for the Longford Diwali Event."

    # Set up the MIME
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = customer_email
    msg['Subject'] = subject

    # Attach the body with the msg instance
    msg.attach(MIMEText(message, 'plain'))

    # Attach PDF
    with open(pdf_path, 'rb') as attachment:
        part = MIMEApplication(attachment.read(), Name=os.path.basename(pdf_path))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(pdf_path)}"'
        msg.attach(part)

    # Send email using SMTP
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

