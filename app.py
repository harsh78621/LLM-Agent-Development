import streamlit as st
import openai

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # You can change the model as needed
        messages=[
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,  # Adjust the token limit as needed
        temperature=0.5  # Control creativity
    )
    return response.choices[0].message["content"].strip()

# Define the functions
def complete_code(partial_code):
    prompt = f"""
    Given the following partial Python code, complete it to make it a valid Python program:

    {partial_code}

    Return the completed code as a string.
    """

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content.strip()


# Debugging assistance function
def debug_code(error_message):
    prompt = f"""
    Given the following error message: 
    {error_message},
    suggest a fix and explain why this error occurs.
    Provide the corrected Python code as well.
    """
    response = ask_gpt(prompt) 
    response_text = response.choices[0].message["content"].strip()

    explanation_marker = "Here is the corrected code:"  # Identifies the start of the code block
    if explanation_marker in response_text:
        explanation = response_text.split(explanation_marker)[0].strip()  # Before the marker
        code_block = response_text.split(explanation_marker)[1].strip()  # After the marker
        
        # Format the code block for proper display
        formatted_code = '\n'.join(code_block.split('\n'))  # Ensure correct newlines and indentation
    else:
        # Fallback if the marker isn't found
        explanation = response_text
        formatted_code = ""
    
    return explanation, formatted_code

# Documentation retrieval function
def documentation(query):
    prompt = f"Provide a Example and documentation for:\n{query}"
    return ask_gpt(prompt)

def main():
    # Define the application title and header
    st.title("Code Utility App")
    st.header("What would you like to do?")

    # Create a select box for user input
    selectbox = st.selectbox("Select an option", ("Complete code", "Debug code", "Documentation"))

    # Get the user input
    selected_option = selectbox

    # Add a text input field for additional user input
    text_input = st.text_area("Please enter any additional information or instructions")

    # Display the user's selection
    st.write("You selected:", selected_option)

    # Add a submit button
    if st.button("Submit"):
        # Access the function based on the selected option
        if selected_option == "Complete code":
            output = complete_code(text_input)
            st.code(output, language='python')
        elif selected_option == "Debug code":
            explanation, corrected_code = debug_code(text_input)  # Get both explanation and code
            # Display the explanation as plain text
            st.write("Debugging Suggestion:", explanation)
            # Display the corrected code with syntax highlighting
            st.code(corrected_code, language='python')
        elif selected_option == "Documentation":
            output = documentation(text_input)
            # Print the output from the function
            st.write("Output:", output)
        

# Run the main function
if __name__ == "__main__":
    main()
