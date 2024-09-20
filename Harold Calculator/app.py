from flask import Flask, render_template, request, flash

# Initialize the Flask application
app = Flask(__name__)
app.secret_key = 'some_secret'  # Required for enabling flash messages

@app.route('/', methods=['GET', 'POST'])
def index():
    """
    Handle the main page where users can input their prelim grade.
    
    If the request method is POST, it attempts to retrieve and process
    the 'prelim_grade' from the submitted form. It validates the input
    and calculates the required grades if applicable.
    
    Returns:
        Rendered HTML template for the index page. """
    if request.method == 'POST':
        try:
            # Attempt to convert prelim_grade from form data to a float
            prelim_grade = float(request.form['prelim_grade'])
            
            # Validate the prelim_grade to ensure it is within a valid range
            if not (0 <= prelim_grade <= 100):
                flash("Prelim grade must be between 0 and 100.")
            else:
                # Calculate the required grades based on the prelim_grade
                result = calculate_grades(prelim_grade)
                flash(result)  # Display the result to the user
        except ValueError:
            # Handle the case where input cannot be converted to float
            flash("Please enter a valid number for Prelim grade.")

    return render_template('index.html')  # Render the main index page

def calculate_grades(prelim):
    """
    Calculate the grades required for a student to pass based on 
    their prelim grade.

    Parameters:
        prelim (float): The prelim grade given by the user.

    Returns:
        str: A message indicating whether the student can pass and 
             if so, what the minimum required grades for the midterm 
             and final exams are.
    """
    passing_grade = 75  # The grade required to pass the subject
    max_midterm_final = 0.30 * 100 + 0.50 * 100  # Max possible points from midterm and final

    # Check if the prelim grade already passes the requirement
    if prelim >= passing_grade:
        return "You have already passed the subject."

    # Calculate the overall score needed to pass the subject
    required_overall_score = passing_grade - 0.20 * prelim

    # Check if it's possible to pass with the given prelim grade
    if required_overall_score > max_midterm_final:
        return "It is impossible to pass the subject with this Prelim grade."

    # Calculate the minimum grades needed for midterm and final exams
    min_midterm_final = required_overall_score / 0.80
    return f"Minimum Midterm and Final grades needed: {min_midterm_final:.2f}"

if __name__ == '__main__':
    app.run(debug=True)  # Run the application in debug mode for development purposes