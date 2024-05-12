# SDEV140-53P       #
# Katherine Alberto #
#####################


# Import necessary libraries
import tkinter as tk
from tkinter import messagebox
import json
import random
import pickle

# Main application window
class Application(tk.Tk):
    # Initialize the application window
    def __init__(self):
        super().__init__() # call th eparent class (tk.Tk) constructor
        self.title('Python Flashcard Quiz') # Set the window title
        self.geometry('400x300') # Set the window size
        self.protocol("WM_DELETE_WINDOW", self.on_exit) # Set the function to call when the window is closed

        # Create widgets
        self.create_widgets()
    
    # Function to create the widgets
    def create_widgets(self):
        # Create a Canvas widget to display the image
        self.canvas = tk.Canvas(self, width=700, height=200) # Create a Canvas widget
        self.canvas.pack() # Add the Canvas to the window
        
       # Load and display the image
        self.img1 = tk.PhotoImage(file='PythonEx.png')# Load the image
        self.img1 = self.img1.subsample(2, 2)  # Resizes image while keeping aspect ratio
        self.canvas.create_image(200, 100, image=self.img1) # Add the image to the Canvas

        # Create a label with a welcome message
        self.label1 = tk.Label(self, text="Welcome to Python Quiz Wiz!") # Create the label
        self.label1.pack() # Add the label to the window

        # Create a button to start the quiz
        self.button1 = tk.Button(self, text="Start Quiz", command=self.start_quiz) # Create the button
        self.button1.pack() # Add the button to the window
        
        # Create a button to exit the application
        self.button2 = tk.Button(self, text="Exit", command=self.on_exit) # Create the button
        self.button2.pack() # Add the button to the window
        
    # Function to start the quiz
    def start_quiz(self):
        try:
            # Try to load the saved state
            with open('save.pkl', 'rb') as f: # Open the save file
                flashcards, current_flashcard, score = pickle.load(f) # Load the saved state
        except (FileNotFoundError, pickle.UnpicklingError):
            # If there's no saved state, start a new quiz
            
            with open('flashcards.json', 'r') as f: # Open the flashcards file
                flashcards = json.load(f) # Load the flashcards
            random.shuffle(flashcards)  # Randomize the order of questions
            
            for flashcard in flashcards:
                correct_answer = flashcard['answers'][flashcard['correct_answer']]  # Get the correct answer before shuffling
                random.shuffle(flashcard['answers'])  # Randomize the order of answers
                flashcard['correct_answer'] = flashcard['answers'].index(correct_answer)  # Update the correct_answer index after shuffling
                
            current_flashcard = 0 # Start with the first flashcard
            score = 0 # Start with a score of 0
            

        # Open quiz window
        QuizWindow(self, flashcards=flashcards, current_flashcard=current_flashcard, score=score)
    
    # Function to handle the exit event
    def on_exit(self):
        if hasattr(self, 'exit_window') and self.exit_window.winfo_exists():
            # If the exit window already exists, bring it to the front
            self.exit_window.lift()
        else:
            # Otherwise, create a new exit window
            self.exit_window = tk.Toplevel(self) # Create a new window
            self.exit_window.title("Exit") # Set the window title
            self.exit_window.geometry('400x240') # Set the window size

            # Load and display the image
            img = tk.PhotoImage(file='python-1.png') # Load the image
            img = img.subsample(2, 2)  # Resizes image while keeping aspect ratio

            canvas = tk.Canvas(self.exit_window, width=200, height=100) # Create a Canvas widget
            canvas.pack() # Add the Canvas to the window
            canvas.create_image(100, 50, image=img) # Add the image to the Canvas

            label = tk.Label(self.exit_window, text="Do you want to quit the application?") # Create a label
            label.pack() # Add the label to the window

            yes_button = tk.Button(self.exit_window, text="Yes", command=self.destroy) # Create a button
            yes_button.pack(side="left") # Add the button to the left side of the window

            no_button = tk.Button(self.exit_window, text="No", command=self.exit_window.destroy) # Create a button
            no_button.pack(side="right") # Add the button to the right side of the window

            self.exit_window.mainloop() # Start the window's event loop
            

# Quiz window
class Flashcard(tk.Frame):
    # Initialize the flashcard
    def __init__(self, master=None, question=None, answers=None, correct_answer=None, **kwargs):
        super().__init__(master, **kwargs) # Call the parent class (tk.Frame) constructor
        self.question = question # The question text
        self.answers = answers # The list of answers
        self.correct_answer = correct_answer # The index of the correct answer
       
        self.create_widgets() # Create the widgets

    # Function to create the widgets
    def create_widgets(self):
        self.question_label = tk.Label(self, text=self.question) # Create a label for the question
        self.question_label.grid(row=1, column=0, sticky="w") # Left align the question
        
        self.flip_frame = tk.Frame(self)  # Create a new frame for the Flip button
        self.flip_frame.grid(row=2, column=0, sticky="nsew")  # Center the frame

        self.flip_button = tk.Button(self.flip_frame, text="Flip", command=self.flip_card, width=len("Flip")) # Create a Flip button
        self.flip_button.pack()  # Pack the Flip button inside the frame without any sticky option
       
        
        self.answer_var = tk.IntVar() # Initialize with an empty string
        self.answer_var.set(-1) # Set initial value to -1 to indicate no answer selected
        
        self.answer_widgets = []  # List to store answer widgets
        
        
        for i, answer in enumerate(self.answers):
            rb = tk.Radiobutton(self, text=answer, variable=self.answer_var, value=i+1) # Create a Radiobutton for each answer
            rb.grid(row=i+4, column=0, sticky="w") # Left align the Radiobutton
            rb.grid_remove()  # Hide the answer widget
            self.answer_widgets.append(rb) # Add the Radiobutton to the list of answer widgets

    # Function to flip the card        
    def flip_card(self):
        # Show the answers when the "Flip" button is clicked
        for rb in self.answer_widgets:
            rb.grid()  # Show the answer widget
        self.flip_button['state'] = 'disabled'  # Disable the "Flip" button after revealing answers
    
    # Function to deselect all answers
    def deselect_all(self):
        self.answer_var.set(0) # Deselect all radio buttons
        

 # Quiz window           
class QuizWindow(tk.Toplevel):
    # Initialize the quiz window
    def __init__(self, master=None, flashcards=None, current_flashcard=0, score=0, **kwargs):
        super().__init__(master, **kwargs) # Call the parent class (tk.Toplevel) constructor
        self.title('Quiz Window') # Set the window title
        self.geometry('400x250') # Set the window size

        self.flashcards = flashcards # The list of flashcards
        self.current_flashcard = current_flashcard # The index of the current flashcard
        self.score = score  # Initialize the score attribute

        # Create widgets
        self.create_widgets()

    # Function to create the widgets
    def create_widgets(self):
        # Create a Flashcard widget for the current flashcard
        self.flashcard_frame = Flashcard(self, question=self.flashcards[self.current_flashcard]['question'], answers=self.flashcards[self.current_flashcard]['answers'], correct_answer=self.flashcards[self.current_flashcard]['correct_answer'])
        self.flashcard_frame.pack(fill="both", expand=True) # Add the Flashcard to the window
        self.flashcard_frame.config(width=400, height=200) # Set the size of the Flashcard
        self.flashcard_frame.grid_propagate(False) # Prevent the Flashcard from resizing
        
        self.button_frame = tk.Frame(self)  # Creates a separate frame for the buttons
        self.button_frame.pack(side="bottom", fill="x") # Add the frame to the bottom of the window

        # Create a button to go to the previous flashcard
        self.previous_button = tk.Button(self.button_frame, text="Previous", command=self.previous_flashcard, state='disabled') # Creates the button and disables "Previous" button initially
        self.previous_button.pack(side="left")  # Add the button to the left side of the frame
        
        # Create a label to show the progress of the quiz
        self.progress_label = tk.Label(self.button_frame, text=f"Question {self.current_flashcard + 1} of {len(self.flashcards)}") # Create the label
        self.progress_label.pack(side="left", expand=True)  # Add the label to the left side of the frame
        
        # Create a button to go to the next flashcard
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_flashcard) # Create the button
        self.next_button.pack(side="right")  # Add the button to the right side of the frame

    # Function to go to the next flashcard
    def next_flashcard(self):
        # Check if an answer is selected
        selected_answer = self.flashcard_frame.answer_var.get()
        if selected_answer:
            # Check if the selected answer is correct
            # Subtract 1 from answer_var to make it 0-indexed
            if selected_answer - 1 == self.flashcard_frame.correct_answer:
                self.score += 1 # Increment the score
                
        self.flashcard_frame.deselect_all() # Deselects radio buttons before moving to the next question

        self.current_flashcard += 1 # Go to the next flashcard
        
        # Update the progress label after incrementing current_flashcard
        self.progress_label['text'] = f"Question {self.current_flashcard + 1} of {len(self.flashcards)}"

        if self.current_flashcard < len(self.flashcards):
            # If there are more flashcards, show the next one
            self.flashcard_frame.destroy() # Remove the current Flashcard
            self.flashcard_frame = Flashcard(self, question=self.flashcards[self.current_flashcard]['question'], answers=self.flashcards[self.current_flashcard]['answers'], correct_answer=self.flashcards[self.current_flashcard]['correct_answer']) # Create a new Flashcard
            self.flashcard_frame.pack(fill="both", expand=True) # Add the new Flashcard to the window

            # Enables the Previous button when moving to the next question
            self.previous_button['state'] = 'normal'

        else:
            # If there are no more flashcards, show the score and close the window
            
            self.next_button['state'] = 'disabled'  # Disable the "Next" button after the last question has been answered
            messagebox.showinfo("Quiz Complete", f"You've completed the quiz! Your score is {self.score}/{len(self.flashcards)}") # Show a message box with the score
            self.destroy() # Close the window
    
    # Function to go to the previous flashcard
    def previous_flashcard(self):
        self.current_flashcard -= 1 # Go to the previous flashcard
        
        # Update the progress label after decrementing current_flashcard
        self.progress_label['text'] = f"Question {self.current_flashcard + 1} of {len(self.flashcards)}"

        if self.current_flashcard >= 0:
            # If there are previous flashcards, show the previous one
            self.flashcard_frame.destroy() # Remove the current Flashcard
            self.flashcard_frame = Flashcard(self, question=self.flashcards[self.current_flashcard]['question'],
                                             answers=self.flashcards[self.current_flashcard]['answers'],
                                             correct_answer=self.flashcards[self.current_flashcard]['correct_answer']) # Create a new Flashcard
            self.flashcard_frame.pack(fill="both", expand=True)  # Add the new Flashcard to the window

        # Update the progress label
        self.progress_label['text'] = f"Question {self.current_flashcard + 1} of {len(self.flashcards)}"


# Main function
if __name__ == "__main__":
    app = Application()
    app.mainloop()
